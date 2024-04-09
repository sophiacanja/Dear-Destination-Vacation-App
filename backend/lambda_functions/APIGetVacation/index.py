import pymysql
import boto3
import datetime
import json
from datetime import datetime
from backend.custom_exceptions import VacationPlannerDatabaseConnectionError, VacationPlannerAuroraDbError, VacationPlannerJsonOutputError

#Database Configuration 
# endpoint = 'vacationapp-dbcluster-instance-1.cmzd0vkepxf7.us-west-1.rds.amazonaws.com'
# username = 'admin'
# password = 'Asdiop123!'
# database_name = 'vacationAppDb'


def lambda_handler(event, context):
    try: 
        #establishing connection
        connection = get_db_connection()
        cursor = connection.cursor()
        print(f"Is the database connection open? {connection.open}")
    
        #get data from vacation table
        output = get_vacation_data(cursor)

        #format vacation data
        formatted_output = format_vacation_data(output)
        
        
    except VacationPlannerDatabaseConnectionError as e: 
        return_obj = e.get_err_obj() 

    except VacationPlannerAuroraDbError as e:
        return_obj = e.get_err_obj()

    except VacationPlannerJsonOutputError as e:
        return_obj = e.get_err_obj()

    else: 
        return_obj = {
            'statusCode' : 200, 
            'headers': {"Access-Control-Allow-Origin": "*"},
            'body' : json.dumps(formatted_output)
        }

    finally: 
        connection.commit()    
        connection.close()

    return return_obj


#helper function that gets data from vacation table or throws an error
def get_vacation_data(cursor):
    try:
        query = """SELECT * FROM Vacation"""
        cursor.execute(query)

        rows = cursor.fetchall()

            # Get column names from cursor.description
        columns = [desc[0] for desc in cursor.description]
            # Convert the result set to a list of dictionaries
        output = [dict(zip(columns, row)) for row in rows]
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
        
        
def format_vacation_data(output):
    try:
        for dictionary in output:
            date_obj = dictionary.get("DepartureDate")
            if date_obj:
                formatted_date = date_obj.strftime("%A, %B %-d, %Y")
                dictionary["DepartureDate"] = formatted_date
        
        return output
    

    except Exception as e:
        raise VacationPlannerJsonOutputError(message={e})
    

#helper function that prints data in vacation table
def print_vacation_table_data(cursor):
    query = """SELECT * FROM Vacation"""
    cursor.execute(query)
    rows = cursor.fetchall()
       
    for row in rows:
        print(row)
    
    
   