#!env/bin/python

ERROR_MESSAGES = {
    400 : 'No uri provided',
    401 : 'No query provided',
    430 : 'No grant type provided',
    431 : 'Invalid grant type',
    450 : 'No client id provided',
    451 : 'No client secret provided',
    500 : 'Client not found',
    600 : 'No refresh token',
    601 : 'Invlid refresh token',
}

def error(err_no=None):
    """Returns an error message with specified status code"""
    if err_no: return {
        "error": {
            "status": error,
            "message": ERROR_MESSAGES[error]
        }
    }

    return { "error": "No message" }
