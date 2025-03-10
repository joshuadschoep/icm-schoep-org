#!/bin/bash
echo "Begin flush"

# Constants
REGION="us-east-1"

echo """
REGION: ${REGION}
TIMEOUT: ${TIMEOUT} minutes
PROFILE: ${PROFILE}
"""

# Args
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
    api) STACK_NAME=${API_STACK_NAME};;
    backend) STACK_NAME=${BACKEND_STACK_NAME};;
    frontend) STACK_NAME=${FRONTEND_STACK_NAME};;
esac

# Flow

## CFN Flush
echo "Begin delete"

DELETE_STACK_ARGS="--stack-name ${STACK_NAME} --region ${REGION}"

if [[ $PROFILE ]]; then
    DELETE_STACK_ARGS+=" --profile $PROFILE"
fi

echo "Deleting stack ${STACK_NAME} with args ${DELETE_STACK_ARGS}"
aws cloudformation delete-stack ${DELETE_STACK_ARGS}

if [ $? -ne 0 ]; then
    echo "Create stack failed with error code $?"
    exit 2
fi

## Wait

if [ -z $WAIT ]; then
    exit 0
fi

DESCRIBE_ARGS=""
if [[ $PROFILE ]]; then
    DESCRIBE_ARGS+=" --profile $PROFILE"
fi

while : 
do
    STACK_STATUS=$(aws cloudformation describe-stacks --stack-name ${STACK_NAME} --region ${REGION} ${DESCRIBE_ARGS} | jq -r ".Stacks[0].StackStatus")
    echo "Pinged stack and received status $STACK_STATUS"
    if [[ $STACK_STATUS == "DELETE_IN_PROGRESS" ]]; then
        sleep 5
    elif [[ $STACK_STATUS == "DELETE_COMPLETE" ]]; then
        break
    else
        echo "Unknown status: $STACK_STATUS"
        exit 2
    fi
done
