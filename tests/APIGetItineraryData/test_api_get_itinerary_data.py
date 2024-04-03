import sys
from unittest import mock
import pytest
import json
from unittest.mock import patch, MagicMock
sys.path.extend([".","backend/custom_exceptions", "backend/lambda_functions"])

from APIGetItineraryData.index import lambda_handler as api_get_itinerary 
from backend.custom_exceptions import VacationPlannerDynamoDbError

invalid_event = {
    "headers" : {}
}

event = {
    "headers" : {
        "vacation_id" : "2"
    }
}

@patch('APIGetItineraryData.index.get_dynamo_db')
def test_headers_invalid_400(mock_dynamo):
    mock_dynamo.return_value = MagicMock()
    response = api_get_itinerary(invalid_event, None)
    assert response.get('statusCode') == 400


@patch('APIGetItineraryData.index.getDataById')
@patch('APIGetItineraryData.index.get_dynamo_db')
def test_db_error_500(mock_dynamo, mock_itinerary_data):
    mock_dynamo.return_value = MagicMock()
    mock_itinerary_data.side_effect = VacationPlannerDynamoDbError
    response = api_get_itinerary(event, None)
    assert response.get('statusCode') == 500


@patch('APIGetItineraryData.index.getDataById')
@patch('APIGetItineraryData.index.get_dynamo_db')
def test_headers_valid_200(mock_dynamo, mock_itinerary_data):
    mock_dynamo.return_value = MagicMock()
    mock_itinerary_data.return_value = ["toothbrush, towel"]
    response = api_get_itinerary(event, None)
    assert response.get('statusCode') == 200 
    assert response.get('body') == '["toothbrush, towel"]'


@patch('APIGetItineraryData.index.getDataById')
@patch('APIGetItineraryData.index.get_dynamo_db')
def test_no_data_200(mock_dynamo, mock_itinerary_data):
    mock_dynamo.return_value = MagicMock()
    mock_itinerary_data.return_value = []
    response = api_get_itinerary(event, None)
    assert response.get('statusCode') == 200 
    assert response.get('body') == '[]'