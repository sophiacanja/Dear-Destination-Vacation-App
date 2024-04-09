import sys
from unittest import mock
import pytest
import json
from unittest.mock import patch, MagicMock
import datetime
sys.path.extend([".","backend/custom_exceptions", "backend/lambda_functions"])

from APIPostVacation.index import lambda_handler as api_post_vacation, is_headers_valid
from backend.custom_exceptions import VacationPlannerMissingOrMalformedHeadersError, VacationPlannerAuroraDbError, VacationPlannerDatabaseConnectionError


event = {
    "location" : "San Diego",
    "departure_date" : "2024-03-31T12:00:00Z"
}

invalid_event = {}


def test_is_headers_valid():
    response = is_headers_valid(event)
    assert response == True


def test_is_headers_invalid():
    with pytest.raises(VacationPlannerMissingOrMalformedHeadersError):
        is_headers_valid(invalid_event)


@patch('APIPostVacation.index.get_db_connection')
def test_api_post_vacation_invalid_headers_400(mock_db_connection):
    mock_db_connection.return_value = MagicMock()
    response = api_post_vacation(invalid_event, None)
    assert response.get('statusCode') == 400


@patch('APIPostVacation.index.insert_new_vacation')
@patch('APIPostVacation.index.get_db_connection')
def test_api_post_vacation_invalid_db_connection_500(mock_db_connection, mock_query):
    mock_db_connection.return_value = MagicMock()
    mock_query.side_effect = VacationPlannerAuroraDbError
    response = api_post_vacation(event, None)
    assert response.get('statusCode') == 500


@patch('APIPostVacation.index.insert_new_vacation')
@patch('APIPostVacation.index.get_db_connection')
def test_api_post_vacation_valid_200(mock_db_connection, mock_query):
    mock_db_connection.return_value = MagicMock() 
    mock_query.return_value = None
    response = api_post_vacation(event, None)
    assert response.get('statusCode') == 201
    assert json.loads(response.get('body')) == "Successfully added vacation into database"