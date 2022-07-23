import * as cdk from 'aws-cdk-lib';
import { ApiStack } from '../lib/api-stack';

const app = new cdk.App();
const stackId = "numberplace-api-stack";
new ApiStack(app, stackId, {});
