import { Duration, RemovalPolicy, Stack, StackProps } from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigw from 'aws-cdk-lib/aws-apigateway';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import { RetentionDays } from 'aws-cdk-lib/aws-logs';

export class ApiStack extends Stack {
    constructor(scope: Construct, id: string, props: StackProps) {
        super(scope, id, props);

        // DynamoDB
        const resultDbId = "numberplace-api-results";
        const resultDb = new dynamodb.Table(this, resultDbId, {
            tableName: "results",
            billingMode: dynamodb.BillingMode.PAY_PER_REQUEST,
            partitionKey: {
                name: "question",
                type: dynamodb.AttributeType.STRING,
            },
            removalPolicy: RemovalPolicy.DESTROY,
            pointInTimeRecovery: false, // backup once a day
        });

        // Lambda 
        const lambdaId = "numberplace-lambda"
        const lambdaFunction = new lambda.Function(this, lambdaId, {
            runtime: lambda.Runtime.PYTHON_3_9,
            code: lambda.Code.fromAsset("lambda_functions"),
            handler: "index.handler",
            timeout: Duration.seconds(60),
            logRetention: RetentionDays.ONE_MONTH,
        });

        // Lambda -> DynamoDB
        resultDb.grantReadWriteData(lambdaFunction);

        // APIGateway
        const apiId = "numberplace-api";
        const restApi = new apigw.RestApi(this, apiId, {
            restApiName: 'numberplace-api',
            deployOptions: { stageName: 'v1' },
        });
        const lambdaIntegration = new apigw.LambdaIntegration(lambdaFunction);
        const apiResource = restApi.root.addResource("solve");
        apiResource.addMethod("GET", lambdaIntegration);
    }
}
