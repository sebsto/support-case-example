## Support Cases Sample App

This is a simple Support Cases sample app for Serverless demos. The app is written in Python and will be used in GenAI demos.

Please note the app is not perfect and it is purposely so. The app is used to demonstrate how GenAI tools can help builders improve their code.

Deploy this app to create the DynamoDB table and required permissions.

To deploy this app run following commands:
- `sam build`
- `sam deploy --guided`

## Test Locally 

Take note of the DynamoDB table name created in the previous step and run this command to create `env.json` file. The file is used when testing locally.

```sh
DDB_AWS_REGION=eu-central-1
DDB_TABLE_NAME=GenAIAPIDemo-DynamoDBTable-1G6LBCGHO50AD
cat << EOF > env.json
{
	"CreateFunction": {
		"DDB_AWS_REGION":"$DDB_AWS_REGION",
		"DDB_TABLE_NAME":"$DDB_TABLE_NAME"
	},
	"GetFunction": {
		"DDB_AWS_REGION":"$DDB_AWS_REGION",
		"DDB_TABLE_NAME":"$DDB_TABLE_NAME"
	}
}
EOF
```

Start the Lambda function in a local docker container
- `sam local start-api --env-vars ./env.json`

Create a support case 
- `curl -v -d @events/data.json http://localhost:3000/case`

(take note of the support case created)
```sh
CASE_ID=c91fac76-f38d-44b0-9e9c-648244cea127
```

Get a support case 
- `curl -v http://localhost:3000/case/$CASE_ID`

## Tear down the infrastructure

When done playing with this infra, delete all the resources created (IAM role, DynamoDB table, and Lambda functions) with 

```sh
sam delete
```

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

