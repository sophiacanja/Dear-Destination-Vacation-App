import sys
from unittest import mock
import pytest
import json
from unittest.mock import patch, MagicMock
import datetime
sys.path.extend([".","backend/custom_exceptions", "backend/lambda_functions"])

from APIPutCheckin.index import lambda_handler as api_put_checkin, is_headers_present
from backend.custom_exceptions import VacationPlannerMissingOrMalformedHeadersError, VacationPlannerAuroraDbError, VacationPlannerDatabaseConnectionError

event = {
    "AttendeeName" : "Sophia",
    "VacationId" : "1",
    "Message" : "Excited to go!",
    "PaymentType" : "Venmo", 
    "PaymentInfo" : "Sophia_"
}

event_missing_headers = {
    "AttendeeName" : "Sophia",
    "VacationId" : "1",
    "Message" : "Excited to go!",
    "PaymentInfo" : "Sophia_"
}

def test_is_headers_present():
    response = is_headers_present(event)
    assert response == True


@patch('APIPutCheckin.index.get_db_connection')
def test_api_put_checkin_invalid_headers_400(mock_db_connection): 
    mock_db_connection.return_value = MagicMock()
    response = api_put_checkin(event_missing_headers, None)
    assert response.get('statusCode') == 400


@patch('APIPutCheckin.index.insert_checkin_info')
@patch('APIPutCheckin.index.get_db_connection')
def test_api_put_checkin_invalid_db_query_500(mock_db_connection, mock_query_result): 
    mock_db_connection.return_value = MagicMock()
    mock_query_result.side_effect = VacationPlannerAuroraDbError
    response = api_put_checkin(event, None)
    assert response.get('statusCode') == 500


@patch('APIPutCheckin.index.insert_checkin_info')
@patch('APIPutCheckin.index.get_db_connection')
def test_api_put_checkin_valid_200(mock_db_connection, mock_query_result): 
    mock_db_connection.return_value = MagicMock()
    mock_query_result.return_value = MagicMock()
    response = api_put_checkin(event, None)
    assert response.get('statusCode') == 201
    assert json.loads(response.get('body')) == "Successfuly checked in user"