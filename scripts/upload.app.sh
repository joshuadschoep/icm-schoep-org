make app
aws s3 sync app/dist s3://$FRONTEND_BUCKET_NAME --profile ${PROFILE} --region ${REGION}