from flask import Config


def create_resource_path(config: Config, resource: str) -> str:
    """
    Create a resource path for the API
    """
    return f"/v{config.get('API_VERSION', '0.0')}/{resource}"


def camel_case_payload(payload: dict) -> dict:
    """
    Convert a payload so that all snake_case keys are in camelCase
    """

    def camel_case(key: str) -> str:
        tokens = key.split("_")
        return tokens[0] + "".join(token.capitalize() for token in tokens[1:])

    def convert(value):
        if isinstance(value, dict):
            return camel_case_payload(value)
        if isinstance(value, list):
            return [convert(item) for item in value]
        return value

    return {camel_case(key): convert(value) for key, value in payload.items()}
