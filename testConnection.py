#! /Users/jayden/anaconda2/envs/py36/bin/python
import json
import pymysql
import datetime

with open('config.json') as json_data_file:
    data = json.load(json_data_file)


conn_params = data['mysql']

conn = pymysql.connect(
    host=conn_params['host'],
    user=conn_params['user'],
    password=conn_params['password'],
    db=conn_params['db'],
    port=conn_params['port']
)

cursor = conn.cursor()
sql = 'SELECT * FROM `leadtracker__lead` WHERE `type` = "Lead_Form";'
cursor.execute(sql)
result = cursor.fetchall()

for row in result:
    for key, value in row.items():
        print('key is %s'%key)
        print('value is %s'%value)





