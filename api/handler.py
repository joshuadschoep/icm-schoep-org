import signal
from pydantic import ValidationError
from request import Request, validateHttpContext
from response import Success, ClientError
from malmuthharville import calculate as mh_calculate
from tysen import calculate as tysen_calculate
from logging import getLogger
from time import process_time

logger = getLogger(__name__)

def handler(event, context):
    logger.info("New request", event)

    logger.debug("Setting alarm for aborting solution")
    signal.alarm((int(context.get_remaining_time_in_millis() / 1000)) - 1)

    logger.debug("Validating request context")
    solution_method, earlyResponse = validateHttpContext(event)
    if earlyResponse is not None:
        logger.warning('Received early response request. Responding')
        return earlyResponse.toDict()
    
    logger.debug("Validating request body")
    try:
        request = Request.model_validate_json(event['body'])
    except ValidationError as v:
        logger.warning("Request body failed validation. Responding")
        return ClientError(v.errors()).toDict()
    except Exception as e:
        logger.warning("Request body failed validation outside pydantic. Responding")
        return ClientError([
            "Malformed input"
        ]).toDict()

    logger.info("Beginning solution process", extra = {
            "signal": "BEGIN_SOLVE",
            "solution_method": solution_method,
            "payout_count": len(request.payouts),
            "player_count": len(request.players)
        }
    )
    begin_time = process_time()

    anon_stacks = [player.stack for player in request.players]
    result = []
    if solution_method == "malmuth":
        result = list(mh_calculate(request.payouts, anon_stacks))
    else:
        result = list(tysen_calculate(request.payouts, anon_stacks))

    end_time = process_time()
    logger.info(
        "Solution complete", extra={
        "signal": "END_SOLVE",
        "solution_method": solution_method,
        "duration": end_time - begin_time,
        "payout_count": len(request.payouts),
        "player_count": len(request.players)
    })

    labeled_results = [{"stack": player.stack, "name": player.name, "payout": result[index]} for index, player in enumerate(request.players)]
    ordered_result_map = sorted([(result['payout'], result) for result in labeled_results], reverse=True)
    ordered_result_list = [result[1] for result in ordered_result_map]

    sort_time = process_time()
    logger.info(
        "Sorting complete", extra={
        "signal": "END_SORT",
        "solution_method": solution_method,
        "duration": sort_time - end_time,
        "total_duration": sort_time - begin_time,
        "payout_count": len(request.payouts),
        "player_count": len(request.players)
    })

    logger.info("Solution complete and sorted. Responding")
    return Success({
        "original_payouts": sorted(request.payouts, reverse=True),
        "solution_method": solution_method,
        "results": ordered_result_list
    }).toDict()

def timeout_handler(_signal, _frame):
    '''Handle SIGALRM'''

    logger.info(
        "Aborting due to timeout", extra={
        "signal": "SOLVE_ABORT",
    })

    logger.warn("Solution took too long and will be aborted.")

    raise Exception('Time exceeded')

signal.signal(signal.SIGALRM, timeout_handler)