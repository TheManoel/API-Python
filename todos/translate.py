import os
import json
import traceback

from todos import decimalencoder
import boto3
dynamodb = boto3.resource('dynamodb')
awstranslate = boto3.client('translate', region_name='us-east-1')


def translate(event, context):
    table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

    # fetch todo from the database
    result = table.get_item(
        Key={
            'id': event['pathParameters']['id']
        }
    )

    translatedText = awstranslate.translate_text(Text=result['Item']['text'],
                                  SourceLanguageCode="auto",
                                  TargetLanguageCode=event['pathParameters']['lang'])
                                  
    result['Item']['text'] = translatedText['TranslatedText']
    
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'],
                           cls=decimalencoder.DecimalEncoder)
    }

    return response