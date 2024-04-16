import json
import boto3
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    # Create DynamoDB client
    dynamodb = boto3.resource('dynamodb')
    
    # Name of your DynamoDB table
    table_name = 'csa-project-usertable'
    
    try:
        # Retrieve ID from the event
        id_value = event.get('id')
        
        if id_value is None:
            raise ValueError("ID is missing from the query string parameters")

        # Retrieve item from DynamoDB table based on ID
        table = dynamodb.Table(table_name)
        response = table.get_item(Key={'id': int(id_value)})
        item = response.get('Item')

        if item is None:
            raise ValueError(f"Item with ID {id_value} not found")

        # Convert DynamoDB JSON format to regular JSON
        item = json.loads(json.dumps(item, cls=DecimalEncoder))
        
        # Prepare the response
        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Origin': '*',
                
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(item)
        }
        
        # Return the response
        return response
    
    except Exception as e:
        # Handle errors
        error_response = {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Origin': '*',
                
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'error': str(e)})
        }
        
        # Return the error response
        return error_response
