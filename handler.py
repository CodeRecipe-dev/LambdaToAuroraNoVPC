import json
import os
import boto3
from random import *
import sql

def handle_aurora_crud(event, context):
    request_body = event['body']
    event_type = request_body['eventType']
    databaseName = os.environ['DatabaseName']
    awsSecretStoreArn = os.environ['AwsSecretStoreArn']
    dbClusterOrInstanceArn = os.environ['DbClusterArn']

    if event_type == "createTable":
        sql.create_table(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn)
        return {"success": True, "message": "Created Table"}

    if event_type == "getRecords":
        records = sql.get_records(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn)
        return {"success": True, "records": records}

    if event_type == "saveRecord":
        record_info = request_body['recordInfo']
        record_info['record_id'] = randint(1,10000000)
        sql.create_record(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, record_info)
        return {"success": True, "message": "Saved Record", "record": record_info}

    if event_type == "updateRecord":
        record_info = request_body['recordInfo']
        sql.update_record(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, record_info)
        return {"success": True, "message": "Updated Record"}