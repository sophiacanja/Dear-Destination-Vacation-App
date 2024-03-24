import pymysql
import boto3
import datetime
import json
from datetime import datetime

#Database Configuration 
# endpoint = 'vacationapp-dbcluster-instance-1.cmzd0vkepxf7.us-west-1.rds.amazonaws.com'
# username = 'admin'
# password = 'Asdiop123!'
# database_name = 'vacationAppDb'


def lambda_handler(event, context):
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId='vacationAppDb/MySQL')
    secretDict = json.loads(response['SecretString'])
    endpoint = secretDict['host']
    username = secretDict['username']
    password = secretDict['password']
    database_name = 'vacationAppDb'
    #Connection 
    connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name)
    try: 
        cursor = connection.cursor()
        print(f"Is the database connection open? {connection.open}")

    except Exception as e:
        return {
            'body': f"Error with cursor connection {e}"
        }
    
    try:
        query = """SELECT * FROM Vacation"""
        cursor.execute(query)
        rows = cursor.fetchall()
        if not rows:
            return {
                'statusCode': 404,
                'body' :"No records found"
            }
        for row in rows:
            print(row)

        # Get column names from cursor.description
        columns = [desc[0] for desc in cursor.description]
        # Convert the result set to a list of dictionaries
        output = [dict(zip(columns, row)) for row in rows]

        formatted_output = formatData(output)
        
        connection.commit()    
        connection.close()
        return{
            'statusCode' : 200, 
            'body' : json.dumps(formatted_output)
        }
    except Exception as e: 
        return {
            'statusCode' : 500, 
            'body': f"Error querying the database {e}"
        }
        
def formatData(output):
    try:
        for dictionary in output:
            date_obj = dictionary.get("DepartureDate")
            if date_obj:
                formatted_date = date_obj.strftime("%A, %B %-d, %Y")
                dictionary["DepartureDate"] = formatted_date
        
        return output
    except Exception as e:
        return {
            'body' : f"Error formatting data {e}"
        }
    
    
   