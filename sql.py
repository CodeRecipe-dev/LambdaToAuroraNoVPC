import json
import os
import boto3
import pymysql


def create_table(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn):
    sqlStatement = 'create table records(record_id int NOT NULL, user_id int, data varchar(255), PRIMARY KEY (record_id))'
    _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement)

def create_record(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, record_info):
    parameters = _get_record_id_data_parameters(record_info)
    sqlStatement = "INSERT INTO records(user_id, record_id, data) VALUES (1, :record_id, :data);"
    _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement, parameters)

def update_record(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, record_info):
    parameters = _get_record_id_data_parameters(record_info)
    sqlStatement = 'UPDATE records SET data = :data WHERE record_id = :record_id;'
    _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement)

def get_records(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn):
    sqlStatement = 'select * from records limit 5'
    response = _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement)
    return response['records']

def _get_record_id_data_parameters(record_info):
    record_id = {'name':'record_id', 'value':{'longValue': record_info['record_id']}}
    data = {'name':'data', 'value':{'stringValue': record_info['data']}}
    return [record_id, data]

def _send_sql_to_rds(databaseName, awsSecretStoreArn, dbClusterOrInstanceArn, sqlStatement, parameters=[]):
    database_name = databaseName
    client = boto3.client('rds-data')
    response = client.execute_statement(
        secretArn=awsSecretStoreArn,
        resourceArn=dbClusterOrInstanceArn,
        database=databaseName,
        parameters=parameters,
        sql=sqlStatement
    )
    return response