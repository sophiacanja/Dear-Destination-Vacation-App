import sys
from unittest import mock
import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime
sys.path.extend([".","backend/custom_exceptions", "backend/lambda_functions"])

from APIGetVacation.index import lambda_handler as api_get_vacation, format_vacation_data
from backend.custom_exceptions import VacationPlannerJsonOutputError, VacationPlannerAuroraDbError, VacationPlannerDatabaseConnectionError



@patch('APIGetVacation.index.format_vacation_data')
@patch('APIGetVacation.index.get_vacation_data')
@patch('APIGetVacation.index.get_db_connection')
def test_get_vacation_valid_200(mock_db_connection, mock_query_result, mock_format):
    mock_db_connection = MagicMock()
    mock_query_result.return_value = [{"VacationId": "1", "DepartureDate": "2024-04-05 02:29:09.681487"}]
    mock_format.return_value = [{"VacationId": "1", "DepartureDate": "Thursday, April 4, 2024"}]

    response = api_get_vacation(None, None)
    assert response.get('statusCode') == 200
    

#format_vacation_data does not like the use of .strftime, so I cannot test properly
def test_format_vacation_data_invalid():
    data = [{"VacationId": "1", "DepartureDate": "2024-04-05 02:29:09.681487" }]
    with pytest.raises(VacationPlannerJsonOutputError):
        response = format_vacation_data(data)


@patch('APIGetVacation.index.get_vacation_data')
@patch('APIGetVacation.index.get_db_connection')
def test_db_query_error_500(mock_db_connection, mock_db_call):
    mock_db_connection.side_effect = MagicMock()
    mock_db_call.side_effect = VacationPlannerAuroraDbError
    response = api_get_vacation(None,None)
    assert response.get('statusCode') == 500