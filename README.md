# Feedback Sentiment Analysis

Attempting to do as much local development as possible to create a workflow to perform sentiment analysis on feedback.

## Project Dependencies

* Docker && Docker Compose
* aws-cli
* sam-cli

## How does it work

The lambda for the project was generated using `sam init --runtime python3.7` and the modified the names and structures.

The top level docker-compose pulls in the [localstack](https://github.com/localstack/localstack) to help develop and test the stack offline.

The idea is that the workflow this would involve a .csv file uploaded to s3 everyday containing the previous days feedback. The lambda would run the feedback
through [textblob](https://textblob.readthedocs.io/en/dev/) for simple NLP to detect sentiment. If feedback is negative it can be sorted into another bucket or just alerted on.

## Getting started

### Generating s3 bucket with localstack

Pull up localstack.

```bash
docker-compose up -d
```

Create an s3 bucket to receive the feedback.

```bash
aws --endpoint_url=http://localhost:4572 s3 mb s3://daily-feedback
```

Upload some feedback

```bash
aws --endpoint_url=http://localhost:4572 s3 cp samples/feedback_01.csv s3://daily-feedback --acl public-read
```

### Running the lambda

Build the lambda with requirements

```bash
sam build -b ./build --user-container -m ./feedback-sentiment-analysis/requirements.txt
```

```bash
sam local generate-event s3 put --bucket daily-feedback --key feedback_01.csv | sam local invoke --docker-network feedback-sentiment-analysis_sentiment -t build/template.yaml FeedBackSentimentAnalysis
```

The above command is telling sam to build our application against the container in order have textblob available to the lambda.

We are generating an example s3 put event with the information we pushed into localstack and piping that into the command to invoke the lambda.

While invoking the lambda we are telling it to invoke the particular FeedbackSentimentAnalysis function as defined in the template.yml and to attach to the running docker-network generated when starting localstack with docker-compose.
