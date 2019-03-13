import json
import urllib.parse
import boto3
import pandas as pd
from textblob import TextBlob

s3 = boto3.client('s3',
                    endpoint_url='http://localstack:4572',
                    use_ssl=False,
                    aws_access_key_id='123',
                    aws_secret_access_key='abc')

def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else res,
        'headers': {
            'Content-Type': 'application/json'
        }
    }

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf8')
    print(key)

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        df = pd.read_csv(response['Body'])
        df['sentiment'] = df.apply(calculate_sentiment, axis=1)

        return respond(None, df.to_json(orient = "record"))
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))

def calculate_sentiment(row):
    print(row)
    return 'negative' if TextBlob(row.feedback).sentiment.polarity < 0 else 'positive'
