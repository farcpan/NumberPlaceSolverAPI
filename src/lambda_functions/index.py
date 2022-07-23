import json
import solver
import boto3

def handler(event, context):
    input_data = event["queryStringParameters"]["q"]

    dynamodb = boto3.resource('dynamodb')
    target_table = dynamodb.Table("results")
    get_response = target_table.get_item(Key={ "question": input_data })
    if "Item" in get_response:
        return {
            "statusCode": 200,
            "body": json.dumps({ "result": get_response["Item"]["answer"] }),
        }

    s = solver.NumberPlaceSolver(input_data)
    result = s.solve(0)
    result_string = s.get_fields_output()

    put_response = target_table.put_item(Item={ "question": input_data, "answer": result_string })

    return {
        "statusCode": 200,
        "body": json.dumps({ "result": result_string }),
    }
