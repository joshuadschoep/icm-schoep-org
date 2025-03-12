#!/bin/bash
echo "Begin deploy"

# Constants
TIMEOUT=10

echo """
TEMPLATE_S3_URL: ${TEMPLATE_S3_URL}
TEMPLATE_HTTPS_URL: ${TEMPLATE_HTTPS_URL}
REGION: ${REGION}
TIMEOUT: ${TIMEOUT} minutes
PROFILE: ${PROFILE}
ENVIRONMENT: ${ENV}
"""

# Args
while getopts ":s:w" opt; do
    case $opt in
        s) STACK_TYPE="${OPTARG}"
        ;;
        w) WAIT=true
        ;;
    esac

    case $OPTARG in
        w) break;;
        -*) echo "Option $opt needs a valid argument"
        exit 1
        ;;
    esac
done

echo """
STACK_TYPE: ${STACK_TYPE}
WAIT: ${WAIT}
"""

case $STACK_TYPE in
    api) 
        SRC_FILE=infra/Api.yaml
        REMOTE_FILE=${API_TEMPLATE_NAME}
        STACK_NAME=${API_STACK_NAME}
        PARAMETERS="ParameterKey=DomainName,ParameterValue=${API_DOMAIN_NAME} \
            ParameterKey=ApiStageName,ParameterValue=${STAGE_NAME} \
            ParameterKey=LogRetention,ParameterValue=${LOG_RETENTION_DAYS} \
            ParameterKey=Environment,ParameterValue=${ENV}"
        ;;
    backend) 
        SRC_FILE=infra/Backend.yaml
        REMOTE_FILE=${BACKEND_TEMPLATE_NAME}
        STACK_NAME=${BACKEND_STACK_NAME}
        PARAMETERS="ParameterKey=MhPath,ParameterValue=${BACKEND_MH_PATH} \
            ParameterKey=TysenPath,ParameterValue=${BACKEND_TYSEN_PATH} \
            ParameterKey=ApiStackName,ParameterValue=${API_STACK_NAME} \
            ParameterKey=Environment,ParameterValue=${ENV}"
        ;;
    frontend)
        SRC_FILE=infra/App.yaml
        REMOTE_FILE=${FRONTEND_TEMPLATE_NAME}
        STACK_NAME=${FRONTEND_STACK_NAME}
        PARAMETERS="ParameterKey=HostedZone,ParameterValue=${HOSTED_ZONE} \
            ParameterKey=DomainName,ParameterValue=${FRONTEND_DOMAIN_NAME} \
            ParameterKey=BucketName,ParameterValue=${FRONTEND_BUCKET_NAME} \
            ParameterKey=Ttl,ParameterValue=${FRONTEND_CACHE_TTL}"
esac

# Flow

## S3 Copy
echo "Begin copy"

S3_ARGS=""
if [[ $PROFILE ]]; then
    S3_ARGS+=" --profile $PROFILE"
fi

echo "Copying ${SRC_FILE} to ${TEMPLATE_S3_URL}/${REMOTE_FILE} with args ${S3_ARGS}";
aws s3 cp ${SRC_FILE} ${TEMPLATE_S3_URL}/${REMOTE_FILE} ${S3_ARGS}

if [[ $? -ne 0 ]]; then
    echo "Copy failed with error code $?"
    exit 1
else
    echo "Copy success"
fi;

## CFN Update
echo "Begin Update"

CREATE_CHANGE_SET_ARGS="--stack-name ${STACK_NAME} --region ${REGION} --change-set-name CLIUpdate-$(date +%s) --template-url ${TEMPLATE_HTTPS_URL}/${REMOTE_FILE} --parameters ${PARAMETERS}"

if [[ $PROFILE ]]; then
    CREATE_CHANGE_SET_ARGS+=" --profile $PROFILE"
fi

echo "Updating stack ${STACK_NAME} from template ${REMOTE_FILE} with args ${CREATE_CHANGE_SET_ARGS}"
aws cloudformation create-change-set ${CREATE_CHANGE_SET_ARGS}

if [ $? -ne 0 ]; then
    echo "Create change set failed with error code $?"
    exit 2
fi

ChangeSet=$(aws cloudformation create-change-set ${CREATE_CHANGE_SET_ARGS} | jq -r .Id)
echo "Change set success: ${ChangeSet}"

## Wait for CS
echo "Waiting briefly"

sleep 10

## Execute 
echo "Begin execute"

EXECUTE_ARGS="--change-set-name ${ChangeSet} --region ${REGION}"
if [[ $PROFILE ]]; then
    EXECUTE_ARGS+=" --profile $PROFILE"
fi

echo "Executing changeset with ID ${ChangeSet} and args ${EXECUTE_ARGS}"
aws cloudformation execute-change-set ${EXECUTE_ARGS}


## Wait

if [ -z $WAIT ]; then
    exit 0
fi

DESCRIBE_ARGS="--stack-name ${STACK_NAME} --region ${REGION}"
if [[ $PROFILE ]]; then
    DESCRIBE_ARGS+=" --profile $PROFILE"
fi

while : 
do
    STACK_STATUS=$(aws cloudformation describe-stacks ${DESCRIBE_ARGS} | jq -r ".Stacks[0].StackStatus")
    echo "Pinged stack and received status $STACK_STATUS"
    if [[ $STACK_STATUS == "UPDATE_IN_PROGRESS" ]]; then
        sleep 5
    elif [[ $STACK_UPDATE == "UPDATE_ROLLBACK_IN_PROGRESS" ]]; then
        sleep 5
    elif [[ $STACK_UPDATE == "UPDATE_COMPLETE_CLEANUP_IN_PROGRESS" ]]; then
        sleep 5
    elif [[ $STACK_STATUS == "UPDATE_COMPLETE" ]]; then
        break
    else
        echo "Unknown status: $STACK_STATUS"
        exit 2
    fi
done
