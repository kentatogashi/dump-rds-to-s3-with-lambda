import json
import os.path
import sys
import logging
import pymysql
import config
import csv
import boto3

# RDS
db_host = config.rds_host
db_user = config.rds_username
db_password = config.rds_password
db_name = config.rds_name

# S3
bucket_name = config.bucket_name
tmp_csv = "/tmp/output.csv"
s3_key = os.path.basename(tmp_csv)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(db_host, user=db_user, passwd=db_password, db=db_name, connect_timeout=10)
    logger.info("SUCCESS: Connected database")
except:
    logger.error("ERROR: Unexpected ERROR")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql interface suceeded")

def lambda_handler(event, context):
    with conn.cursor() as cur:
        query = "SELECT * FROM actor;" # From sakila sample database.
        cur.execute(query)
        with open(tmp_csv, "w") as outfile:
            writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
            writer.writerow([str(col[0]) for col in cur.description])
            for row in cur:
                writer.writerow(row)
    logger.info("SUCCESS: Outputed to csv file")
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.upload_file(tmp_csv, s3_key)
    logger.info("SUCCESS: Uploaded csv to s3")
    return {
        'statusCode': 200,
        'body': json.dumps('SUCCESS: Uploaded csv to s3')
    }
