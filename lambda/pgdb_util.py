'''
Created on October 18, 2018
Updated on
Authored by Kunal Ghosh
Purpose is to connect to postgres RDS from Lambda
On 10/18/2018 created the first version
'''

import psycopg2

db_host = 'kunal-pg-aws-sentiment.cuqb2rlrkpmp.us-east-1.rds.amazonaws.com'
db_port = 5432
db_name = 'kunalawssentiment'
db_user = 'kunal'
db_pass = 'kunalghosh'

def make_conn():
    conn = None
    try:
        conn = psycopg2.connect("dbname='%s' user='%s' host='%s' password='%s' port='%d'" % (db_name, db_user, db_host, db_pass, db_port))
        conn.autocommit = True
    except:
        print('Cannot Connect to database')
    return conn

def fetch_data(conn, query):
    result = []
    print('Now executing :{}'.format(query))
    cursor = conn.cursor()
    cursor.execute(query)

    row = cursor.fetchall()
    for line in row:
        result.append(line)
    return result

def execute_query(conn, query):
    print('Now executing :{}'.format(query))
    cursor = conn.cursor()
    cursor.execute(query)
