"""
JSON Schema for the GET User Account Detail by Email API response.

Endpoint : GET /api/getUserDetailByEmail?email=<email>
Response shape:
    {
        "responseCode": 200,
        "user": {
            "id": 123,
            "name": "John Doe",
            "email": "john@example.com",
            "title": "Mr",
            "birth_date": "1",
            "birth_month": "January",
            "birth_year": "1990",
            "firstname": "John",
            "lastname": "Doe",
            "company": "Acme",
            "address1": "123 Main St",
            "address2": "",
            "country": "India",
            "state": "Karnataka",
            "city": "Bengaluru",
            "zipcode": "560001",
            "mobile_number": "9876543210"
        }
    }
"""

_USER_PROPERTIES: dict = {
    "id": {"type": "integer", "description": "Unique numeric account identifier."},
    "name": {"type": "string"},
    "email": {"type": "string"},
    "title": {"type": "string"},
    "birth_day": {"type": "string"},
    "birth_month": {"type": "string"},
    "birth_year": {"type": "string"},
    "first_name": {"type": "string"},
    "last_name": {"type": "string"},
    "company": {"type": "string"},
    "address1": {"type": "string"},
    "address2": {"type": "string"},
    "country": {"type": "string"},
    "state": {"type": "string"},
    "city": {"type": "string"},
    "zipcode": {"type": "string"},
}

_USER_REQUIRED: list = [
    "id",
    "name",
    "email",
    "title",
    "birth_day",
    "birth_month",
    "birth_year",
    "first_name",
    "last_name",
    "company",
    "address1",
    "address2",
    "country",
    "state",
    "city",
    "zipcode",
]

ACCOUNT_DETAIL_SCHEMA: dict = {
    "type": "object",
    "required": ["responseCode", "user"],
    "properties": {
        "responseCode": {
            "type": "integer",
            "description": "HTTP-style response code returned by the API.",
        },
        "user": {
            "type": "object",
            "description": "Full account detail object for the requested user.",
            "properties": _USER_PROPERTIES,
            "required": _USER_REQUIRED,
        },
    },
}

# Shape returned by createAccount, updateAccount, deleteAccount, verifyLogin
SIMPLE_RESPONSE_SCHEMA: dict = {
    "type": "object",
    "required": ["responseCode", "message"],
    "properties": {
        "responseCode": {"type": "integer"},
        "message": {"type": "string"},
    },
}
