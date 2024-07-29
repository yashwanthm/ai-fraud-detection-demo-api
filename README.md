## Summary
In this demo, we train and deploy a model using OpenShift AI, then integrate it into an application running on OpenShift. This showcases the complete process of how AI engineers develop, train, and deploy models, and how these models are incorporated into applications to deliver AI capabilities to end users.

## About the fraud detection model

The fraud detection model evaluates credit card transactions based on factors like distance from previous transactions, price relative to median spend, and transaction method to determine the likelihood of fraud.

## Train and Deploy the AI Model

Follow [OpenShift AI tutorial - Fraud detection example](https://docs.redhat.com/en/documentation/red_hat_openshift_ai_self-managed/2-latest/html/openshift_ai_tutorial_-_fraud_detection_example/index) to train and deploy the fraud detection model using OpenShift AI Sandbox without any local setup needed. By the end of 4.2 you will have the applicaiton up and running on OpenShift AI

## Integrate the AI Model into your application
Integrate the fraud detection AI Model into your API that tells if a transaction is fraud or not. See [app.py](https://github.com/yashwanthm/ai-fraud-detection-demo-api/blob/main/app.py) for details

