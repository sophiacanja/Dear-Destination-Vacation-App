import json
import boto3
import logging

from backend.custom_exceptions import VacationPlannerDynamoDbError, VacationPlannerMissingOrMalformedHeadersError


#setting up logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO) 


def lambda_handler(event, context):
    try:
        itinerary_table = get_db_connection()
        #getting variables needed from headers 
        if is_headers_present(event): 
            vacation_id = event['VacationId']
            message = event['Message']

            # Update and get the item
            updatedItem = add_message(vacation_id, message, itinerary_table)  

    except VacationPlannerMissingOrMalformedHeadersError as e:
        return_obj = e.get_err_obj()

    except VacationPlannerDynamoDbError as e:
        return_obj = e.get_err_obj() 

    else: 
        return_obj = {
            'statusCode': 200,
            'body': json.dumps(f"Message successfully added {str(updatedItem)}")
        }

    return return_obj

def get_db_connection():
    # Get service resource
    dynamodb = boto3.resource('dynamodb')

    # Instantiate table resource object
    table = dynamodb.Table('Itinerary')
    return table

#helper method that checks if headers passed in is present and can be parsed
def is_headers_present(event):
    try: 
        vacation_id = event['VacationId']
        message = event['Message']
        return True
    
    except Exception:
        raise VacationPlannerMissingOrMalformedHeadersError()

# Update and get the item after inserting data
def add_message(vacation_id, message, table):
    try:
        table.update_item(
            Key={
                'VacationId': vacation_id
            },
            UpdateExpression='ADD Message :message',
            ExpressionAttributeValues={
                ':message': set([message])
            },
            # Get the updated item
            ReturnValues='ALL_NEW'  
        )
        
        # Retrieve and return the updated item
        updatedItem = table.get_item(Key={"VacationId": vacation_id})
        
        return updatedItem
    
    except Exception as e:
        logger.info("Error adding message into dynamo db table: {e}")
        raise VacationPlannerDynamoDbError(message= {e}) 