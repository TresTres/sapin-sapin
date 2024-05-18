import werkzeug
from typing import List, Dict, Any

from backend.server.routes import create_resource_path
from tests.constants import *


class TestDataBatchCreation:

    def batch_helper(self) -> List[Dict[str, Any]]:
        return [
            {
                "label": f"{DATA_LABEL}-{d}",
                "date": DATA_DATE.strftime("%Y-%m-%d"),
                "amount": DATA_AMOUNT,
            }
            for d in range(120)
        ]

    def test_batch_creation_failure_no_series(
        self,
        client: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test exception when posting data with a non-existent series
        """
        response = client.post(
            create_resource_path(client.application.config, "data/batch"),
            json={"series_id": 1, "data": []},
            headers=valid_user_token_header,
        )
        assert response.status_code == 404
        assert "Series does not exist" in response.json["message"]

    def test_batch_creation_failure_no_data(
        self,
        client_with_data_series: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test that zero rows are created when no data input is given
        """
        response = client_with_data_series.post(
            create_resource_path(
                client_with_data_series.application.config, "data/batch"
            ),
            json={"series_id": VALID_SERIES_ID, "data": []},
            headers=valid_user_token_header,
        )
        assert response.status_code == 400
        assert "No valid data were provided" in response.json["message"]

    def test_batch_creation_failure_all_bad_data(
        self,
        client_with_data_series: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test exception when posting data with invalid input
        """
        response = client_with_data_series.post(
            create_resource_path(
                client_with_data_series.application.config, "data/batch"
            ),
            json={
                "series_id": str(VALID_SERIES_ID),
                "data": [{}, {"date": "bad date"}],
            },
            headers=valid_user_token_header,
        )
        assert response.status_code == 400
        assert "batch_errors" in response.json
        assert len(response.json["batch_errors"]) == 2
        assert "Item was empty" in response.json["batch_errors"][0]["message"]
        assert "Date" in response.json["batch_errors"][1]["message"]

    def test_batch_creation_total_success(
        self,
        client_with_data_series: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test successful data batch creation
        """
        response = client_with_data_series.post(
            create_resource_path(
                client_with_data_series.application.config, "data/batch"
            ),
            json={"series_id": VALID_SERIES_ID, "data": self.batch_helper()},
            headers=valid_user_token_header,
        )
        assert response.status_code == 201
        assert response.json["created"] == 120
        assert response.json["errors"] == []

    def test_batch_creation_partial_success(
        self,
        client_with_data_series: werkzeug.test.Client,
        valid_user_token_header: dict,
    ) -> None:
        """
        Test partial success in data batch creation, with the ability
        to identify the items with errors
        """
        response = client_with_data_series.post(
            create_resource_path(
                client_with_data_series.application.config, "data/batch"
            ),
            json={
                "series_id": VALID_SERIES_ID,
                "data": self.batch_helper()
                + [{"label": "bad data", "date": "bad date", "amount": "bad amount"}],
            },
            headers=valid_user_token_header,
        )
        assert response.status_code == 201
        assert response.json["created"] == 120
        assert len(response.json["errors"]) == 1
        assert response.json["errors"][0]["item"] == 120
