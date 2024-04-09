import sys
from unittest import mock
import pytest
import json
from unittest.mock import patch, MagicMock
from datetime import datetime
import boto3
# from moto import mock_aws
sys.path.extend([".","backend/custom_exceptions", "backend/lambda_functions"])

from APIPostItineraryMessage.index import lambda_handler as api_post_itinerary_message, is_headers_present, add_message
from backend.custom_exceptions import VacationPlannerMissingOrMalformedHeadersError, VacationPlannerDynamoDbError, VacationPlannerDatabaseConnectionError


event = {
    "VacationId" : "2",
    "Message" : "Let's go get ramen"
}

#DB fixtures set up to mock aws dynamo db table, but cannot run tests due to moto not able to be installed
# @pytest.fixture
# def fixture_dynamodb_base():
#     with mock_aws():
#         dynamodb = boto3.resource("dynamodb")
#         table = dynamodb.create_table(
#             TableName="Itinerary",
#             KeySchema=[{"AttributeName": "identifier", "KeyType": "HASH"}],
#             AttributeDefinitions=[{"AttributeName": "identifier", "AttributeType": "S"}],
#             BillingMode="PAY_PER_REQUEST",
#         )
#         table.wait_unit_exists() 
#         yield table 


# @pytest.fixture
# def fixture_dynamodb_itinerary(fixture_dynamodb_base):
#     fixture_dynamodb_base.put_item(
#         Item={
#             "VacationId": "2",
#             "Message": "Hello world"
#         }
#     )

@patch('APIPostItineraryMessage.index.get_db_connection')
def test_is_headers_present_valid(mock_db_connection):
    mock_db_connection.return_value = MagicMock()
    response = is_headers_present(event)
    assert response == True


@patch('APIPostItineraryMessage.index.is_headers_present')
@patch('APIPostItineraryMessage.index.get_db_connection')
def test_is_headers_present_invalid(mock_db_connection, mock_headers_result):
    mock_db_connection.return_value = MagicMock() 
    mock_headers_result.side_effect = VacationPlannerMissingOrMalformedHeadersError
    response = api_post_itinerary_message(event, None)
    assert response.get('statusCode') == 400 


@patch('APIPostItineraryMessage.index.add_message')
@patch('APIPostItineraryMessage.index.get_db_connection')
def test_post_itinerary_200(mock_db_connection, mock_add_message):
    mock_db_connection.return_value = MagicMock() 
    mock_add_message.return_value = MagicMock()
    response = api_post_itinerary_message(event, None)
    response.get('statusCode') == 200


@patch('APIPostItineraryMessage.index.add_message')
@patch('APIPostItineraryMessage.index.get_db_connection')
def test_post_itinerary_500(mock_db_connection, mock_add_message):
    mock_db_connection.return_value = MagicMock() 
    mock_add_message.return_value = VacationPlannerDynamoDbError
    response = api_post_itinerary_message(event, None)
    response.get('statusCode') == 500


#cannot test test because it references moto & fixtures which cannot be downloaded currently
# @patch('APIPostItineraryMessage.index.get_db_connection')
# def test_add_message(mock_db_conenction, fixture_dynamodb_base, fixture_dynamodb_itinerary):
#     mock_db_conenction = MagicMock()
#     boto3_session = boto3.session.Session()
#     dynamodb = boto3_session.resource("dynamodb")
#     add_message(event["VacationId"], event["Message"], dynamodb)
#     response = fixture_dynamodb_base.get_item(Key={"identifier": event["VacationId"]})
#     updated_message = response.get("Item")
#     assert updated_message["VacationId"] == "2"