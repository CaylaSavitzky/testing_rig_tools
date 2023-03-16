# Flex Visualizer AWS Lambda Script

## Configuration

### S3 Configuration
Create an S3 bucket that will store your Lambda script

### Lambda Configuration
Create a new lambda function that points to the previously created S3 bucket

### ENV Configuration
This script relies on environment variables to configure the scripts. The accepted environment variables are listed below:


| Environment Variable  | Description                                                      | Required | Default Value                 | Example Value                 |
|-----------------------|------------------------------------------------------------------|----------|-------------------------------|-------------------------------|
| AWS_ACCESS_KEY_ID     | AWS Access Key ID for account that can publish to Cloudwatch     | yes      |                               | ADJADJA27271273               |
| AWS_SECRET_ACCESS_KEY | AWS Secret Access Key for account that can publish to Cloudwatch | yes      |                               | 7asdf7asdhjfJDAHDHJ22         |
| AWS_DEFAULT_REGION    | AWS region info                                                  | yes      |                               | us-east-1                     |
| GTFS_DIRECTORY        | Where gtfs files are stored locally                              | yes      | /tmp/gtfs                     | /tmp/gtfs                     |
| OUTPUT_FILE           | Where visualizer html output file is stored                      | no       | /tmp/gtfs/output.html         | /tmp/gtfs/output.html         |
| S3_OUTPUT_BUCKET      | Name of s3 bucket where html output is uploaded to               | yes      |                               | my-s3-flex-output             |
| S3_OUTPUT_PATH        | Path of output file in the OUTPUT s3 bucket                      | no       | index.html                    | index.html                    |
| S3_ARCHIVE_PATH       | Path of archive output file in the OUTPUT s3 bucket              | no       | archive/index-yyyy-mm-dd.html | archive/index-2023-01-01.html |
| S3_GTFS_BUCKET        | Name of s3 bucket where gtfs files will be pulled from           | yes      |                               | my-s3-gtfs-bucket             |
| S3_GTFS_FILE_PATH     | Path of input files in the GTFS s3 bucket                        | no       | v2qa/input                    | prod/input                    |
| HIDE_LEGEND           | Whether or not to show legend on map                             | no       | False                         | True                          |

## Lambda Deployment
### Prerequisite
* Lambda function pointing to S3 bucket
* AWS CLI tool

### Deploying the script to AWS Lambda
Make sure to replace `my-s3-lambda-bucket` and `path/to/deployment` with your own values
```
./lambda_pre_deploy.sh # this packages up any python dependencies
./lambda_deploy.sh my-s3-lambda-bucket path/to/deployment # deploys lambda function by uploading it to s3 first
```
