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
table = dynamodb.Table('Itinerary')

def lambda_handler(event, context):
    try:
        request_body = event["body"]
        vacation_id = request_body["vacation_id"]
        logger.info(f"sucessfully parsed vacation_id")
        data = getDataById(vacation_id)
        response = {
            'statusCode': 200,
            'body': json.dumps(data, default=str)  # You should serialize 'data' to JSON
        }
    except Exception as e:
        response = {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
    return response
    
def getDataById(vacation_id):
    try:
        vacation_id = int(vacation_id)
        response = table.query(KeyConditionExpression=Key("VacationId").eq(vacation_id))
        table_data = response.get("Items",[])
        logger.info(f"Data returned from table: {table_data}")
        return table_data
        
    except Exception as e:
        logger.error(f"Error querying dynamo db table")
        return {
            'statusCode' : 500,
            'body': json.dumps(f"Error querying dynamo db table")
        }
    
