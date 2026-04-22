"""
Utility for JSON schema validation.

Wraps jsonschema.validate() and converts ValidationError into a clean
AssertionError with a human-readable message — so failures surface as
normal test assertion failures in pytest rather than raw library exceptions.
"""

import jsonschema


def validate(response_json: dict, schema: dict) -> None:
    """Validate response_json against a JSON schema.

    Args:
        response_json (dict): Parsed JSON body returned by the API
            (plain Python dict).
        schema (dict): JSON Schema dict (Draft 7 compatible) describing
            the expected shape.

    Raises:
        AssertionError: If response_json does not conform to schema.
            Message includes the failing field path and human-readable
            reason for pytest output.
    """
    try:
        jsonschema.validate(instance=response_json, schema=schema)
    except jsonschema.ValidationError as exc:
        field_path = (
            " -> ".join(str(segment) for segment in exc.absolute_path) or "(root)"
        )
        raise AssertionError(
            f"Schema validation failed at '{field_path}': {exc.message}"
        ) from None
