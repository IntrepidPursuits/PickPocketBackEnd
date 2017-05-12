import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

"""
JSON Format:
    "token" = "pick pocket token",
    "firebaseToken" = "Super Long Token"
"""

def lambda_handler(event, context):
    output = {}
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PickPocket')
    
    token = event['token']
    firebaseToken = event['firebaseToken']
    
    queryTable = table.scan(FilterExpression=Key('Token').eq(token))
        
    if (queryTable['Count'] == 0):
        output["response"] = "INVALID_AUTH_TOKEN"
        return output
        
    userId = queryTable['Items'][0]['UserId']

    response = table.update_item(
        Key={
            'UserId': userId
            },
        UpdateExpression="set FirebaseToken = :t",
    ExpressionAttributeValues={
        ':t': firebaseToken
    },
    ReturnValues="UPDATED_NEW"
    )
    
    output = {}
    output["response"] = "success"
    return output