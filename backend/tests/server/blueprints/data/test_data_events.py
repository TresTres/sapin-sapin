import werkzeug

from backend.server.routes import create_resource_path
from tests.constants import *



class TestDataSeriesCreation:

    
    def test_series_creation_failure_no_series(
        self,
        client: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test exception when posting data with a non-existent series 
        """
        response = client.post(
            create_resource_path(client.application.config, "data/batch"),
            json={
                "series": 1,
                "data": []
            },
            headers=valid_user_token_header,
        )
        assert response.status_code == 404
        assert "Series does not exist" in response.json["message"]