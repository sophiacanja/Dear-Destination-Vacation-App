import boto3
from boto3.dynamodb.conditions import Key
import json
import logging 
from backend.custom_exceptions import VacationPlannerMissingOrMalformedHeadersError, VacationPlannerDynamoDbError

#setting logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        itinerary_table = get_dynamo_db()
        logger.info(event)


        #parsing through request headers
        if is_headers_present(event):
            request_headers = event["headers"]
            vacation_id = request_headers["vacation_id"]


        #calls helper function to query the database and displays the data
        data = getDataById(vacation_id, itinerary_table)

    except VacationPlannerMissingOrMalformedHeadersError as e:
        return_obj = e.get_err_obj()

    except VacationPlannerDynamoDbError as e:
        return_obj = e.get_err_obj()

    else: 
        return_obj = {
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps(data, default=str)  # You should serialize 'data' to JSON
        }

    return return_obj

def get_dynamo_db():
    # Get the service resource.
    dynamodb = boto3.resource('dynamodb')
    # instantiate a table resource obj without actually creating a DynamoDB table (attributes of this table are lazy loaded)
    itinerary_table = dynamodb.Table('Itinerary')
    return itinerary_table
    
#helper function that checks if needed variables can be parsed from the event, else raises an error
def is_headers_present(event):
    try:
        request_headers = event["headers"]
        vacation_id = request_headers["vacation_id"]
        return True

    except Exception as e:
        raise VacationPlannerMissingOrMalformedHeadersError(message={e})
    
#helper function that queries the itinerary dynamodb table for data associated with vacation_id 
def getDataById(vacation_id, itinerary_table):
    try:
        vacation_id = int(vacation_id)
        response = itinerary_table.query(KeyConditionExpression=Key("VacationId").eq(vacation_id))
        table_data = response.get("Items",[])

        if len(table_data) == 0:
            logger.info(f"No database data for given vacation_id : {vacation_id}")
        else:
            logger.info(f"Data returned from table: {table_data}")

        return table_data
        
    except Exception as e:
        raise VacationPlannerDynamoDbError(message={e})