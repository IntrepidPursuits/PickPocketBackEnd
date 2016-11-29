import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PickPocket')

    query = table.scan(AttributesToGet=[
        'UserId',
    ])

    query = query['Items']
    
    return {
        'result': query
    }