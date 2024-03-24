import pymysql
import boto3
from datetime import datetime
import json
import logging
from botocore.exceptions import ClientError
from custom_exceptions import VacationPlannerDatabaseConnectionError, VacationPlannerAuroraDbError, VacationPlannerMissingOrMalformedHeadersError

#set logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        #establishing database connection
        connection = get_db_connection() 
        cursor = connection.cursor()

        #checking if headers is valid
        if is_headers_valid(event):
            logger.info(event)
            location = event["location"]
            departure_date = event["departure_date"]
            date_object = datetime.fromisoformat(departure_date[:-1]) 
            logger.info(f"Event Departure date {departure_date}")
            logger.info(f"Converted date object {date_object}")
            data = (location, date_object)

        #add data into vacation table
        insert_new_vacation(cursor, data) 
        success_message = "Successfully added vacation into database"
        
        
    except VacationPlannerDatabaseConnectionError as e:
        return_obj = e.get_err_obj()

    except VacationPlannerMissingOrMalformedHeadersError as e:
        return_obj = e.get_err_obj()

    except VacationPlannerAuroraDbError as e:
        return_obj = e.get_err_obj()
    
    else:
        return_obj = {
            'statusCode': 201, 
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(success_message)
        }

    finally:
        connection.commit()
        connection.close() 

    return return_obj


#helper function that adds the new vacation data into vacation table
def insert_new_vacation(cursor, data):
    try:
        insert_query = """
                INSERT INTO Vacation (Location, DepartureDate)  
                VALUES (%s, %s)
            """
            
            #calls sql insert statement and inserts data into database
        cursor.execute(insert_query, data)

    except Exception as e:
        raise VacationPlannerAuroraDbError(message={e})



#helper function that esatblishes the database connection or throws an error
def get_db_connection():
    try: 
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId='vacationAppDb/MySQL')


        secretDict = json.loads(response['SecretString'])
        print("Secret Dict:", secretDict)
        endpoint = secretDict['host']
        username = secretDict['username']
        password = secretDict['password']
        database_name = 'vacationAppDb'

        #Connection 
        connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name)
        return connection
    
    except Exception as e: 
        raise VacationPlannerDatabaseConnectionError(message={e})
    

#helper function that checks if needed variables can be parsed from the event, else raises an error
def is_headers_valid(event):
    try:
        location = event["location"]
        departure_date = event["departure_date"]

        return True

    except Exception as e:
        raise VacationPlannerMissingOrMalformedHeadersError(message={e})
    

#helper function that prints data in vacation table
def print_vacation_table_data(cursor):
    query = """SELECT * FROM Vacation"""
    cursor.execute(query)
    rows = cursor.fetchall()
       
    for row in rows:
        print(row)