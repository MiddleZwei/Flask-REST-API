from flask import Response, json


def response(res, status_code):
    # response function
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
