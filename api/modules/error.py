#!/usr/bin/python3.6

ERROR_MESSAGES = {
    400 : 'No uri provided',
    401 : 'No query provided',
    450 : 'No client id provided',
    451 : 'No client secret provided'
}

def die(error=None):
    """Returns an error message with specified status code"""
    if error: return {
        "error": {
            "status": error,
            "message": ERROR_MESSAGES[error]
        }
    }

    return { "error": "No message" }
