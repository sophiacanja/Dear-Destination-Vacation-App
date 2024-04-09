import sys
import pytest
from unittest.mock import patch, MagicMock
sys.path.extend([".","backend/custom_exceptions", "backend/lambda_functions"])

from APIGetChecklistItems.index import lambda_handler as api_get_checklist
from backend.custom_exceptions import VacationPlannerDatabaseConnectionError


event = {
    "headers" : {
        "vacation_id" : "1"
    }
}

invalid_event = {
    "headers": {}
}

@patch('APIGetChecklistItems.index.get_db_connection')
def test_valid_no_data_200(mock_connection):
    mock_connection.return_value = MagicMock() 
    response = api_get_checklist(event, None)
    expected_response = {
        'body': '[]',
        'headers': {'Access-Control-Allow-Origin': '*'}, 
        'statusCode': 200
    }
    assert response == expected_response


@patch('APIGetChecklistItems.index.get_checklist_data')
@patch('APIGetChecklistItems.index.get_db_connection')
def test_valid_200(mock_connection, mock_db_response):
    mock_connection.return_value = MagicMock() 
    mock_db_response.return_value = ["shoes", "shirt", "pants"]
    response = api_get_checklist(event, None)
    expected_response = {
        'body': '["shoes", "shirt", "pants"]',
        'headers': {'Access-Control-Allow-Origin': '*'}, 
        'statusCode': 200
    }
    assert response == expected_response


@patch('APIGetChecklistItems.index.get_db_connection')
def test_invalid_missing_headers_400(mock_connection):
    mock_connection.return_value = MagicMock() 
    response = api_get_checklist(invalid_event, None)
    assert response.get('statusCode') == 400


@patch('APIGetChecklistItems.index.get_checklist_data')
@patch('APIGetChecklistItems.index.get_db_connection')
def test_invalid_db_error_500(mock_connection, mock_db_response):
    mock_connection.return_value = MagicMock() 
    mock_db_response.side_effect = VacationPlannerDatabaseConnectionError
    response = api_get_checklist(event, None)
    assert response.get('statusCode') == 500