import json
# Response objects and inheritence for Lambda & API Gateway.
# Expects format version 2.0. Creates only JSON responses.
# https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html#http-api-develop-integrations-lambda.response

class Response:
    def __init__(self, statusCode: int, body: dict):
        self.statusCode = statusCode
        self.body = body

    def toDict(self):
        return {
            "isBase64Encoded": False,
            "statusCode": self.statusCode,
            "headers": {
                "access-control-allow-origin": "*",
                "access-control-allow-headers": "content-type,accept",
                "accept": "application/json",
                "content-type": "appliction/json"
            },
            "body": json.dumps(self.body)
        }

class InternalError(Response):
    def __init__(self):
        super().__init__(500, {"message": "An internal server error has occured."})

class ClientError(Response):
    def __init__(self, errors):
        super().__init__(400, {
            "message": "Request is invalid",
            "errors": errors
        })

class OptionsSuccess(Response):
    def __init__(self, body: dict = {}):
        super().__init__(200, body)

    def toDict(self):
        # Probably unnecessary, but we want to have pretty
        # good control over CORS requests in proxy integrations
        return { 
            "statusCode": 200, 
            "isBase64Encoded": False,
            "headers": {
                'Access-Control-Allow-Headers': 'Content-Type,Accept',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            "body": json.dumps(self.body)
        }

class Success(Response):
    def __init__(self, body: dict = {}):
        super().__init__(200, body)