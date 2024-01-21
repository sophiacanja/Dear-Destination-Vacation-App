import boto3
import json

# Get the service resource.
dynamodb = boto3.resource('dynamodb')
# instantiate a table resource obj without actually creating a DynamoDB table (attributes of this table are lazy loaded)
table = dynamodb.Table('Itinerary')

def lambda_handler(event, context):
    try:
        data = getData()
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

def getData():
    response = table.scan()
    data = response['Items']
    # print(data)

    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    return data
