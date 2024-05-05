import werkzeug

from backend.server.routes import create_resource_path
from tests.constants import *



class TestDataSeriesCreation:
    
    def test_series_creation_failure_no_user(
        self,
        client: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test exception when creating a data series with a non-existent user
        """
        response = client.post(
            create_resource_path(client.application.config, "data/series"),
            json={
                "title": VALID_SERIES_TITLE,
                "description": VALID_SERIES_DESCRIPTION
            },
            headers=valid_user_token_header,
        )
        assert response.status_code == 404
        assert "User does not exist" in response.json["message"]
        
    def test_series_creation_failure_bad_title(
        self, 
        client_with_user: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test exception when creating a data series with invalid input
        """
        response = client_with_user.post(
            create_resource_path(client_with_user.application.config, "data/series"),
            json={
                "description": VALID_SERIES_DESCRIPTION
            },
            headers=valid_user_token_header,
        )
        assert response.status_code == 400
        assert "Title must be non-empty" in response.json["message"]
        
    def test_series_creation_failure_already_exists(
        self,
        client_with_data_series: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test exception when creating a data series that already exists
        """
        
        response = client_with_data_series.post(
            create_resource_path(client_with_data_series.application.config, "data/series"),
            json={
                "title": VALID_SERIES_TITLE,
                "description": VALID_SERIES_DESCRIPTION
            },
            headers=valid_user_token_header,
        )
        assert response.status_code == 409
        assert "Series already exists" in response.json["message"]
        
    def test_series_creation_success(
        self, 
        client_with_user: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test successful data series creation
        """
        
        response = client_with_user.post(
            create_resource_path(client_with_user.application.config, "data/series"),
            json={
                "title": VALID_SERIES_TITLE,
                "description": VALID_SERIES_DESCRIPTION
            },
            headers=valid_user_token_header,
        )
        assert response.status_code == 201
        assert VALID_SERIES_TITLE.upper() in response.json.values()
        assert VALID_SERIES_DESCRIPTION in response.json.values()
              
class TestDataSeriesRetrieval:
    
    def test_series_retrieval_failure_no_user(
        self,
        client: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test exception when retrieving data series with a non-existent user
        """
        response = client.get(
            create_resource_path(client.application.config, "data/series"),
            headers=valid_user_token_header,
        )
        assert response.status_code == 404
        assert "User does not exist" in response.json["message"]
        
    def test_series_retrieval_success(
        self,
        client_with_data_series: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test successful data series retrieval
        """
        response = client_with_data_series.get(
            create_resource_path(client_with_data_series.application.config, "data/series"),
            headers=valid_user_token_header,
        )
        assert response.status_code == 200
        assert "owned_series" in response.json
        assert len(response.json["owned_series"]) == 1
        assert response.json["owned_series"][0]["title"] == VALID_SERIES_TITLE.upper()
        assert response.json["owned_series"][0]["description"] == VALID_SERIES_DESCRIPTION