#!/usr/bin/python
from bs4 import BeautifulSoup
import ast
import urllib
import mysql.connector
from mysql.connector import Error
from datetime import datetime
def GettingRdsData():
    usock = urllib.urlopen("http://www.ec2instances.info/rds/")
    html = usock.read()
    usock.close()

    Name = ''
    API_Name = ''
    Memory = ''
    Storage = ''
    Processor = ''
    vCPUs = ''
    Network_Performance = ''
    Arch = ''
    Amazon_Aurora_On_Demand_cost = ''
    Amazon_Aurora_Reserved_cost = ''
    MariaDB_On_Demand_cost = ''
    MariaDB_Reserved_cost = ''
    MySQL_On_Demand_cost = ''
    MySQL_Reserved_cost = ''
    Oracle_On_Demand_cost = ''
    Oracle_Reserved_cost = ''
    PostgreSQL_On_Demand_cost = ''
    PostgreSQL_Reserved_cost = ''
    SQL_Server_On_Demand_cost = ''
    SQL_Server_Reserved_cost = ''

    RegionList = ['ap-south-1','ap-northeast-2','ap-southeast-1','ap-southeast-2','ap-northeast-1','eu-central-1',
                  'eu-west-1','sa-east-1','us-east-1','us-east-2','us-west-1','us-west-2']

    soup = BeautifulSoup(html)
    table = soup.find("table")
    for Region in RegionList:
        for table_row in table.find_all("tr")[1:]:
            for table_data in table_row.find_all('td'):
                tble_attr = table_data.attrs
                if 'data-pricing' in tble_attr:
                    attr_pricing = ast.literal_eval(str(tble_attr['data-pricing']).replace("null","\"null\""))
                if 'name' in tble_attr['class']: Name = table_data.get_text()
                elif 'apiname' in tble_attr['class']: API_Name = table_data.get_text()
                elif 'memory' in tble_attr['class']: Memory = table_data.get_text()
                elif 'storage' in tble_attr['class']: Storage = table_data.get_text()
                elif 'processor' in tble_attr['class']: Processor = table_data.get_text()
                elif 'vcpus' in tble_attr['class']: vCPUs = table_data.get_text().strip()
                elif 'networkperf' in tble_attr['class']: Network_Performance = table_data.get_text().strip()
                elif 'architecture' in tble_attr['class']: Arch = table_data.get_text().strip()
                elif 'cost-ondemand-Amazon' in  tble_attr['class']:
                    if Region in attr_pricing:
                        Amazon_Aurora_On_Demand_cost = attr_pricing[Region] if bool(attr_pricing[Region]) else ''
                elif 'cost-reserved-Amazon' in tble_attr['class']:
                    if Region in attr_pricing:
                        cost_reserved_amazon = attr_pricing[Region]
                        if 'yrTerm1.allUpfront' in cost_reserved_amazon:
                            Amazon_Aurora_Reserved_cost = cost_reserved_amazon['yrTerm1.allUpfront'] if bool(
                                cost_reserved_amazon['yrTerm1.allUpfront']) else ''
                        elif type(cost_reserved_amazon) == float: Amazon_Aurora_Reserved_cost = cost_reserved_amazon
                elif 'cost-ondemand-MariaDB' in tble_attr['class']:
                    if Region in attr_pricing:
                        MariaDB_On_Demand_cost = attr_pricing[Region] if bool(attr_pricing[Region]) else ''
                elif 'cost-reserved-MariaDB' in tble_attr['class']:
                    if Region in attr_pricing:
                        cost_reserved_mariadb = attr_pricing[Region]
                        if 'yrTerm1.allUpfront' in cost_reserved_mariadb:
                            MariaDB_Reserved_cost = cost_reserved_mariadb['yrTerm1.allUpfront'] if bool(
                                cost_reserved_mariadb['yrTerm1.allUpfront']) else ''
                        elif type(cost_reserved_mariadb) == float: MariaDB_Reserved_cost = cost_reserved_mariadb

                elif 'cost-ondemand-MySQL' in tble_attr['class']:
                    if Region in attr_pricing:
                        MySQL_On_Demand_cost = attr_pricing[Region] if bool(attr_pricing[Region]) else ''
                elif 'cost-reserved-MySQL' in tble_attr['class']:
                    if Region in attr_pricing:
                        cost_reserved_mysql = attr_pricing[Region]
                        if 'yrTerm1.allUpfront' in cost_reserved_mysql:
                            MySQL_Reserved_cost = cost_reserved_mysql['yrTerm1.allUpfront'] if bool(
                                cost_reserved_mysql['yrTerm1.allUpfront']) else ''
                        elif type(cost_reserved_mysql) == float: MySQL_Reserved_cost = cost_reserved_mysql
                elif 'cost-ondemand-Oracle' in tble_attr['class']:
                    if Region in attr_pricing:
                        Oracle_On_Demand_cost = attr_pricing[Region] if bool(attr_pricing[Region]) else ''
                elif 'cost-reserved-Oracle' in tble_attr['class']:
                    if Region in attr_pricing:
                        cost_reserved_oracle = attr_pricing[Region]
                        if 'yrTerm1.allUpfront' in cost_reserved_oracle:
                            Oracle_Reserved_cost = cost_reserved_oracle['yrTerm1.allUpfront'] if bool(
                                cost_reserved_oracle['yrTerm1.allUpfront']) else ''
                        elif type(cost_reserved_oracle) == float:Oracle_Reserved_cost = cost_reserved_oracle
                elif 'cost-ondemand-PostgreSQL' in tble_attr['class']:
                    if Region in attr_pricing:
                        PostgreSQL_On_Demand_cost = attr_pricing[Region] if bool(attr_pricing[Region]) else ''
                elif 'cost-reserved-PostgreSQL' in tble_attr['class']:
                    if Region in attr_pricing:
                        cost_reserved_postgresql = attr_pricing[Region]
                        if 'yrTerm1.allUpfront' in cost_reserved_postgresql:
                            PostgreSQL_Reserved_cost = cost_reserved_postgresql['yrTerm1.allUpfront'] if bool(
                                cost_reserved_postgresql['yrTerm1.allUpfront']) else ''
                        elif type(cost_reserved_postgresql) == float:PostgreSQL_Reserved_cost = cost_reserved_postgresql
                elif 'cost-ondemand-SQL' in tble_attr['class']:
                    if Region in attr_pricing:
                        SQL_Server_On_Demand_cost = attr_pricing[Region] if bool(attr_pricing[Region]) else ''
                elif 'cost-reserved-SQL' in tble_attr['class']:
                    if Region in attr_pricing:
                        cost_reserved_sql = attr_pricing[Region]
                        if 'yrTerm1.allUpfront' in cost_reserved_sql:
                            SQL_Server_Reserved_cost = cost_reserved_sql['yrTerm1.allUpfront'] if bool(
                                cost_reserved_sql['yrTerm1.allUpfront']) else ''
                        elif type(cost_reserved_sql) == float:
                            SQL_Server_Reserved_cost = cost_reserved_sql

            Storage = " ".join(Storage.split())
            query = "insert into "+tbName+"(Name,API_Name,Memory,Storage,vCPUs,Network_Performance,Arch,Processor," \
                                          "Amazon_Aurora_On_Demand_cost,Amazon_Aurora_Reserved_cost,MariaDB_On_Demand_cost," \
                                          "MariaDB_Reserved_cost,MySQL_On_Demand_cost,MySQL_Reserved_cost," \
                                          "Oracle_On_Demand_cost,Oracle_Reserved_cost,PostgreSQL_On_Demand_cost," \
                                          "PostgreSQL_Reserved_cost,SQL_Server_On_Demand_cost,SQL_Server_Reserved_cost," \
                                          "Region) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = (Name,API_Name,Memory,Storage,vCPUs,Network_Performance,Arch,Processor,Amazon_Aurora_On_Demand_cost,
                    Amazon_Aurora_Reserved_cost,MariaDB_On_Demand_cost,MariaDB_Reserved_cost,
                    MySQL_On_Demand_cost,MySQL_Reserved_cost,Oracle_On_Demand_cost,Oracle_Reserved_cost,
                    PostgreSQL_On_Demand_cost,PostgreSQL_Reserved_cost,SQL_Server_On_Demand_cost,SQL_Server_Reserved_cost,
                    Region)
            cursor.execute(query, args)

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
        tbName = 'rds_costing'+str(datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        connection.set_database(dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)
        createTB = "CREATE TABLE "+tbName+" (Name varchar(30),API_Name varchar(30),Memory varchar(30)," \
                                          "Storage varchar(30),vCPUs varchar(30),Network_Performance varchar(30)," \
                                          "Arch varchar(30),Processor varchar(50),Amazon_Aurora_On_Demand_cost DOUBLE," \
                                          "Amazon_Aurora_Reserved_cost DOUBLE,MariaDB_On_Demand_cost DOUBLE," \
                                          "MariaDB_Reserved_cost DOUBLE, MySQL_On_Demand_cost DOUBLE," \
                                          "MySQL_Reserved_cost DOUBLE,Oracle_On_Demand_cost DOUBLE," \
                                          "Oracle_Reserved_cost DOUBLE, PostgreSQL_On_Demand_cost DOUBLE," \
                                          "PostgreSQL_Reserved_cost DOUBLE,SQL_Server_On_Demand_cost DOUBLE," \
                                          "SQL_Server_Reserved_cost DOUBLE,Region varchar(30))"

        cursor.execute(createTB)

    except Error as e:
        print(e)
        cursor.close()
        connection.close()
if __name__ == '__main__':
    connect()
    GettingRdsData()
    connection.commit()
    cursor.close()
    connection.close()

