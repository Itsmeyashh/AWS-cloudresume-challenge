import json
import boto3


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('resume-challenge')

def lambda_handler(event, context):
    try:
        # To Fetch the current views count from the DynamoDB table
        response = table.get_item(Key={'id': '1'})
        
        if 'Item' in response:
            views = int(response['Item']['views'])
        else:
            views = 0  # Default value if no item exists

        # Increment the views count
        views += 1
        
        # Update the views count in DynamoDB
        table.put_item(Item={
            'id': '1',
            'views': views
        })

        # Return the updated views count and include CORS headers in the response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'  # Allow requests from any domain
            },
            'body': json.dumps({'visitor_count': views})
        }

    except Exception as e:
        print(f"Error updating DynamoDB: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps('Error fetching or updating views count')
        }
