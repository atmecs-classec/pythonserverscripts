#!/usr/bin/python
from bs4 import BeautifulSoup
import ast
import urllib
import mysql.connector
from mysql.connector import Error
from datetime import datetime
def GettingEc2Data():
    usock = urllib.urlopen("http://www.ec2instances.info/")
    html = usock.read()
    usock.close()

    name = ''
    apiname = ''
    memory = ''
    computeunits = ''
    vcpus = ''
    storage = ''
    architecture = ''
    networkperf = ''
    ebs_max_bandwidth = ''
    vpc_only = ''
    cost_ondemand_linux = ''
    cost_reserved_linux = ''
    cost_ondemand_mswin = ''
    cost_reserved_mswin = ''
    RegionList = ['ap-south-1','ap-northeast-2','ap-southeast-1','ap-southeast-2','ap-northeast-1','eu-central-1',
                  'eu-west-1','sa-east-1','us-east-1','us-east-2','us-west-1','us-west-2']

    soup = BeautifulSoup(html)
    table = soup.find("table")
    for Region in RegionList:
        for table_row in table.find_all("tr")[1:]:
            for table_data in table_row.find_all('td'):
                tble_attr = table_data.attrs
                if 'name' in tble_attr['class']: name = table_data.get_text()
                elif 'apiname' in tble_attr['class']: apiname = table_data.get_text()
                elif 'memory' in tble_attr['class']: memory = table_data.get_text()
                elif 'computeunits' in tble_attr['class']: computeunits = table_data.get_text()
                elif 'vcpus' in tble_attr['class']: vcpus = table_data.get_text()
                elif 'storage' in tble_attr['class']: storage = table_data.get_text()
                elif 'architecture' in tble_attr['class']: architecture = table_data.get_text()
                elif 'networkperf' in tble_attr['class']: networkperf = table_data.get_text()
                elif 'ebs-max-bandwidth' in tble_attr['class']: ebs_max_bandwidth = table_data.get_text()
                elif 'vpc-only' in tble_attr['class']: vpc_only = table_data.get_text()
                elif 'cost-ondemand-linux' in  tble_attr['class']:
                    if Region in ast.literal_eval(tble_attr['data-pricing']):
                        cost_ondemand_linux = (ast.literal_eval(tble_attr['data-pricing']))[Region]
                elif 'cost-reserved-linux' in tble_attr['class']:
                    if Region in ast.literal_eval(tble_attr['data-pricing']):
                        cost_reserved_linux_d = (ast.literal_eval(tble_attr['data-pricing']))[Region]
                        if 'yrTerm1Standard.allUpfront' in cost_reserved_linux_d:
                            cost_reserved_linux = cost_reserved_linux_d['yrTerm1Standard.allUpfront']
                elif 'cost-ondemand-mswin' in tble_attr['class']:
                    if Region in ast.literal_eval(tble_attr['data-pricing']):
                        cost_ondemand_mswin = (ast.literal_eval(tble_attr['data-pricing']))[Region]
                elif 'cost-reserved-mswin' in tble_attr['class']:
                    if Region in ast.literal_eval(tble_attr['data-pricing']):
                        cost_reserved_mswin_d = (ast.literal_eval(tble_attr['data-pricing']))[Region]
                        if 'yrTerm1Standard.allUpfront' in cost_reserved_mswin_d:
                            cost_reserved_mswin = cost_reserved_mswin_d['yrTerm1Standard.allUpfront']
            query = "insert into " + tbName + " values ('" + name + "','" + apiname + "','" + memory + "','" + computeunits.strip() + "','" + vcpus.strip() + "','" + " ".join(storage.split()) + "','" + architecture.strip() + "','" + networkperf.strip() + "','" + ebs_max_bandwidth.strip() + "','" + vpc_only.strip() + "','" + cost_ondemand_linux + "','" + cost_reserved_linux + "','" + cost_ondemand_mswin + "','" + cost_reserved_mswin + "','" + Region + "')"
            cursor.execute(query)

def connect():
    global connection, cursor, tbName
    try:
        connection = mysql.connector.connect(host='110.110.110.170',
                                             user='root',
                                             password='root')
        if  connection.is_connected():
            print 'Connection got established'
        cursor = connection.cursor()
        dbName = 'cloud_assessment'
        tbName = 'ec2_costing'+str(datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        connection.set_database(dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)
        createTB = "CREATE TABLE "+tbName+" (name varchar(50),apiname varchar(20),memory varchar(10)," \
                                          "computeunits varchar(10),vcpus varchar(10),storage varchar(30)," \
                                          "architecture varchar(10), networkperf varchar(20),ebs_max_bandwidth varchar(10)," \
                                          "vpc_only varchar(10), cost_ondemand_linux_hourly double, cost_reserved_linux_hourly double," \
                                          "cost_ondemand_mswin_hourly double,cost_reserved_mswin_hourly double,Region varchar(10))"
        cursor.execute(createTB)

    except Error as e:
        print(e)
        cursor.close()
        connection.close()
if __name__ == '__main__':
    connect()
    GettingEc2Data()
    connection.commit()
    cursor.close()
    connection.close()

