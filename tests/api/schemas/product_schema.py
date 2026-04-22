"""
JSON Schema for the GET All Products List API response.

Endpoint : GET /api/productsList
Response shape:
    {
        "responseCode": 200,
        "products": [
            {
                "id": 1,
                "name": "Blue Top",
                "price": "Rs. 500",
                "brand": "Polo",
                "category": {
                    "usertype": {"usertype": "Women"},
                    "category": "Tops"
                }
            },
            ...
        ]
    }
"""

PRODUCT_LIST_SCHEMA: dict = {
    "type": "object",
    "required": ["responseCode", "products"],
    "properties": {
        "responseCode": {
            "type": "integer",
            "description": "HTTP-style response code returned by the API.",
        },
        "products": {
            "type": "array",
            "description": "List of product objects.",
            "items": {
                "type": "object",
                "required": ["id", "name", "price", "brand", "category"],
                "properties": {
                    "id": {
                        "type": "integer",
                        "description": "Unique product identifier.",
                    },
                    "name": {
                        "type": "string",
                        "description": "Display name of the product.",
                    },
                    "price": {
                        "type": "string",
                        "description": (
                            "Price string as returned by the API " "(e.g. 'Rs. 500')."
                        ),
                    },
                    "brand": {
                        "type": "string",
                        "description": "Brand name of the product.",
                    },
                    "category": {
                        "type": "object",
                        "description": "Nested category information.",
                        "required": ["usertype", "category"],
                        "properties": {
                            "usertype": {
                                "type": "object",
                                "description": (
                                    "User-type classification "
                                    "(e.g. Women, Men, Kids)."
                                ),
                            },
                            "category": {
                                "type": "string",
                                "description": "Category label (e.g. Tops, Tshirts).",
                            },
                        },
                    },
                },
            },
        },
    },
}
