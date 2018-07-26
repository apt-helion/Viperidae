Developer API
=============

Authorisation Header
^^^^^^^^^^^^^^^^^^^^

In every call to an API endpoint, an authenication header must be sent as well in order to auhtorise you application.

All requests must include an 'Authorisation' header parameter with a Base 64 encoded string that contains the client ID and client secret key. The field must have the format:

    Authorisation: Basic <base64 encoded client_id:client_secret>


API Reference
^^^^^^^^^^^^^
