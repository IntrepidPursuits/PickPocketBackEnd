import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

"""
JSON Format:
    "token" = "auth token ",
    "displayName" = "Steve Nash"
"""

def lambda_handler(event, context):
    output = {}
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PickPocket')
    
    token = event['token']
    displayName = event['displayName']
    
    queryTable = table.scan(FilterExpression=Key('Token').eq(token))
        
    if (queryTable['Count'] == 0):
        output["response"] = "USER_DOES_NOT_EXIST"
        return output
        
    userId = queryTable['Items'][0]['UserId']

    response = table.update_item(
        Key={
            'UserId': userId
            },
        UpdateExpression="set DisplayName = :d",
    ExpressionAttributeValues={
        ':d': displayName
    },
    ReturnValues="UPDATED_NEW"
    )
    
    output = {}
    output["response"] = "success"
    return output