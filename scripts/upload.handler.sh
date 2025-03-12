make handler.zip
chmod 644 handler.zip

FUNCTION_NAME=$(aws cloudformation describe-stacks --stack-name ${BACKEND_STACK_NAME} --profile ${PROFILE} --region ${REGION} | jq -r '.Stacks[0].Outputs[] | select(.OutputKey == "HandlerFunction").OutputValue')

aws lambda update-function-code --function-name ${FUNCTION_NAME} --profile ${PROFILE} --region ${REGION} --zip-file fileb://handler.zip