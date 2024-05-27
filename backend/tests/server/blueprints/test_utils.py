from backend.server.blueprints.utils import *


class TestCreateResourcePath:
    def test_create_resource_path(self):
        fake_config = {"API_VERSION": "test"}
        assert create_resource_path(fake_config, "foo") == "/vtest/foo"



class TestCamelCasePayload:
    def test_camel_case_payload(self):
        payload = {
            "snake_case_key": "value",
            "key": "value",
        }
        assert camel_case_payload(payload) == {
            "snakeCaseKey": "value",
            "key": "value",
        }
        
    def test_camel_case_payload_nested(self):
        payload = {
            "snake_case_key": {
                "snake_case_key": "value",
            },
            "key": {
                "snake_case_key": "value",
            },
        }
        assert camel_case_payload(payload) == {
            "snakeCaseKey": {
                "snakeCaseKey": "value",
            },
            "key": {
                "snakeCaseKey": "value",
            },
        }
        
    def test_camel_case_payload_list(self):
        payload = {
            "snake_case_key": ["snake_case_string", "key", {
                "snake_case_key": "value",   
            }],
            "key": ["snake_case_string", "key", {
                "snake_case_key": "value",   
            }],
        }
        assert camel_case_payload(payload) == {
            "snakeCaseKey": ["snake_case_string", "key", {
                "snakeCaseKey": "value",   
            }],
            "key": ["snake_case_string", "key", {
                "snakeCaseKey": "value",   
            }],
        }