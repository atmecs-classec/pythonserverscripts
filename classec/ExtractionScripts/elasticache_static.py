#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime


def ToCheckForNextMarker(retrieveNextElastiCache) :
    if 'Marker' in retrieveNextElastiCache :
        ToLoadDataOntoFile(retrieveNextElastiCache)
        withNextMarker = ElastiCache.describe_cache_clusters(Marker=retrieveNextElastiCache['Marker'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextElastiCache)


def ToLoadDataOntoFile(Datatoload):
    # Initialize all the variable which will hold json values

    ListOfAllElastiCacheClusters = ' '
    ElastiCache = '' 
    ListOfAllElastiCacheClusters = Datatoload['CacheClusters'] # getting all elasticache

    print'length of all elasticache ' + str(len(ListOfAllElastiCacheClusters))
    for ElastiCache in ListOfAllElastiCacheClusters:
        if 'CacheClusterId' in ElastiCache:
            CacheClusterId = str(ElastiCache['CacheClusterId'])
        else:
            CacheClusterId = ''

        if 'CacheClusterCreateTime' in ElastiCache:
            CacheClusterCreateTime = str((ElastiCache['CacheClusterCreateTime']).date())
        else:
            CacheClusterCreateTime = ''

        if 'CacheClusterStatus' in ElastiCache:
            CacheClusterStatus = str(ElastiCache['CacheClusterStatus'])
        else:
            CacheClusterStatus = ''

        if 'CacheNodeType' in ElastiCache:
            CacheNodeType = str(ElastiCache['CacheNodeType'])
        else:
            CacheNodeType = ''

        if 'CacheSubnetGroupName' in ElastiCache:
            CacheSubnetGroupName = str(ElastiCache['CacheSubnetGroupName'])
        else:
            CacheSubnetGroupName = ''
        if 'ClientDownloadLandingPage' in ElastiCache:
            ClientDownloadLandingPage = str(ElastiCache['ClientDownloadLandingPage'])
        else:
            ClientDownloadLandingPage = ''

        if 'Engine' in ElastiCache:
            Engine = str(ElastiCache['Engine'])
        else:
            Engine = ''			
	
	if 'EngineVersion' in ElastiCache:
            EngineVersion = str(ElastiCache['EngineVersion'])
        else:
            EngineVersion = ''

	if 'NumCacheNodes' in ElastiCache:
            NumCacheNodes = str(ElastiCache['NumCacheNodes'])
        else:
            NumCacheNodes = ''

        if 'PreferredMaintenanceWindow' in ElastiCache:
            PreferredMaintenanceWindow = str(ElastiCache['PreferredMaintenanceWindow'])
        else:
            PreferredMaintenanceWindow = ''
				   
        if 'PreferredAvailabilityZone' in ElastiCache:
      	    PreferredAvailabilityZone = ElastiCache['PreferredAvailabilityZone']
        else:
            PreferredAvailabilityZone = ''
	
	if 'ReplicationGroupId' in ElastiCache:
            ReplicationGroupId = str(ElastiCache['ReplicationGroupId'])
        else:
            ReplicationGroupId = ''

	if 'SnapshotRetentionLimit' in ElastiCache:
            SnapshotRetentionLimit = str(ElastiCache['SnapshotRetentionLimit'])
        else:
            SnapshotRetentionLimit = ''

	if 'SnapshotWindow' in ElastiCache:
            SnapshotWindow = str(ElastiCache['SnapshotWindow'])
        else:
            SnapshotWindow = ''
        
	if 'AutoMinorVersionUpgrade' in ElastiCache:
            AutoMinorVersionUpgrade = str(ElastiCache['AutoMinorVersionUpgrade'])
        else:
            AutoMinorVersionUpgrade = ''

	if 'CacheParameterGroup' in ElastiCache:
	    ParameterGroupList = ElastiCache['CacheParameterGroup']
            for key,value in ParameterGroupList.iteritems():
		if 'CacheParameterGroupName' == key:
		     CacheParameterGroupName = value
		if 'ParameterApplyStatus' == key:
		     ParameterApplyStatus = value
        else:
	    CacheParameterGroup = ''         
        
        if 'SecurityGroups' in ElastiCache:
            SecurityGroupsList = ElastiCache['SecurityGroups']
            for k in range(len(SecurityGroupsList)):
                for key,value in SecurityGroupsList[k].iteritems():
		    if 'SecurityGroupId' == key:
		        SecurityGroupId = value
		    if 'Status' == key:
		        Status = value
        else:
            SecurityGroups = ''


        textfile.write(CacheClusterId + '|' + CacheClusterCreateTime + '|' +
		       CacheClusterStatus + '|' + CacheNodeType + '|' + 
		       CacheSubnetGroupName + '|' + ClientDownloadLandingPage + '|' + 
		       Engine + '|' + EngineVersion +'|'+ NumCacheNodes + '|'+ 
		       PreferredMaintenanceWindow + '|' + 
		       PreferredAvailabilityZone + '|' + ReplicationGroupId + '|' +
		       SnapshotRetentionLimit + '|' + SnapshotWindow + '|' +
		       AutoMinorVersionUpgrade + '|'+ CacheParameterGroupName + '|'+ 
		       ParameterApplyStatus +'|'+ SecurityGroupId + '|'+ 
		       Status+"\n")

        query = "insert into " + tbName + " values('" + CacheClusterId + "','" +\
		CacheClusterCreateTime + "','" + CacheClusterStatus + "','" + \
		CacheNodeType + "','" + CacheSubnetGroupName + "','" + \
                ClientDownloadLandingPage + "','" + Engine + "','" + \
		EngineVersion + "',' " + NumCacheNodes + "','" + \
		PreferredMaintenanceWindow + "','" + \
		PreferredAvailabilityZone + "','" + ReplicationGroupId + "','"+\
		SnapshotRetentionLimit + "','" + SnapshotWindow + "','" +\
		AutoMinorVersionUpgrade + "','"+ CacheParameterGroupName +"','"+\
		ParameterApplyStatus + "','"+ SecurityGroupId + "','"+\
		Status + "')"

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
        tbName = 'elasticache_static'
        createDB = 'CREATE DATABASE IF NOT EXISTS ' + DBName
        cursor.execute(createDB)
        connection.set_database(DBName)
        dropQuery = 'DROP TABLE IF EXISTS ' + tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS " + tbName + "(CacheClusterId varchar(50),\
                   CacheClusterCreateTime date,CacheClusterStatus varchar(50),CacheNodeType varchar(50),\
                   CacheSubnetGroupName varchar(50),ClientDownloadLandingPage varchar(250),Engine varchar(50),\
                   EngineVersion varchar(60),NumCacheNodes int,PreferredMaintenanceWindow varchar(20),\
		           PreferredAvailabilityZone varchar(90),ReplicationGroupId varchar(50),\
		           SnapshotRetentionLimit varchar(50),SnapshotWindow varchar(50),\
		           AutoMinorVersionUpgrade varchar(50),CacheParameterGroupName varchar(50),\
		           ParameterApplyStatus varchar(50),SecurityGroupId varchar(50),Status varchar(50),\
                   PRIMARY KEY (CacheClusterId))"

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
        allElastiCacheRegion = EC2Client.describe_regions()
        ElastiCacheRegion = allElastiCacheRegion['Regions']

        textfile = open('ElastiCache_mysqlimport.txt','a+') 
        #+ str(datetime.datetime.now()) + '.txt', 'a+')
        textfile.write("CacheClusterId|CacheClusterCreateTime|CacheClusterStatus|CacheNodeType|"
                       "CacheSubnetGroupName|ClientDownloadLandingPage|Engine|EngineVersion|NumCacheNodes|"
	               "PreferredMaintenanceWindow|PreferredAvailabilityZone|ReplicationGroupId|"
	               "SnapshotRetentionLimit|SnapshotWindow|AutoMinorVersionUpgrade|CacheParameterGroupName|"
	               "ParameterApplyStatus|SecurityGroupId|Status" + "\n")

        for eachRegion in ElastiCacheRegion:
            print(eachRegion['RegionName'])
            ElastiCache = boto3.client('elasticache', region_name=eachRegion['RegionName'])
            DescElastiCache = ElastiCache.describe_cache_clusters()
            ToCheckForNextMarker(DescElastiCache)
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
