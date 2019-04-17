import json
import os
import boto3
import pymysql

def create_table(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn):
    sqlStatement = 'create table records(record_id int NOT NULL, user_id int, data varchar(255), PRIMARY KEY (record_id))'
    _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement)


def create_record(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, record_info):
    sqlStatement = "INSERT INTO records(user_id, record_id, data) VALUES (1,{},'{}')".format(record_info['record_id'], pymysql.escape_string(record_info['data']))
    _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement)

def update_record(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, record_info):
    sqlStatement = 'UPDATE records SET data = '+json.dumps(record_info['data'])+' WHERE record_id = '+json.dumps(record_info['record_id'])+';'
    _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement)

def get_records(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn):
    sqlStatement = 'select * from records limit 5'
    response = _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement)
    return response['sqlStatementResults'][0]['resultFrame']['records']

def _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement):
    database_name = databaseName
    client = boto3.client('rds-data')
    response = client.execute_sql(
        awsSecretStoreArn=awsSecretStoreArn,
        dbClusterOrInstanceArn=dbClusterOrInstanceArn,
        database=databaseName,
        sqlStatements=sqlStatement
    )
    return response