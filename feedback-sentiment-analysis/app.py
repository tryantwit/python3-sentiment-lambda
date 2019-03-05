import json
import urllib.parse
import boto3
import csv

from textblob import TextBlob

s3 = boto3.client('s3',
                    endpoint_url='http://localstack:4572',
                    use_ssl=False,
                    aws_access_key_id='123',
                    aws_secret_access_key='abc')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf8')
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        lines = response['Body'].read().decode('utf8').splitlines(True)
        csv_reader = csv.DictReader(lines)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            feedback = TextBlob(row['feedback'])
            sentiment = feedback.sentiment
            if sentiment.polarity < 0:
                print('{} from {} was NEGATIVE!'.format(row['feedback'], row['username']))
            else:
                print('{} from {} was NEUTRAL to POSITIVE!'.format(row['feedback'], row['username']))
        print('Processed {} lines.'.format(line_count))
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
