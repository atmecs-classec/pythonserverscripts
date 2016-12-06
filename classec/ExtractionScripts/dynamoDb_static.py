#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime


def ToCheckForNextTable(AllTables) :
    TableData = ''
    if 'LastEvaluatedTableName' in AllTables :
        LastEvaluatedTableName = AllTables['LastEvaluatedTableName']
        TableNames = AllTables['TableNames']
        for i in range(len(TableNames)):
            TableName = str(TableNames[i])
            TableData = DynamoDb.describe_table(TableName = TableName)
            #print TableData
            loadData(TableData)

def loadData(AllTableData):
    # Initialize all the variable which will hold json values
     print'length of table ' + str(len(AllTableData['Table']))
     table = AllTableData['Table']
     TableName = ''
     TableStatus = ''
     TableSizeBytes = ''
     TableArn = ''
     CreationDateTime = ''
     ItemCount = ''
     ProvisionedThroughput = ''
     LastIncreaseDateTime = ''
     LastDecreaseDateTime = ''
     NumberOfDecreasesToday = ''
     ReadCapacityUnits = ''
     WriteCapacityUnits = ''

     for key,value in table.iteritems():
        if 'TableName' == key:
            TableName = str(value)
            #print'table name'+value 
        
        if 'TableStatus' == key:
            TableStatus = str(value)

        if 'TableSizeBytes' == key:
            TableSizeBytes = str(value)

        if 'TableArn' == key:
            TableArn = str(value) 

        if 'CreationDateTime' == key:
            CreationDateTime = str(value)
        

        if 'ItemCount' == key:
            ItemCount = str(value)
        			
        if 'ProvisionedThroughput' == key:	   
            for i,j in value.iteritems():
                if i == 'LastIncreaseDateTime':
                     LastIncreaseDateTime = str(j)

                elif i == 'LastDecreaseDateTime': 
                     LastDecreaseDateTime = str(j)

                elif i == 'NumberOfDecreasesToday': 
                     NumberOfDecreasesToday = str(j)

                elif i == 'ReadCapacityUnits': 
                     ReadCapacityUnits = str(j)
                 
                elif i == 'WriteCapacityUnits':
                     WriteCapacityUnits = str(j)
                else :
                     print ''
                   
     textfile.write(TableName + '|' + TableStatus + '|' + TableArn + '|'+ 
                       TableSizeBytes + '|' + ItemCount + '|' + CreationDateTime + 
                       '|'+ LastIncreaseDateTime + '|' + LastDecreaseDateTime +
                       '|' + NumberOfDecreasesToday + '|' + ReadCapacityUnits + 
                       '|' + WriteCapacityUnits +"\n")

     query = "insert into " + tbName + " values('" + TableName + "','"+\
              TableStatus + "','" + TableArn + "','" + TableSizeBytes +\
              "','" + ItemCount + "','" + CreationDateTime + "','" +\
              LastIncreaseDateTime + "','" + LastDecreaseDateTime + "','" +\
              NumberOfDecreasesToday + "','" + ReadCapacityUnits + "','" +\
              WriteCapacityUnits +"')"
        
     #print query
     cursor.execute(query)


def connect():
    global connection
    global cursor
    global tbName
    try:
        connection = mysql.connector.connect(host='110.110.110.170',
                                             user='root',
                                             password='root')
        if connection.is_connected():
            print 'Connection got established'
        cursor = connection.cursor()
        DBName = 'cloud_assessment'
        tbName = 'dynamodb_static'
        createDB = 'CREATE DATABASE IF NOT EXISTS ' + DBName
        cursor.execute(createDB)
        connection.set_database(DBName)
        dropQuery = 'DROP TABLE IF EXISTS ' + tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS " + tbName + "(TableName varchar(50),\
                   TableStatus varchar(50),TableArn varchar(50),TableSizeBytes varchar(50),\
                   ItemCount varchar(50),CreationDateTime date,LastIncreaseDateTime date,\
                   LastDecreaseDateTime date,NumberOfDecreasesToday varchar(50),\
                   ReadCapacityUnits varchar(60),WriteCapacityUnits varchar(50))"

        cursor.execute(createTB)

    except Error as e:
        print(e)
        cursor.close()
        connection.close()


if __name__ == '__main__':
    global textfile
    try:
        connect()
        EC2Client = boto3.client('ec2')
        allELBRegion = EC2Client.describe_regions()
        ELBRegion = allELBRegion['Regions']

        textfile = open('Dynamodb_mysqlimport.txt', 'a+')
        textfile.write("TableName|TableStatus|TableArn|TableSizeBytes|"
                        "ItemCount|CreationDateTime|LastIncreaseDateTime|"
                        "LastDecreaseDateTime|NumberOfDecreasesToday|ReadCapacityUnits"
                        "|WriteCapacityUnits" + "\n")

        for eachRegion in ELBRegion:
            print(eachRegion['RegionName'])
            DynamoDb = boto3.client('dynamodb', region_name=eachRegion['RegionName'])
            ListOfAllTable = DynamoDb.list_tables()
            #print ListOfAllTable
            ToCheckForNextTable(ListOfAllTable)
        connection.commit()
        cursor.close()
        connection.close()
        textfile.close()
    except Exception as e:
        print 'Exception : Closing all connection '
        print e
        cursor.close()
        connection.close()
        textfile.close()
