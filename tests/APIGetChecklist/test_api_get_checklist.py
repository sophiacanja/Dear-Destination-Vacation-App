import sys
import pytest
from unittest.mock import patch, MagicMock
sys.path.extend([".","backend/custom_exceptions", "backend/lambda_functions"])

from APIGetChecklist.index import lambda_handler as api_get_checklist
from backend.custom_exceptions import VacationPlannerMissingOrMalformedHeadersError


event = {
    "headers" : {
        "vacation_id" : "1"
    }
}

invalid_event = {
}

@patch('APIGetChecklist.index.get_db_connection')
def test_isTrue(mock_connection):
    mock_connection.return_value = MagicMock() 
    response = api_get_checklist(event, None)
    expected_response = {
        'body': '[]',
        'headers': {'Access-Control-Allow-Origin': '*'}, 
        'statusCode': 200
    }
    assert response == expected_response


@patch('APIGetChecklist.index.get_db_connection')
def test_True(mock_connection):
    mock_connection.return_value = MagicMock() 
    response = api_get_checklist(event, None)
    expected_response = {
        'body': 'VacationPlanerDynamoDbError raised.',
        'headers': {'Access-Control-Allow-Origin': '*'}, 
        'statusCode': 400
    }
    assert response == expected_response