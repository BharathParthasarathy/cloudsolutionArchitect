import json
import boto3
from boto3.dynamodb.conditions import Key

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table_name = 'csa-project-usertable'
    table = dynamodb.Table(table_name)
    
    try:
        # Ensure that 'id' is present in the event object
        if 'id' not in event:
            raise ValueError("ID is missing from the request")

        # Extract the ID from the event
        id_value = int(event['id'])
        
        # Check if the item with the specified ID exists
        response = table.query(
            KeyConditionExpression=Key('id').eq(id_value)
        )
        items = response.get('Items')
        if not items:
            raise ValueError(f"Item with ID {id_value} not found")

        # Extract other attributes to update
        authors = event.get('Authors')
        publisher = event.get('Publisher')
        title = event.get('Title')
        year = event.get('Year')

        # Construct the update expression and attribute values
        update_expression = "SET "
        expression_attribute_values = {}
        expression_attribute_names = {}
        if authors is not None:
            update_expression += "#a = :a, "
            expression_attribute_values[':a'] = authors
            expression_attribute_names['#a'] = "Authors"
        if publisher is not None:
            update_expression += "#p = :p, "
            expression_attribute_values[':p'] = publisher
            expression_attribute_names['#p'] = "Publisher"
        if title is not None:
            update_expression += "#t = :t, "
            expression_attribute_values[':t'] = title
            expression_attribute_names['#t'] = "Title"
        if year is not None:
            update_expression += "#y = :y, "
            expression_attribute_values[':y'] = year
            expression_attribute_names['#y'] = "Year"

        # Remove the trailing comma and space
        update_expression = update_expression.rstrip(', ')

        # Update item in DynamoDB table
        response = table.update_item(
            Key={'id': id_value},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ExpressionAttributeNames=expression_attribute_names,
            ReturnValues="UPDATED_NEW"
        )
        
        # Construct response
        response_body = {
            'message': 'Item updated successfully'
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
