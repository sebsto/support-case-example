import os
import boto3
import uuid
import json


# Initialize DynamoDB client
ddb_aws_region = os.getenv('DDB_AWS_REGION', "eu-central-1")
ddb_table_name = os.getenv('DDB_TABLE_NAME', "support-cases")

ddb = boto3.resource('dynamodb', region_name=ddb_aws_region)
ddbtable = ddb.Table(ddb_table_name)


def create_case(event, context):
    # print(event)
    data = event['body']

    if 'body' not in event or 'title' not in event['body'] or 'description' not in event['body']:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'malformed request'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # Proceed with creating a case using the provided data
    data = json.loads(event['body'])
    print(data)
    if 'title' not in data or 'description' not in data:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Request body has no title or description'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # Generate a unique case ID
    caseid = str(uuid.uuid4())

    # Put the new item into the DynamoDB table
    ddbtable.put_item(Item={
        'caseid': caseid,
        'title': data['title'],
        'description': data['description'],
        'status': 'open'
    })

    # Return a successful response
    return {
        "statusCode": 200,
        "body": caseid
    }

def get_case(event, context):

    # print(event)
    # verify there is a path parameter
    if 'pathParameters' not in event or 'case_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No caseId provided'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    case_id = event['pathParameters']['case_id']

    # Retrieve the item from the DynamoDB table
    response = ddbtable.get_item(Key={'caseid': case_id})

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'caseId not found'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # Return the item as a JSON object
    return response['Item']
