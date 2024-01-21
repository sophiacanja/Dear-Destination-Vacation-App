import pymysql
import boto3
import datetime
import json
import logging

#Database Configuration 
# endpoint = 'vacationapp-dbcluster-instance-1.cmzd0vkepxf7.us-west-1.rds.amazonaws.com'
# username = 'admin'
# password = 'Asdiop123!'
# database_name = 'vacationAppDb'

#setting up logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
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

    except Exception as e: 
        logger.error(f"Error establishing connection to the database")
        return{
            'statusCode' : 500, 
            'body' : (f"Error establishing connection to the database: {e}")
        } 
    
    try: 
        #retrieve input data/ table data from Lambda event
        attendeeName = event['AttendeeName']
        vacationId = event['VacationId']
        checkInLocation = event['CheckInLocation']
        checkInTime = datetime.datetime.now()
        cursor = connection.cursor() 
    
    except Exception: 
        logger.error(f"Missing one or more event attributes")
        return {
            'statusCode' : 400, 
            'body' : (f"Missing one or more event attributes")
        }
        
    try:
        insert_check_in_table_query = (
            "INSERT INTO CheckIn (AttendeeName, VacationId, CheckInLocation, CheckInDateTime)"
            "VALUES (%s, %s, %s, %s)"
        )
        
        data = (attendeeName, vacationId, checkInLocation, checkInTime)
        
        #calls sql insert statement and inserts data into database
        cursor.execute(insert_check_in_table_query, data)
        
        #commits query to the database 
        connection.commit()
        
        #used for printing out contents in CheckIn table in db
        cursor.execute("select * from CheckIn")
        rows = cursor.fetchall() 
        for row in rows: 
            print (row)
        
        connection.close()
    
    except Exception as e:
        logger.erro(f"Malformed event attributes")
        return {
            'statusCode' : 406,
            'body' : (f"Malformed event attributes")
        }

