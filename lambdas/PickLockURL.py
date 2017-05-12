import json
import boto3
import decimal
from boto3.dynamodb.conditions import Key, Attr

"""
JSON Format:
    "userId" = "JohnM",
    "displayName" = "John Mack",
    "combination" = "[1 2 3 4]"
"""
validDigits = [1, 2, 3, 4, 5, 6]

def lambda_handler(event, context):
    output = {}
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PickPocket')
    
    userId = event['userId']
    combination = event['combination']
    
    queryTable = table.query(KeyConditionExpression=Key('UserId').eq(userId))
    
    if (queryTable['Count'] != 0):
        output["response"] = "USER_EXISTS"
        return output
        
    if (not validateCombination(combination)):
        output["response"] = "INVALID_COMBINATION_FORMAT"
        return output
    
    if 'displayName' in event:
        displayName = event['displayName']
    else:
        displayName = userId
    
    response = table.put_item(
       Item={
            'UserId': userId,
            'DisplayName': displayName,
            'Combination': combination,
        }
    )
    
    output = {}
    output["response"] = "success"
    return output
    
def validateCombination(combinationString):
    try:
        combinationParse = combinationString.split()
        for digit in combinationParse:
            if int(digit) not in validDigits:
                print digit
                return False
        return True
    except error:
        return False