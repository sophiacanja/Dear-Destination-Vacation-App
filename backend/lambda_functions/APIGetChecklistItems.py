import pymysql
import boto3
import json
import logging

#setting up logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    #connecting to database using secrets manager 
    try: 
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId='vacationAppDb/MySQL')
        secretDict = json.loads(response['SecretString'])
        endpoint = secretDict['host']
        username = secretDict['username']
        password = secretDict['password']
        database_name = 'vacationAppDb'
        #establishing connection 
        connection = pymysql.connect(host=endpoint, user=username, password=password, db=database_name)
        logger.info("Successfully connected to the database!")
    
    except Exception as e:
        error_message = f"Error establishing connection with the database: {e}"
        logger.error(error_message)
        return {
            'statusCode' : 500,
            'headers' : { "Access-Control-Allow-Origin" : "*"},
            'body' : json.dumps({'error' : error_message})
        }
        
    try:
        if 'headers' in event:
            request_headers = event['headers']
            logger.info(f"Request headers: {request_headers}")
            vacation_id = request_headers.get("vacation_id")
    
            if not vacation_id:
                raise ValueError("Vacation ID not found in headers")
        else:
            raise ValueError("Headers not found in the event")
    
    except Exception as e:
        error_message = f"Error parsing through request headers: {e}"
        logger.error(error_message)
        return {
            'statusCode': 400,
            'headers': { "Access-Control-Allow-Origin": "*"},
            'body': json.dumps({'error': error_message})
        }

        
    #querying the database
    try:
        cursor = connection.cursor()
        query = """SELECT * FROM Checklist where VacationId=%s"""
        cursor.execute(query, (vacation_id,))
        rows = cursor.fetchall()
        if len(rows) == 0:
            logger.info(f"No records associated with the passed in vacation id {vacation_id}")
            return {
                'statusCode': 200,
                'headers' : { "Access-Control-Allow-Origin" : "*"},
                'body' : json.dumps(f"No records associated with the passed in vacation id {vacation_id}")
            }
        for row in rows:
            logger.info(f"Row in database: {row}")

        # Get column names from cursor.description
        columns = [desc[0] for desc in cursor.description]
        # Convert the result set to a list of dictionaries
        output = [dict(zip(columns, row)) for row in rows]
        logger.info(f"Returned rows from database: {output}")
        
        connection.commit()    
        connection.close()
        logger.info(output)
        
        return{
            'statusCode' : 200, 
            'headers' : { "Access-Control-Allow-Origin" : "*"},
            'body' : json.dumps(output)
        }
    except Exception as e: 
        error_message = f"Error querying the database {e}"
        logger.error(error_message)
        return {
            'statusCode' : 500, 
            'headers' : { "Access-Control-Allow-Origin" : "*"},
            'body': json.dumps({'error' : error_message})
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
        error_message = f"Error formatting data for output: {e}"
        logger.error(error_message)
        return {
            'statusCode' : 502,
            'headers' : { "Access-Control-Allow-Origin" : "*"},
            'body' : json.dumps({'error': error_message})
        }
    
    
   