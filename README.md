# dump-rds-to-s3-with-lambda

## Create package for AWS Lambda

```
$ pip3 install pymysql -t .
$ pip3 install boto3 -t .
$ zip -r upload.zip *
```
## Other setting

* Assign VPC to Lambda.
* Add s3 policy to IAM role for lambda
* Add rds policy to IAM role for lambda
* Add sns policy to IAM role for lambda
* Create VPC endpoint for s3
