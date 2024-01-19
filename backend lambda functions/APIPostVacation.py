import pymysql
import boto3
from datetime import datetime
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='vacationAppDb/MySQL')

secretDict = json.loads(response['SecretString'])
# print("Secret Dict:", secretDict)
endpoint = secretDict['host']
username = secretDict['username']
password = secretDict['password']
database_name = 'vacationAppDb'


def lambda_handler(event, context):
    try:
        connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name)
        cursor = connection.cursor()
    except Exception as e:
        logger.error(f"Error with pymyql connection: {e}")
        
    # retrieve input data/ table data from Lambda event
    request_headers = event["headers"]
    location = request_headers['location']
    departure_date = request_headers['departure_date']
    #datestring example to be passed in date_string = "01-01-2023 12:30:45"
    date_format = "%m-%d-%Y %H:%M:%S"
    date_object = datetime.strptime(departure_date, date_format)
    
    try:
        cursor = connection.cursor() 
        
        # insert_query = (
        #     "INSERT INTO Vacation (Location, DepartureDate)"
        #     "VALUES (%s, %s)"
        # )
        
        # data = (location, date_object)
        
        insert_query = ( 
            "SELECT * FROM vacationAppDb.Checklist"
        
            # "INSERT INTO Checklist (VacationId, Item)"   
            # "VALUES (%s, %s, %s)"
        )
        # data = ("1", "Surfboard")
        
        #calls sql insert statement and inserts data into database
        cursor.execute(insert_query)
        output= cursor.fetchall
        print(output)
        # rows = cursor.fetchall() 
        # for row in rows: 
        #     print(row)
        
        #commits query to the database 
        connection.commit()
        connection.close() 
        return{
            statusCode: 200, 
            # body: json.dumps("Successfully added vacation into database")
        }
        
        #used for printing out contents in CheckIn table in db
        # cursor.execute("SELECT * FROM Vacation")
        # rows = cursor.fetchall() 
        # for row in rows: 
        #     print(row)
            
    except Exception as e:
        print("Error:", str(e))
