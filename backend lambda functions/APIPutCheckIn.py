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

#setting logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('secretsmanager')
response = client.get_secret_value(SecretId='vacationAppDb/MySQL')

print("hello from line 15")
secretDict = json.loads(response['SecretString'])
print("Secret Dict:", secretDict)
endpoint = secretDict['host']
username = secretDict['username']
password = secretDict['password']
database_name = 'vacationAppDb'

#Connection 
connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name)


def lambda_handler(event, context):
    try:
        #retrieve input data/ table data from Lambda event
        attendeeName = event['AttendeeName']
        vacationId = event['VacationId']
        message = event['Message']
        paymentType = event['PaymentType']
        paymentInfo = event['PaymentInfo']
        checkInTime = datetime.datetime.now()
        
        cursor = connection.cursor() 
        
        insert_query = (
            "INSERT INTO CheckIn (AttendeeName, VacationId, Message, PaymentType, PaymentInfo)"
            "VALUES (%s, %s, %s, %s, %s)"
        )
        
        data = (attendeeName, vacationId, message, paymentType, paymentInfo)
        
        #calls sql insert statement and inserts data into database
        cursor.execute(insert_query, data)
        
        #commits query to the database 
        connection.commit()
        
        #used for printing out contents in CheckIn table in db
        cursor.execute("select * from CheckIn")
        rows = cursor.fetchall() 
        for row in rows: 
            print (row)
            
        logger.info(f"Successfuly checked in user")
        
        connection.close()
    
    except Exception as e: 
        logger.erro(f"Error querying the database")