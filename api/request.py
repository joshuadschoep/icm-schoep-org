from enum import Enum
from typing import List, Optional
from typing_extensions import Annotated
from pydantic import BaseModel, Field, PositiveInt, conlist, model_validator, ValidationError
from response import OptionsSuccess, ClientError, Response
from logging import getLogger

logger = getLogger(__name__)

class Player(BaseModel):
    name: Optional[Annotated[str, Field(min_length=1, max_length=63, frozen=True)]] = None
    stack: PositiveInt

class Request(BaseModel):
    payouts: conlist(PositiveInt, min_length=1, max_length=12)
    players: conlist(Player, min_length=1, max_length=12)

    @model_validator(mode='after')
    def more_players_than_payouts(self):
        if len(self.payouts) > len(self.players):
            raise ValidationError("There must be more players than remaining payouts")
        return self

# Checks headers, method, data format, etc
# Anything outside the body and content
def validateHttpContext(event) -> tuple[str, Response]:
    httpMethod = event["requestContext"]['http']['method']
    logger.debug("Validating HTTP method: {}".format(httpMethod))
    errorResponse = validateMethod(httpMethod)
    if errorResponse is not None:
        return "", errorResponse
    
    httpPath = event['rawPath'].split("/")
    logger.debug("Valid method: {}. Validating path: {}".format(httpMethod, httpPath))
    solutionMethod, errorResponse = validatePath(httpPath)
    if errorResponse is not None:
        return "", errorResponse
    
    logger.debug("Valid path: {}. Validating body and format: {}".format(httpPath, event['isBase64Encoded']))
    errorResponse = validateBodyFormat(event)
    if errorResponse is not None:
        return "", errorResponse

    return solutionMethod, None

def validateMethod(httpMethod) -> Response:
    if httpMethod == "OPTIONS":
        logger.info("Received OPTIONS request. Responding")
        return OptionsSuccess() 
    elif httpMethod != "POST":
        logger.warning("Received unsupported request: {}. Responding with error".format(httpMethod))
        return ClientError([
            "Method not supported: {}".format(httpMethod)
        ])
    return None

def validatePath(path: list[str]) -> tuple[str, Response]:
    solutionMethod = ""
    ## Should be expecting .../(malmuth-harville | tysen)
    if path[-1] == "malmuth-harville":
        solutionMethod = "malmuth"
    elif path[-1] == "tysen":
        solutionMethod = "tysen"
    else:
        logger.warning("Received unsupported solution method from path: {}".format(path))
        return "", ClientError([
            "Solution method from path not supported: {}".format(path[-1])
        ])
    return solutionMethod, None

def validateBodyFormat(event) -> Response:
    if event['isBase64Encoded']:
        logger.warning("Received unsupported body format: base64")
        return ClientError([
            "Only supports requests in JSON format"
        ]).toDict()
    elif 'body' not in event:
        logger.warning("Received request with no body")
        return ClientError([
            "Only supports requests in JSON format"
        ]).toDict()
    return None