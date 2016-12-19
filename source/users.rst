Users
==========================================

.. highlight:: rst

.. role:: python(code)
    :language: python

.. role:: latex(code)
    :language: latex


========   ========  ==========================================
Field      Type      Notes
========   ========  ========================================== 
id         int       Friendly user number, unique value.
name       str       The user's full name
email      str       The user's email with a valid email patern 
password   str        
Username   str       
========   ========  ==========================================



Listing Users
----------------

::

    GET /api/v1.0/users


================  ================================================
Query Parameter   Notes
================  ================================================
limit             The number of itens to be returned
offset            The start position based on user id
fields            A list of user fields to be returned in response body
================  ================================================

**Sample Request**::

    GET /api/v1.0/users?limit2&offset=2&fields=id,username

**Sample Response**::

    200 OK
    Content-Type: application/json

::

    {
        "message": "",
        "total_count": "2", 
        "users": [
            {
                "id": 3,
                "username": "daveksp"
            },
            {
                "id": 4,
                "username": "david.pinheiro"
            }
        ],
        "uuid": "d02f453a-54f3-4347-8c8d-40be9293cb55"
    }



Getting a single User
----------------------

::

    GET /api/v1.0/users/user_id


**Sample Request**::

    GET /api/v1.0/users/1

**Sample Response**::

    200 OK
    Content-Type: application/json

::

    {
        "message": "",
        "users": [
            {
                "id": 1,
                "name": "David Pinheiro",
                "email": "daveksp@gmail.com",
                "username": "daveksp"
            }
        ],
        "uuid": "d02f453a-54f3-4347-8c8d-40be9293cb55"
    }


Create an User
----------------

Create a new user::

    POST /api/v1.0/users


========   ========  ==========================================
Field      Required  Notes
========   ========  ========================================== 
name       True      The user's full name
email      True      The user's email with a valid email patern 
password   True      The password 
Username   True      The Username 
========   ========  ==========================================



**Sample Request**::

    POST /api/v1.0/users
    Content-Type: application/json

::

    {
        "name": "John Doe",
        "email": "john@example.com",
        "username": "john.doe",
        "password": "password123"
    }


**Sample Response**::

    201 Created
    Location: http://skyone.com/flask_template/api/v1.0/users/13
    Content-Type: application/json

::

    {
        "message": "User successfully registered",
        "user": {
            "email": "john@example.com",
            "id": 13,
            "name": "John Doe",
            "username": "john.doe"
        },
        "uuid": "7aba9891-3120-42fd-aee6-d0b62d3032b9"
    }



Deleting Users
----------------

::

    DELETE /api/v1.0/users/user_id


**Sample Request**::

    DELETE /api/v1.0/users/99

**Sample Response**::

    200 OK
    Content-Type: application/json

::

    {
        "message": "User successfully removed",
        "uuid": "d02f453a-54f3-4347-8c8d-40be9293cb55"
    }

