
# AWS Lambda to AWS RDS without VPC

More info here:  [https://coderecipe.ai/architectures/77374273](https://coderecipe.ai/architectures/77374273)

**Problem Statement:**

In the past, in order to have lambda talking to RDS one would have to introduce a VPC in between, this is problematic because:

- VPC cold start time takes seconds!
- Complexity of setting up and maintaining a VPC is really unnecessary
- VPC is not free either!

**Solution:**

Using the [new Data API provided by AWS Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/data-api.html), an AWS Lambda can directly communicate with the RDS Instance. The Lambda is then connected to an API Gateway to allow user interface.

**Functional Requirements:**

Be able to query an RDS instance from within a AWS Lambda function without the use of VPC.

**Performance Requirements:**

Avoid performance issues caused by VPC configuration.

**Recipes built on top of this recipe:**

[How I Build a Scalable Crypto Exchange with AWS and web3.js](https://coderecipe.ai/architectures/95580531)

### Prerequisites

Make sure you have AWS access key and secrete keys setup locally, following this video [here](https://www.youtube.com/watch?v=_f0d2pLJjiA)

### Download the code locally

```  
git clone https://github.com/CodeRecipe-dev/LambdaToAuroraNoVPC 
```

### Deploy to the cloud  

```
cd LambdaToAuroraNoVPC

npm install serverless
pip install -r requirements.txt

serverless deploy --stage <stage-name> --dbUser <db-user-name>
```

#### Create DB - Must be done before using app

```
sls invoke -f AuroraCRUD -d '{"body":{"eventType":"createTable"}}' -l --stage <stage-name> --dbUser <db-user-name>
```

#### CRUD Operations

```
sls invoke -f AuroraCRUD -d '{"body":{"eventType":"saveRecord", "recordInfo": {"record_id": 1, "data": "hello"}}}' -l --stage <stage-name> --dbUser <db-user-name>
sls invoke -f AuroraCRUD -d '{"body":{"eventType":"getRecords"}}' -l --stage <stage-name> --dbUser <db-user-name>
sls invoke -f AuroraCRUD -d '{"body":{"eventType":"updateRecord", "recordInfo": {"record_id": 1, "data": "world"}}}' -l --stage <stage-name> --dbUser <db-user-name>

```