import pymysql
import boto3
import datetime
import json
import logging 
from backend.custom_exceptions import VacationPlannerDatabaseConnectionError, VacationPlannerMissingOrMalformedHeadersError, VacationPlannerAuroraDbError


#setting logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    try:
        #connect to database
        connection = get_db_connection() 
        cursor = connection.cursor() 

        #retrieve input data/ table data from Lambda event
        if is_headers_present(event): 
            attendeeName = event['AttendeeName']
            vacationId = event['VacationId']
            message = event['Message']
            paymentType = event['PaymentType']
            paymentInfo = event['PaymentInfo']
            checkInTime = datetime.datetime.now()
            checkin_data = (attendeeName, vacationId, message, paymentType, paymentInfo)

        #insert data into table
        insert_checkin_info(cursor, checkin_data)
        success_message = "Successfuly checked in user"
        logger.info(success_message)
        
    
    except VacationPlannerMissingOrMalformedHeadersError as e: 
        return_obj = e.get_err_obj()

    except VacationPlannerDatabaseConnectionError as e:
        return_obj = e.get_err_obj()

    except VacationPlannerAuroraDbError as e:
        return_obj = e.get_err_obj() 

    else: 
        return_obj = {
            'statusCode' : 201, 
            'headers' : { "Access-Control-Allow-Origin" : "*"},
            'body': json.dumps(success_message)
        }

    finally: 
        #commits query to the database 
        connection.commit()
        connection.close()

    return return_obj


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
def is_headers_present(event):
    try: 
        attendeeName = event['AttendeeName']
        vacationId = event['VacationId']
        message = event['Message']
        paymentType = event['PaymentType']
        paymentInfo = event['PaymentInfo']

        return True
    
    except Exception as e:
        raise VacationPlannerMissingOrMalformedHeadersError(message={e})
    
#helper function that inserts data into checkin table or raises an error
def insert_checkin_info(cursor, checkin_data):
    try:
        insert_query = (
                "INSERT INTO CheckIn (AttendeeName, VacationId, Message, PaymentType, PaymentInfo)"
                "VALUES (%s, %s, %s, %s, %s)"
            )
            
        #calls sql insert statement and inserts data into database
        cursor.execute(insert_query, checkin_data)
    
    except Exception as e:
        raise VacationPlannerDatabaseConnectionError(message={e})
    

#helper function used for printing out contents in CheckIn table in db
def print_checkin_table_rows(cursor):
    cursor.execute("select * from CheckIn")
    rows = cursor.fetchall() 
    for row in rows: 
        print (row)
    


