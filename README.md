
# AWS Lambda to AWS RDS without VPC

More info here:  [https://coderecipe.ai/architectures/77374273](https://coderecipe.ai/architectures/77374273)

**Problem Statement:**

Traditionally, in order to have lambda talking to RDS one would have to introduce a VPC in between, this is problematic because:

-   VPC cold start time takes seconds!
-   Complexity of setting up and maintaining a VPC is really unnecessary
-   VPC is not free either!
    
**Solution:**

Using the  [new Data API provided by AWS Aurora (currently still in beta)](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/data-api.html), an AWS Lambda can directly communicate with the RDS Instance. The Lambda is then connected to an API Gateway to allow user interface.

**Functional Requirements:**

Be able to query an RDS instance from within a AWS Lambda function without the use of VPC.

**Performance Requirements:**

Avoid performance issues caused by VPC configuration.

**Recipes built on top of this recipe:**

[How I Build a Scalable Crypto Exchange with AWS and web3.js](https://coderecipe.ai/architectures/95580531)

**Note:**

One note about using the Data API is that the sql query being sent over is taken in as raw input and could potentially introduce SQL injection vulnerability. To avoid this, we have sanitized the inputs using mysql.escape.


**Prerequisites**

```
npm install serverless

export AWS_ACCESS_KEY_ID=<your-key-here>

export AWS_SECRET_ACCESS_KEY=<your-secret-key-here>

```

**Deploy**

```
serverless create --template-url https://github.com/CodeRecipe-dev/LambdaToAuroraNoVPC --path LambdaToAuroraNoVPC

cd LambdaToAuroraNoVPC

npm install
pip install -r requirements.txt

serverless deploy --stage sample --dbUser dbUser
```

**Create DB - Must be done before using app**

```
sls invoke -f AuroraCRUD -d '{"body":{"eventType":"createTable"}}' -l --stage sample --dbUser dbUser
```