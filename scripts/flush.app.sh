aws s3 rm s3://$FRONTEND_BUCKET_NAME --recursive --profile ${PROFILE} --region ${REGION}
aws s3api delete-bucket --bucket $FRONTEND_BUCKET_NAME --profile ${PROFILE} --region ${REGION}