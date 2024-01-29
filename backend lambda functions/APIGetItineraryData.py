import boto3
from boto3.dynamodb.conditions import Key
import json
import logging 

#setting logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# instantiate a table resource obj without actually creating a DynamoDB table (attributes of this table are lazy loaded)
itinerary_table = dynamodb.Table('Itinerary')

def lambda_handler(event, context):
    try:
        logger.info(event)
        #parsing through request headers
        request_headers = event["headers"]
        vacation_id = request_headers["vacation_id"]
        logger.info(f"sucessfully parsed vacation_id {vacation_id}")
        #calls helper function to query the database and displays the data
        data = getDataById(vacation_id)
        response = {
            'statusCode': 200,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps(data, default=str)  # You should serialize 'data' to JSON
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps(f"Missing or malformed request headers: {e}")
        }
    return response
    
#helper function that queries the itinerary dynamodb table for data associated with vacation_id 
def getDataById(vacation_id):
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
        logger.error(f"Error querying dynamo db table: {e}")
        return {
            'statusCode' : 500,
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body': json.dumps(f"Error thrown in getDataById(). Error querying dynamo db table")
        }