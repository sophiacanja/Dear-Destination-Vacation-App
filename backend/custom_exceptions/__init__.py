import json 


class ReturnErrObj(): 
    """Super class that returns the payload needed from backend when errors are raised"""
    def get_err_obj(self): 
        return {
            'statusCode' : self.status_code, 
            'headers' : { "Access-Control-Allow-Origin" : "*"},
            'body': json.dumps({'error' : self.message})
        }
    
class VacationPlannerMissingOrMalformedHeadersError(Exception, ReturnErrObj):
    """Error thrown when headers received are missing or malformed"""
    def __init__(self, message=None):
        self.status_code = 400
        self.headers = { "Access-Control-Allow-Origin" : "*"}
        self.message = "VacationPlanerDynamoDbError raised. "
        if message is not None: 
            self.message += f"{message}"

    def get_err_obj(self):
        """Returns error object: statusCode, headers, body"""
        return super().get_err_obj() 

class VacationPlannerDynamoDbError(Exception, ReturnErrObj):
    """Error thrown during the execution of queries against dynamo databse. This error is purely a database error, not a logic error"""
    def __init__(self, message=None):
        self.status_code = 500 
        self.headers = { "Access-Control-Allow-Origin" : "*"}
        self.message = "VacationPlanerDynamoDbError raised. "
        if message is not None: 
            self.message += f"{message}"

    def get_err_obj(self):
        """Returns error object: statusCode, headers, body"""
        return super().get_err_obj()

class VacationPlannerAuroraDbError(Exception, ReturnErrObj):
    """Error thrown during the execution of queries against dynamo databse. This error is purely a database error, not a logic error"""
    def __init__(self, message=None):
        self.status_code = 500 
        self.headers = { "Access-Control-Allow-Origin" : "*"}
        self.message = "VacationPlanerDynamoDbError raised. "
        if message is not None: 
            self.message += f"{message}"

    def get_err_obj(self):
        """Returns error object: statusCode, headers, body"""
        return super().get_err_obj()  
    
class VacationPlannerJsonOutputError(Exception, ReturnErrObj):
    """Error thrown when there is an error forming json for output"""
    def __init__(self, message=None):
        self.status_code = 500 
        self.headers = { "Access-Control-Allow-Origin" : "*"}
        self.message = "VacationPlanerDynamoDbError raised. "
        if message is not None: 
            self.message += f"{message}"

    def get_err_obj(self):
        """Returns error object: statusCode, headers, body"""
        return super().get_err_obj() 
    
class VacationPlannerDatabaseConnectionError(Exception, ReturnErrObj):
    """Error thrown when connection to database is unsuccessful"""
    def __init__(self, message=None):
        self.status_code = 500 
        self.headers = { "Access-Control-Allow-Origin" : "*"}
        self.message = "VacationPlanerDynamoDbError raised. "
        if message is not None: 
            self.message += f"{message}"

    def get_err_obj(self):
        """Returns error object: statusCode, headers, body"""
        return super().get_err_obj() 
