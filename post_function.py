import json
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'csa-project-usertable'
    table = dynamodb.Table(table_name)
    
    try:
        # Check if required keys exist in the event
        required_keys = ['Authors', 'Publisher', 'Title', 'Year', 'id']
        for key in required_keys:
            if key not in event:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Headers': 'Content-Type',
                        'Access-Control-Allow-Origin': '*',
                        'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
                    },
                    'body': json.dumps({'error': f'Missing required key: {key}'})
                }
        
        # Retrieve values from the input event
        id_value = event['id']
        author_value = event['Authors']
        publisher_value = event['Publisher']
        title_value = event['Title']
        year_value = event['Year']
        
        # Insert item into DynamoDB table
        table.put_item(Item={
            'id': id_value,
            'Authors': author_value,
            'Publisher': publisher_value,
            'Title': title_value,
            'Year': year_value
        })
        
        # Construct success response
        response_body = {
            'message': 'Item added successfully',
            'id': id_value,
            'Authors': author_value,
            'Publisher': publisher_value,
            'Title': title_value,
            'Year': year_value
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'OPTIONS,POST,GET,PUT,DELETE'
            },
            'body': json.dumps(response_body)
        }
    
    except Exception as e:
        # Handle errors
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
