import json
import boto3
import decimal
import uuid
from boto3.dynamodb.conditions import Key, Attr

"""
JSON Format:
    "userId" = "JohnM",
    "combination" = "[1 2 3 4]"
"""
validDigits = [1, 2, 3, 4, 5, 6]

def lambda_handler(event, context):
    output = {}
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PickPocketProd')

    userId = event['userId']
    combination = event['combination']

    combination = json.loads(combination)

    queryTable = table.query(KeyConditionExpression=Key('UserId').eq(userId))

    if (queryTable['Count'] != 0):
        output["response"] = "USER_EXISTS"
        return output

    if (not validateCombination(combination)):
        output["response"] = "INVALID_COMBINATION_FORMAT"
        return output

    combinationLength = len(combination)

    token = str(uuid.uuid1())

    response = table.put_item(
       Item={
            'UserId': userId,
            'Combination': combination,
            'CombinationLength': combinationLength,
            'Token': token
        }
    )

    output = {}
    output["response"] = token
    return output

def validateCombination(combination):
    try:
        for digit in combination:
            if int(digit) not in validDigits:
                print digit
                return False
        return True
    except:
        return False
