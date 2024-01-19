import json
import boto3
import logging

# Get service resource
dynamodb = boto3.resource('dynamodb')

# Instantiate table resource object
table = dynamodb.Table('Itinerary')

#setting up logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO) 

class VacationPlannerInsertDynamoDbError(Exception):
    pass

def lambda_handler(event, context):
    try:
        vacation_id = event['VacationId']
        message = event['Message']

        # Update and get the item
        updatedItem = addMessage(vacation_id, message)  

        return {
            'statusCode': 200,
            'body': json.dumps(f"Message successfully added {str(updatedItem)}")
        }

    except VacationPlannerInsertDynamoDbError:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Error adding message into dynamo db table"})
        }


# Update and get the item after inserting data
def addMessage(vacation_id, message):
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
        raise VacationPlannerInsertDynamoDbError() 
