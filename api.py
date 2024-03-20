import os
import uuid
import boto3

# Initialize DynamoDB client
ddb_aws_region = os.getenv('DDB_AWS_REGION')
ddb_table_name = os.getenv('DDB_TABLE_NAME')
print("----ENV VARIABLES----")
print(f"TABLE_NAME={ddb_table_name}")
print(f"REGION={ddb_aws_region}")
ddb = boto3.resource('dynamodb', region_name=ddb_aws_region)
ddbtable = ddb.Table(ddb_table_name)

def create_case(title, description):

    # Generate a unique case ID
    case_id = str(uuid.uuid4())

    # Put the new item into the DynamoDB table
    ddbtable.put_item(Item={
        'caseid': case_id,
        'title': title,
        'description': description,
        'status': 'open'
    })

    # Return a successful response
    return case_id

def get_case(case_id):

    # Retrieve the item from the DynamoDB table
    response = ddbtable.get_item(Key={'caseid': case_id})

    if 'Item' not in response:
        return {'error': 'caseId not found'}

    # Return the item as a JSON object
    return response['Item']
