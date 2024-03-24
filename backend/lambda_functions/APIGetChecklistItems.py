import pymysql
import boto3
import json
import logging
from custom_exceptions import VacationPlannerDatabaseConnectionError, VacationPlannerMissingOrMalformedHeadersError, VacationPlannerAuroraDbError

#setting up logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    #connecting to database using secrets manager 
    try: 
        #establishing db connection
        connection = get_db_connection()
        cursor = connection.cursor()

        #checking if headers is valid 
        if  is_headers_present(event): 
            vacation_id = event['headers']['vacation_id']

        output = get_checklist_data(cursor, vacation_id)
        logger.info(output)
        
    
    except VacationPlannerDatabaseConnectionError as e: 
        return_obj = e.get_err_obj() 

    except VacationPlannerMissingOrMalformedHeadersError as e:
        return_obj = e.get_err_obj() 

    except VacationPlannerAuroraDbError as e:
        return_obj = e.get_err_obj() 
    
    else: 
        return_obj ={
            'statusCode' : 200, 
            'headers' : { "Access-Control-Allow-Origin" : "*"},
            'body' : json.dumps(output)
        }
    
    finally:
        connection.commit()    
        connection.close()

    return return_obj

def get_checklist_data(cursor, vacation_id):
    try:
        query = """SELECT * FROM Checklist where VacationId=%s"""
        cursor.execute(query, (vacation_id,))

        rows = cursor.fetchall()
        if len(rows) == 0:
            logger.info(f"No records associated with the passed in vacation id {vacation_id}")
            
        # Get column names from cursor.description
        columns = [desc[0] for desc in cursor.description]

        # Convert the result set to a list of dictionaries
        output = [dict(zip(columns, row)) for row in rows]

        logger.info(f"Returned rows from database: {output}")
        return output
    
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
def is_headers_present(event):
    try: 
        vacation_id = event['headers']['vacation_id']
        return True
    
    except Exception as e:
        raise VacationPlannerMissingOrMalformedHeadersError(message={e})
    

#helper function that prints data in checklist table
def print_vacation_table_data(cursor, vacation_id):
    query = """SELECT * FROM Checklist where VacationId=%s"""
    cursor.execute(query)
    rows = cursor.fetchall()
       
    for row in rows:
        print(row)
    
    
   