#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "S3 Bucket Name not supplied as argument"
    exit 0;
fi

if [ $# -eq 1 ]
  then
    echo "S3 Key not supplied as argument"
    exit 0;
fi


S3_BUCKET=$1
S3_KEY=$2

cd package
zip -r ../deployment-package.zip *
cd ..
zip -g deployment-package.zip *.py

aws s3 cp deployment-package.zip s3://${S3_BUCKET}/${S3_KEY}/

aws lambda update-function-code --function-name flex_visualizer --s3-bucket ${S3_BUCKET} --s3-key ${S3_KEY}/deployment-package.zip