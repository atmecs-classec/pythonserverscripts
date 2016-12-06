#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime


def ToCheckForNextMarker(retrieveNextRDS):
    if 'Marker' in retrieveNextRDS:
        ToLoadDataOntoFile(retrieveNextRDS)
        withNextMarker = RDS.describe_db_clusters(Marker = retrieveNextRDS['Marker'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextRDS)

def ToLoadDataOntoFile(Datatoload):
    #Initialize all the variable which will hold json values
    ListOfAllClust = ' '
    Clust = ''
    AvailabilityZones = ''
    ListOfAllClust = Datatoload['DBClusters']  # getting all Clustumes
    print'length of cluster '+ str(len(ListOfAllClust))
    for Clust in ListOfAllClust:
       if 'MasterUsername' in Clust:
           masterUsername = str(Clust['MasterUsername'])
       else :
           masterUsername = ''
       
       if'VpcSecurityGroups' in Clust:
           for VpcSecurityGroups in Clust['VpcSecurityGroups'] :
               VpcSecurityGroups_Status = str(VpcSecurityGroups['Status'])
               VpcSecurityGroupId =str(VpcSecurityGroups['VpcSecurityGroupId'])
       else:
           VpcSecurityGroups = ''

       if'DBClusterMembers' in Clust:
           for DBClusterMembers in Clust['DBClusterMembers']:
               IsClusterWriter = str(DBClusterMembers['IsClusterWriter'])
               DBClusterParameterGroupStatus = str(DBClusterMembers['DBClusterParameterGroupStatus'])
               PromotionTier = str(DBClusterMembers['PromotionTier'])
               DBInstanceIdentifier = str(DBClusterMembers['DBInstanceIdentifier'])
       else:
           DBClusterMembers = ''
       if 'Port' in Clust:
           Port = str(Clust['Port'])
       else:
           Port = ''
       if 'AvailabilityZones' in Clust:
           AvailabilityZoneslist = Clust['AvailabilityZones']
           for i in range(len(AvailabilityZoneslist)):
               AvailabilityZones+= AvailabilityZoneslist[i]+','           
           
       else:
           AvailabilityZoneslist = ''
       if 'DBClusterParameterGroup' in Clust:
           DBClusterParameterGroup = str(Clust['DBClusterParameterGroup'])
       else :
           DBClusterParameterGroup = ''
       if 'DatabaseName' in Clust:
           DatabaseName = str(Clust['DatabaseName'])
       else:
           DatabaseName = ''
       if 'StorageEncrypted'in Clust:
           StorageEncrypted = str(Clust['StorageEncrypted'])
       else :
           StorageEncrypted = ''
       if 'DBClusterArn' in Clust:
           DBClusterArn = str(Clust['DBClusterArn'])
       else:
           DBClusterArn =''
       if 'DbClusterResourceId' in Clust:
           DbClusterResourceId = str(Clust['DbClusterResourceId'])
       else:
           DbClusterResourceId =''
       if 'DBClusterIdentifier' in Clust:
           DBClusterIdentifier= str(Clust['DBClusterIdentifier'])
       else:
           DBClusterIdentifier = ''
       if 'EngineVersion' in Clust:
           EngineVersion = str(Clust['EngineVersion'])
       else :
           EngineVersion = ''
       if 'AssociatedRoles' in Clust:
           AssociatedRoles = str(Clust['AssociatedRoles'])
       else:
           AssociatedRoles = ''
       if 'EarliestRestorableTime' in Clust:
           EarliestRestorableTime = str((Clust['EarliestRestorableTime']).date())
       else:
           EarliestRestorableTime = ''
       if 'Endpoint' in Clust:
           Endpoint = str(Clust['Endpoint'])
       else:
           Endpoint = ''
       if 'Engine' in Clust:
           Engine = str(Clust['Engine'])
       else:
           Engine = ''
       if 'PreferredMaintenanceWindow' in Clust:
           PreferredMaintenanceWindow = str(Clust['PreferredMaintenanceWindow'])
       else:
           PreferredMaintenanceWindow = ''
       if 'BackupRetentionPeriod' in Clust:
           BackupRetentionPeriod = str(Clust['BackupRetentionPeriod'])
       else:
           BackupRetentionPeriod = ''
       if 'AllocatedStorage' in Clust:
           AllocatedStorage = str(Clust['AllocatedStorage'])
       else:
           AllocatedStorage = ''
       if 'ReaderEndpoint' in Clust:
           ReaderEndpoint = str(Clust['ReaderEndpoint'])
       else :
           ReaderEndpoint = ''
       if 'ReadReplicaIdentifiers' in Clust:
           ReadReplicaIdentifiers = str(Clust['ReadReplicaIdentifiers'])
       else:
           ReadReplicaIdentifiers = ''
       if 'HostedZoneId' in Clust:
           HostedZoneId = str(Clust['HostedZoneId'])
       else:
           HostedZoneId = ''
       if 'Status'in Clust:
           Status = str(Clust['Status'])
       else:
           Status = ''
       if 'PreferredBackupWindow' in Clust:
           PreferredBackupWindow = str(Clust['PreferredBackupWindow'])
       else:
           PreferredBackupWindow = ''
       if 'LatestRestorableTime' in Clust:
           LatestRestorableTime = str((Clust['LatestRestorableTime']).date())
       else:
           LatestRestorableTime = ''
       if 'DBSubnetGroup' in Clust:
           DBSubnetGroup = str(Clust['DBSubnetGroup'])
       else:
           DBSubnetGroup = ''
       textfile.write(masterUsername + '|' + VpcSecurityGroups_Status +
                       '|' + VpcSecurityGroupId + '|' + Port + '|' + 
                       AvailabilityZones + '|' + DBClusterParameterGroup +
                       '|' + DatabaseName + '|' + StorageEncrypted + '|' +
                       DBClusterArn + '|' + DbClusterResourceId + '|' +
                       DBClusterIdentifier + '|' + EngineVersion + '|' +
                       AssociatedRoles + '|' + EarliestRestorableTime + '|'+
                       Endpoint + '|' + Engine + '|' + PreferredMaintenanceWindow +
                       '|' + BackupRetentionPeriod + '|'+ AllocatedStorage + '|'
                       + ReaderEndpoint + '|' + ReadReplicaIdentifiers + '|' +
                       HostedZoneId + '|' + Status + '|' + PreferredBackupWindow +
                       '|' + LatestRestorableTime + '|' + DBSubnetGroup + '|'+"\n")
                       #IsClusterWriter + '|' +DBClusterParameterGroupStatus +
                       #'|' +PromotionTier + '|'+DBInstanceIdentifier +"\n")
        
       query = "insert into "+ tbName +" values ('" + masterUsername + "','" +\
                 VpcSecurityGroups_Status + "','" + VpcSecurityGroupId + \
                 "','" + Port + "','" + AvailabilityZones + "','" + \
                 DBClusterParameterGroup + "','" + DatabaseName + "','" +\
                 StorageEncrypted + "','" + DBClusterArn + "','" +\
                 DbClusterResourceId + "','" + DBClusterIdentifier + "','" +\
                 EngineVersion + "','" + AssociatedRoles + "','" +\
                 EarliestRestorableTime + "','" + Endpoint + "','" + Engine +\
                 "','" + PreferredMaintenanceWindow + "','" + \
                 BackupRetentionPeriod + "','" + AllocatedStorage + "','" +\
                 ReaderEndpoint + "','" + ReadReplicaIdentifiers + "','" + \
                 HostedZoneId + "','"+ Status + "','"+ PreferredBackupWindow +\
                 "','"+ LatestRestorableTime +"','"+ DBSubnetGroup +"')"
                 #IsClusterWriter + "','" + DBClusterParameterGroupStatus +\
                 #"','" + PromotionTier + '|'+ DBInstanceIdentifier + "')"
       #print(query)
       cursor.execute(query)

def connect():
    global connection
    global cursor
    global tbName
    try:
        connection = mysql.connector.connect(host='110.110.110.170',
                                             user='root',
                                             password='root')
        if  connection.is_connected():
            print 'Connection got established'
        cursor = connection.cursor()
        dbName = 'cloud_assessment'
        tbName = 'rds_static_cluster'+str(datetime.datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        connection.set_database(dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS "+tbName+"(masterUsername varchar(50),\
                   VpcSecurityGroups_Status varchar(50),VpcSecurityGroupId varchar(50),\
                   Port varchar(5),AvailabilityZones varchar(20),DBClusterParameterGroup varchar(50),\
                   DatabaseName varchar(50),StorageEncrypted date,DBClusterArn varchar(50),\
                   DbClusterResourceId varchar(10),DBClusterIdentifier varchar(50),\
                   EngineVersion varchar(10),AssociatedRoles varchar(50),EarliestRestorableTime date,\
                   Endpoint varchar(10),Engine varchar(10),PreferredMaintenanceWindow varchar(50),\
                   BackupRetentionPeriod varchar(50),AllocatedStorage varchar(50),\
                   ReaderEndpoint varchar(50),ReadReplicaIdentifiers varchar(50),\
                   HostedZoneId varchar(50),Status varchar(20),PreferredBackupWindow varchar(50),\
                   LatestRestorableTime date,DBSubnetGroup varchar(50),PRIMARY KEY (DBClusterIdentifier))"
                   #IsClusterWriter varchar(50),\
                   #DBClusterParameterGroupStatus varchar(50),PromotionTier varchar(50),\
                   #DBInstanceIdentifier varchar(50),PRIMARY KEY (DBClusterIdentifier))"

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

        textfile = open('RDSMetrics_Cluster_mysqlimport_1.txt', 'a+')
        textfile.write("masterUsername |VpcSecurityGroups_Status|"
                       "VpcSecurityGroupId|Port|AvailabilityZones|DBClusterParameterGroup|"
                       "DatabaseName|StorageEncrypted|DBClusterArn|DbClusterResourceId|"
                       "DBClusterIdentifier|EngineVersion|AssociatedRoles|EarliestRestorableTime|"
                       "Endpoint|Engine|PreferredMaintenanceWindow|BackupRetentionPeriod|"
                       "AllocatedStorage|ReaderEndpoint|ReadReplicaIdentifiers|HostedZoneId|Status|"
                       "PreferredBackupWindow|LatestRestorableTime|DBSubnetGroup"+"\n")
                       #|IsClusterWriter|"
                       #"DBClusterParameterGroupStatus|PromotionTier|DBInstanceIdentifier"+"\n")

        for eachRegion in RDSRegion:
            print(eachRegion['RegionName'])
            RDS = boto3.client('rds',region_name = eachRegion['RegionName'])
            DescRDS = RDS.describe_db_clusters()
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


