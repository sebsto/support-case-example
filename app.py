import json
import base64
import api

def create_case(event, context):
    print(event)
    data = event['body']

    if 'body' not in event:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'malformed request'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # decode the body from base64 to string 


    # Proceed with creating a case using the provided data
    try :
        data = json.loads(event['body'])
    except ValueError:        
        # Maybe the payload is base64 encoded
        print("Base64 decode the payload")
        data = json.loads(base64.b64decode(event['body']))
    print(data)
    
    if 'title' not in data or 'description' not in data:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Request body has no title or description'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # Create the case ID
    try:
        case_id = api.create_case(data['title'], data['description'])
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'}),
            'headers': {'Content-Type': 'application/json'}
        }

    # Return a successful response
    return {
        "statusCode": 200,
        "body": case_id
    }

def get_case(event, context):
    print(event)

    # verify there is a path parameter
    if 'pathParameters' not in event or 'case_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'No caseId provided'}),
            'headers': {'Content-Type': 'application/json'}
        }
    
    case_id = event['pathParameters']['case_id']

    # Retrieve the item from the DynamoDB table
    try:
        response = api.get_case(case_id)
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal server error'}),
            'headers': {'Content-Type': 'application/json'}
        }

    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps(response),
            'headers': {'Content-Type': 'application/json'}
        }

    # Return the item as a JSON object
    return response['Item']