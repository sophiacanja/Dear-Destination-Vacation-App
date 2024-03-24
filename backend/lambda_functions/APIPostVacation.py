import pymysql
import boto3
from datetime import datetime
import json
import logging
from botocore.exceptions import ClientError

#set logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        #getting database information
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId='vacationAppDb/MySQL')
        
        secretDict = json.loads(response['SecretString'])
        endpoint = secretDict['host']
        username = secretDict['username']
        password = secretDict['password']
        database_name = 'vacationAppDb'
        
        #creating db connection
        connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name)
        cursor = connection.cursor()
        
    except Exception as e:
        logger.error(f"Error with pymyql connection: {e}")
        return {
            'statusCode' : 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(f"Database connection failed")
        }
    
    try:
        # set variables from request
        logger.info(event)
        location = event["location"]
        departure_date = event["departure_date"]
        date_object = datetime.fromisoformat(departure_date[:-1]) 
        logger.info(f"Event Departure date {departure_date}")
        logger.info(f"Converted date object {date_object}")
      
    except Exception as e:
        logger.error(f"Malformed headers: {e}")
        return {
            'statusCode' : 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(f"Malformed request")
        } 
    
    try:
        insert_query = """
            INSERT INTO Vacation (Location, DepartureDate)  
            VALUES (%s, %s)
        """
        
        data = (location, date_object)
        
        #calls sql insert statement and inserts data into database
        cursor.execute(insert_query, data)
        connection.commit() 
        
        #outputing rows from database for logging
        cursor.execute("SELECT * FROM Vacation")
        rows = cursor.fetchall() 
        for row in rows: 
            logger.info(f"Rows in the database, with newly added vacation: {row}")
        
        connection.close() 
        
        return{
            'statusCode': 200, 
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps("Successfully added vacation into database")
        }
        
    except Exception as e:
        logger.error("Error thrown in try for inserting into vacation db:", str(e))
        return {
            'statusCode' : 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(f"Database query failed")
        }
