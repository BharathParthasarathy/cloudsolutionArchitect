import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'csa-project-usertable'
    table = dynamodb.Table(table_name)
    
    try:
        # Get the key value from the event payload
        key_id = event.get('id')
        
        # Check if key_id is provided
        if key_id is None:
            raise ValueError("Key 'id' is missing in the request payload")
        
        # Deleting the item with the specified key value
        table.delete_item(Key={'id': key_id})
        
        response = {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': json.dumps({'message': 'Item deleted successfully'})
        }
        return response
    except Exception as e:
        error_response = {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': json.dumps({'error': str(e)})
        }
        return error_response
