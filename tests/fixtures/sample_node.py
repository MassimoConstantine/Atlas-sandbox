"""Sample Atlas pipeline node configuration for testing the doc generator."""


def validate_input(data: dict, strict: bool = False) -> bool:
    """Validate incoming pipeline data against schema rules.

    Checks that all required fields are present and types match.

    Governance:
    - Tier 0 override: reject if schema mismatch
    - Log all validation attempts
    """
    return True


def transform_payload(payload: str, encoding: str) -> dict:
    """Transform raw payload string into structured pipeline format."""
    return {}


def undocumented_node(x, y):
    pass


def no_types_node(data, config):
    """Process data with the given config.

    This function has no type hints on its parameters.
    """
    return None


def _private_helper(value: str) -> str:
    """This is a private helper and should not appear in docs."""
    return value
