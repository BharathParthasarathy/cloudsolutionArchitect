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
        # Retrieve items from DynamoDB table
        table = dynamodb.Table(table_name)
        response = table.scan()  # Scan entire table (for larger tables, consider using pagination)
        items = response['Items']
        
        # Convert DynamoDB JSON format to regular JSON
        items = [json.loads(json.dumps(item, cls=DecimalEncoder)) for item in items]
        
        # Prepare the response
        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(items)
        }
        
        # Return the response
        return response
    
    except Exception as e:
        # Handle errors
        error_response = {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'error': str(e)})
        }
        
        # Return the error response
        return error_response
