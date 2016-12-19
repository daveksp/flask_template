Overview
==========================================

.. highlight:: rst

.. role:: python(code)
    :language: python

.. role:: latex(code)
    :language: latex


Requests
------------

The base url of the API is ``http://skyone.com/flask_template/api/version`` where ``version`` should be replaced by the desired API version.


JSON Bodies
------------

All POST, PUT, PATCH requests are JSON encoded and must have content type of ``application/json``.


HTTP Verbs
------------

- ``GET`` - To retrieve a resource or a collection of resources
- ``POST`` - To create a resource
- ``PATCH`` - To modify a resource
- ``PUT`` - To set a resource
- ``DELETE`` - To delete a resource



HTTP Status Codes
-------------------

Success Codes:

- ``200 OK`` - Request succeeded. Response included
- ``201 Created`` - Resource created. URL to new resource in Location header
- ``204 No Content`` - Request succeeded, but no response body


Error Codes:

- ``400 Bad Request`` - Could not parse request
- ``401 Unauthorized`` - No authentication credentials provided or authentication failed
- ``403 Forbiden`` - Authenticated user does not have access
- ``404 Not Found`` - Resource not found
- ``415 Unsupported Media Type`` - POST/PUT/PATCH request occurred without a application/json content type
- ``500, 501, 502, 503, etc`` - An internal server error occured


Response Messages
------------------

Most of flask_template API responses will return two special fields in it's body:

========   ====================================================================
Field      Notes
========   ==================================================================== 
message    Additional information such as an exception message
uuid       The request's uuid in case you want to perform some kind of tracking 
========   ====================================================================


Errors
------------

All 400 series errors and most of 500 series errors will return a JSON object in the body and an ``applications/json`` content type::

    {
        "message": "Not Found"
    }


Validation Errors
------------------

In case of validation errors on a POST/PUT/PATCH request, a 400 status code will be returned. The JSON response body will include all validation errors in an attribute message::

    {
        "message": {
            "password": "field password is required",
            "username": "field username is required"
        }
    }


Field Filtering
------------------

You can choose which fields to retrieve from an API call. Just pass in a fields query parameter with a comma separated list of fields you need. E.g::

    GET /api/v1.0/users?fields=id,username


The following response body will be returned::

    {
        "message": "",
        "total_count": "2", 
        "users": [
            {
                "id": 1,
                "username": "daveksp"
            },
            {
                "id": 2,
                "username": "david.pinheiro"
            }
        ],
        "uuid": "d02f453a-54f3-4347-8c8d-40be9293cb55"
    }


Limit and Offset
------------------

You can limit your searchs by limit and/or offset parameters, e.g::

    GET /api/v1.0/users?limit=2&offset=4


The following response body will be returned::

    {
        "message": "",
        "total_count": 2,
        "users": [
            {
                "email": "david_pinheiro@skyone.com",
                "id": 5,
                "name": "david",
                "username": "david.pinheiro"
            },
            {
                "email": "daveksp@skyone.com",
                "id": 6,
                "name": "david",
                "username": "daveksp"
            }
        ],
        "uuid": "d02f453a-54f3-4347-8c8d-40be9293cb55"
    }