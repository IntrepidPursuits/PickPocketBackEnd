import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

def lambda_handler(event, context):
    userId = event['user']
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('PickPocket')

    query = table.query(KeyConditionExpression=Key('UserId').eq(userId))
    answer = query['Items'][0]['Combination']
    answer = answer.split()

    guess = event['guess']
    guess = guess.split()
    result = checkAnswer(guess, answer)
    return {
        'result': result
    }
    
    
def checkAnswer(guess, answer):
        correct = 0
        close = 0
        for digit in range(0, len(answer)):
                if (guess[digit] == answer[digit]):
                        answer[digit] = "x"
                        guess[digit] = "x"
                        correct += 1
        # Check Number Close
        for digit in range(0, len(answer)):
                if (guess[digit] != "x" and guess[digit] in answer):
                        answer[answer.index(guess[digit])] = "x"
                        close += 1
        output = {}
        output["correct"] = correct
        output["close"] = close
        return output