#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime


def ToCheckForNextMarker(retrieveNextTable) :
    if 'LastEvaluatedTableName' in retrieveNextTable :
        ToLoadDataOntoFile(retrieveNextTable)
        withNextMarker = DynamoDb.describe_table(Marker=retrieveNextTable['LastEvaluatedTableName'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextTable)


def ToLoadDataOntoFile(Datatoload):
    # Initialize all the variable which will hold json values
    ListOfAllTable = ' '
    Table = ''
    DetailsOFTable = Datatoload['TableNames']  # getting all Table
    print'length of LoadBalancers ' + str(len(DetailsOFTable))
    for Table in DetailsOFTable:
        if 'TableName' in Table:
            TableName = str(Table['TableName'])
        else:
            TableName = ''

        if 'TableStatus' in Table:
            TableStatus = str(Table['TableStatus'])
        else:
            TableStatus = ''

        if 'TableSizeBytes' in Table:
            TableSizeBytes = str(Table['TableSizeBytes'])
        else:
            TableSizeBytes = ''
        if 'TableArn' in Table:
            TableArn = str(Table['TableArn'])
        else:
            TableArn = ''

        if 'CreationDateTime' in Table:
            CreationDateTime = str((Table['CreationDateTime']).date())
        else:
            CreationDateTime = ''
        if 'TableArnID' in Table:
            TableArnID = str(Table['TableArnID'])
        else:
            TableArnID = ''
        if 'ItemCount' in Table:
            ItemCount = str(Table['ItemCount'])
        else:
            ItemCount = ''			
			
	''' KeySchema = ''	   
        if 'KeySchema' in Table:
            zonelist = Table['KeySchema']
	    #print zonelist
            for i in range(len(zonelist)):
                KeySchema += zonelist[i]+' ,'
		print KeySchema
        else:
            KeySchema = ''
        
              
        if 'ProvisionedThroughput' in Table:
            Throughput = Table['ProvisionedThroughput']
            #print Throughput	
            for j in range(len(Throughput)):
                for key,value in Throughput[j].iteritems():
		    #print value
                     InstanceId = value		    
        else:
            ProvisionedThroughput = ''
	'''
        
        
        textfile.write(TableName + '|' + TableStatus + '|' +
                       TableArn + '|' + TableArnID + '|' +
                       TableSizeBytes + '|' + ItemCount + '|' + CreationDateTime + "\n")

        query = "insert into " + tbName + " values('" + TableName + \
                "','" + TableStatus + "','" + TableArn + "','" +\
                TableArnID + "','" + TableSizeBytes + "','" + ItemCount +\
                "','" + CreationDateTime + "')"

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
        tbName = 'dynamoDb_static'
        createDB = 'CREATE DATABASE IF NOT EXISTS ' + DBName
        cursor.execute(createDB)
        connection.set_database(DBName)
        dropQuery = 'DROP TABLE IF EXISTS ' + tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS " + tbName + "(TableName varchar(50),\
                   TableStatus varchar(50),TableArn varchar(50),\
                   TableArnID varchar(50),TableSizeBytes varchar(50),\
                   ItemCount varchar(50),CreationDateTime date,\
                   PRIMARY KEY (TableName))"

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

        textfile = open('DynamoDb_mysqlimport_' + str(datetime.datetime.now()) + '.txt', 'a+')
        textfile.write("TableName|TableStatus|TableArn|TableArnID|"
                       "TableSizeBytes|ItemCount|CreationDateTime" + "\n")

        for eachRegion in ELBRegion:
            print(eachRegion['RegionName'])
            DynamoDb = boto3.client('dynamodb', region_name=eachRegion['RegionName'])
            ListOfAllTable = DynamoDb.list_tables()
            ToCheckForNextMarker(ListOfAllTable)
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
