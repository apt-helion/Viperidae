#!/usr/bin/env python

ERROR_MESSAGES = {
    # 400-409 missing arguments
    400 : 'No uri provided',
    401 : 'No query provided',
    402 : 'No grant type provided',
    404 : 'No client id provided',
    405 : 'No client secret provided',
    406 : 'No refresh token provided',

    # 410-419 <thing> not found
    410 : 'Client not found',
    411 : 'URL not found',

    # 500-509 invalid <thing>
    502 : 'Invalid authentication header',
    503 : 'Invalid header',

    # 550-569 general errors
}

def error(err_no=None):
    """Returns an error message with specified status code"""
    if err_no: return {
        "error": {
            "status": err_no,
            "message": ERROR_MESSAGES[err_no]
        }
    }

    return { "error": "No message" }
