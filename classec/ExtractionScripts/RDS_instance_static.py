#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime

def ToCheckForNextMarker(retrieveNextRDS):
    if 'Marker' in retrieveNextRDS:
        ToLoadDataOntoFile(retrieveNextRDS)
        withNextMarker = RDS.describe_db_instances(Marker=retrieveNextRDS['Marker'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextRDS)


def ToLoadDataOntoFile(Datatoload):
    # Initialize all the variable which will hold json values
    ListOfAllInstances = ' '
    Instance = ''
    AvailabilityZone = ''
    ListOfAllInstances = Datatoload['DBInstances']  # getting all Instance
    print'length of Instances ' + str(len(ListOfAllInstances))
    for Instance in ListOfAllInstances:
        if 'DBInstanceIdentifier' in Instance:
            DBInstanceIdentifier = str(Instance['DBInstanceIdentifier'])
        else:
            DBInstanceIdentifier = ''

        if 'DBInstanceClass' in Instance:
            DBInstanceClass = str(Instance['DBInstanceClass'])
        else:
            DBInstanceClass = ''

        if 'AvailabilityZone' in Instance:
            AvailabilityZone = str(Instance['AvailabilityZone'])
        else:
            AvailabilityZone = ''

        if 'DBName' in Instance:
            DBName = str(Instance['DBName'])
        else:
            DBName = ''
        if 'StorageType' in Instance:
            StorageType = str(Instance['StorageType'])
        else:
            StorageType = ''

        if 'InstanceCreateTime' in Instance:
            InstanceCreateTime = str((Instance['InstanceCreateTime']).date())
        else:
            InstanceCreateTime = ''
        if 'Engine' in Instance:
            Engine = str(Instance['Engine'])
        else:
            Engine = ''
        if 'MultiAZ' in Instance:
            MultiAZ = str(Instance['MultiAZ'])
        else:
            MultiAZ = ''
        if 'BackupRetentionPeriod' in Instance:
            BackupRetentionPeriod = str(Instance['BackupRetentionPeriod'])
        else:
            BackupRetentionPeriod = ''
        if 'AllocatedStorage' in Instance:
            AllocatedStorage = str(Instance['AllocatedStorage'])
        else:
            AllocatedStorage = ''
        if 'ReadReplicaDBInstanceIdentifiers' in Instance:
            RDBIIList = Instance['ReadReplicaDBInstanceIdentifiers']
            ReadReplicaDBInstanceIdentifiers = ''
            for i in range(len(RDBIIList)):
               ReadReplicaDBInstanceIdentifiers += RDBIIList[i]+','
        else:
            ReadReplicaDBInstanceIdentifiers = ''
        if 'EngineVersion' in Instance:
            EngineVersion = str(Instance['EngineVersion'])
        else:
            EngineVersion = ''

        textfile.write(DBInstanceIdentifier + '|' + DBInstanceClass + '|' +
                       StorageType + '|' + Engine + '|'+ EngineVersion + '|' +
                       DBName + '|' + MultiAZ + '|' + AllocatedStorage + '|' +
                       BackupRetentionPeriod + '|' + AvailabilityZone + '|' +
                       InstanceCreateTime + '|' + ReadReplicaDBInstanceIdentifiers +"\n")

        query = "insert into " + tbName + " values('" + DBInstanceIdentifier +\
                "','" + DBInstanceClass + "','" + StorageType + "','" + Engine +\
                "','" + EngineVersion + "','" + DBName + "','" + MultiAZ +\
                "','" + AllocatedStorage + "','" + BackupRetentionPeriod +\
                "','" + AvailabilityZone + "','" + InstanceCreateTime + "','" + \
                ReadReplicaDBInstanceIdentifiers + "')"

       
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
        dbName = 'cloud_assessment'
        tbName = 'rds_static_instance' + str(datetime.datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS ' + dbName
        cursor.execute(createDB)
        connection.set_database(dbName)
        dropQuery = 'DROP TABLE IF EXISTS ' + tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS " + tbName + "(DBInstanceIdentifier varchar(50),\
                   DBInstanceClass varchar(50),StorageType varchar(50),Engine varchar(20),\
                   EngineVersion varchar(50),DBName varchar(50),MultiAZ varchar(50),\
                   AllocatedStorage varchar(50),BackupRetentionPeriod varchar(50),\
                   AvailabilityZone varchar(50),InstanceCreateTime date,\
                   ReadReplicaDBInstanceIdentifiers varchar(50),\
                   PRIMARY KEY (DBInstanceIdentifier))"

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
        allRDSRegion = EC2Client.describe_regions()
        RDSRegion = allRDSRegion['Regions']

        textfile = open('RDSMetrics_Instance_mysqlimport_'+ str(datetime.datetime.now())+'.txt', 'a+')
        textfile.write("DBInstanceIdentifier|DBInstanceClass|StorageType|Engine|"
                       "EngineVersion|DBName|MultiAZ|AllocatedStorage|"
                       "BackupRetentionPeriod|AvailabilityZone|InstanceCreateTime"
                       "|ReadReplicaDBInstanceIdentifiers"+"\n")

        for eachRegion in RDSRegion:
            print(eachRegion['RegionName'])
            RDS = boto3.client('rds', region_name=eachRegion['RegionName'])
            DescRDS = RDS.describe_db_instances()
            ToCheckForNextMarker(DescRDS)
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
