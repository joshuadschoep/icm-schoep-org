import json
from pydantic import ValidationError
from request import Request
from response import Success, ClientError
from malmuthharville import calculate
# https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html

def handler(event, _):
    print("New event", event)
    if event["requestContext"]['http']['method'] == "OPTIONS":
        print("Received an OPTIONS request, returning CORS")
        return { 
            "statusCode": 200, "headers": {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            }
        }

    if event['isBase64Encoded']:
        print("Cannot handle base64 encoded content, including x-form-encoded")
        return ClientError([
            "Only supports requests in JSON format"
        ]).toDict()
    elif 'body' not in event:
        print("Received request with no body")
        return ClientError([
            "Only supports requests in JSON format"
        ]).toDict()

    try:
        request = Request.model_validate_json(event['body'])
    except ValidationError as v:
        print(v)
        return ClientError(v.errors()).toDict()
    except Exception as e:
        print("Generic error", e)
        return ClientError([
            "Malformed input"
        ]).toDict()

    print("Request looks valid:", request)
    print("Attempting a Malmuth-Harville Solution")

    anon_stacks = [player.stack for player in request.players]
    result = list(calculate(request.payouts, anon_stacks))
    labeled_results = [{"stack": player.stack, "name": player.name, "payout": result[index]} for index, player in enumerate(request.players)]
    ordered_result_map = sorted([(result['payout'], result) for result in labeled_results], reverse=True)
    ordered_result_list = [result[1] for result in ordered_result_map]

    print("Success", ordered_result_list)

    return Success({
        "original_payouts": sorted(request.payouts, reverse=True),
        "results": ordered_result_list
    }).toDict()