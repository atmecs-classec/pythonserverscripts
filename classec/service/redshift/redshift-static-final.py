#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime
import sys


def ToCheckForNextMarker(retrieveNextCluster):
    if 'Marker' in retrieveNextCluster:
        ToLoadDataOntoFile(retrieveNextCluster)
        withNextMarker = redshiftClient.describe_clusters(NextToken=retrieveNextCluster['Marker'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextCluster)


def ToLoadDataOntoFile(Datatoload):
    ListOfAllCluster = Datatoload['Clusters']  # getting all instances
    print(len(ListOfAllCluster))
    for cluster in ListOfAllCluster:
        clusterId = cluster['ClusterIdentifier']
        allowVersionUpgrade = cluster['AllowVersionUpgrade']
        automatedSnapshotRetentionPeriod = cluster['AutomatedSnapshotRetentionPeriod']
        availabilityZone = cluster['AvailabilityZone']
        clusterCreateTime = cluster['ClusterCreateTime']
        clusterRevisionNumber = cluster['ClusterRevisionNumber']
        clusterStatus = cluster['ClusterStatus']
        clusterSubnetGroupName = cluster['ClusterSubnetGroupName']
        clusterVersion = cluster['ClusterVersion']
        dbName = cluster['DBName']
        encrypted = cluster['Encrypted']
        enhancedVpcRouting = cluster['EnhancedVpcRouting']
        nodeType = cluster['NodeType']
        numberOfNodes = cluster['NumberOfNodes']
        preferredMaintenanceWindow = cluster['PreferredMaintenanceWindow']
        vpcId = cluster['VpcId']
        nodeRole = ''
        parameterApplyStatus = ''
        tags_Name = ''
        tags_Env = ''
        tags_Brand = ''
        tags_Service = ''
        tags_Domain = ''
        tags_Segment = ''
        tags_Role = ''
        tags_Country = ''
        for parameterGroup in cluster['ClusterParameterGroups']:
            if parameterApplyStatus == '':
                parameterApplyStatus = parameterGroup['ParameterApplyStatus']
            else:
                parameterApplyStatus = parameterApplyStatus + "," + parameterGroup['ParameterApplyStatus']

        for nodes in cluster['ClusterNodes']:
            if nodeRole == '':
                nodeRole = nodes['NodeRole']
            else:
                nodeRole = nodeRole + "," + nodes['NodeRole']

        for tags in cluster['Tags']:
            if tags['Key'] == 'Name':
                tags_Name = tags['Value']
            elif tags['Key'] == 'Env':
                tags_Env = tags['Value']
            elif tags['Key'] == 'Brand':
                tags_Brand = tags['Value']
            elif tags['Key'] == 'Service':
                tags_Service = tags['Value']
            elif tags['Key'] == 'Segment':
                tags_Segment = tags['Value']
            elif tags['Key'] == 'Domain':
                tags_Domain = tags['Value']
            elif tags['Key'] == 'Role':
                tags_Role = tags['Value']
            elif tags['Key'] == 'Country':
                tags_Country = tags['Value']

        textfile.write(clusterId + "|" + str(allowVersionUpgrade) + "|" + str(
            automatedSnapshotRetentionPeriod) + "|" + availabilityZone + "|" + str(clusterCreateTime) + "|" + str(
            clusterRevisionNumber) + "|" + clusterStatus + "|" + clusterSubnetGroupName + "|" + str(
            clusterVersion) + "|" + dbName + "|" + str(encrypted) + "|" + str(
            enhancedVpcRouting) + "|" + nodeType + "|" + str(
            numberOfNodes) + "|" + preferredMaintenanceWindow + "|" + vpcId + "|" + nodeRole + "|" + parameterApplyStatus + "|" + tags_Name + "|" + tags_Env + "|" + tags_Brand + "|" + tags_Service + "|" + tags_Segment + "|" + tags_Domain + "|" + tags_Role + "|" + tags_Country + "\n")

        query = "insert into " + tbName + " values ('" + clusterId + "','" + str(allowVersionUpgrade) + "','" + str(
            automatedSnapshotRetentionPeriod) + "','" + availabilityZone + "','" + str(clusterCreateTime) + "','" + str(
            clusterRevisionNumber) + "','" + clusterStatus + "','" + clusterSubnetGroupName + "','" + str(
            clusterVersion) + "','" + dbName + "','" + str(encrypted) + "','" + str(
            enhancedVpcRouting) + "','" + nodeType + "','" + str(
            numberOfNodes) + "','" + preferredMaintenanceWindow + "','" + vpcId + "','" + nodeRole + "','" + parameterApplyStatus + "','" + tags_Name + "','" + tags_Env + "','" + tags_Brand + "','" + tags_Service + "','" + tags_Segment + "','" + tags_Domain + "','" + tags_Role + "','" + tags_Country + "')"
        cursor.execute(query)

        connection.commit();


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
        # dbName = 'ec2_staticDB_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))
        dbName = sys.argv[1]
        tbName = 'redshift_static'
        createDB = 'CREATE DATABASE IF NOT EXISTS ' + dbName
        cursor.execute(createDB)
        connection.set_database(dbName)
        dropQuery = 'DROP TABLE IF EXISTS ' + tbName
        cursor.execute(dropQuery)
        #	ClusterID,AllowVersionUpgrade,AutomatedSnapshotRetentionPeriod,AvailabilityZone,ClusterCreateTime,ClusterRevisionNumber,ClusterStatus,ClusterSubnetGroupName,ClusterVersion,DBName,Encrypted,EnhancedVpcRouting,NodeType,NumberOfNodes,PreferredMaintenanceWindow,VpcId,NodeRole,ParameterApplyStatus, Tags(Name,Env,Brand,Service,Domain,Segment,Role,Country)


        createTB = "CREATE TABLE IF NOT EXISTS " + tbName + "(ClusterID varchar(50),allowVersionUpgrade BOOLEAN,automatedSnapshotRetentionPeriod INT," \
                                                            "availabilityZone varchar(10),clusterCreateTime DateTime,clusterRevisionNumber INT,clusterStatus varchar(10)," \
                                                            "clusterSubnetGroupName varchar(50),clusterVersion varchar(10),dbName varchar(10),encrypted BOOLEAN,enhancedVpcRouting BOOLEAN," \
                                                            "nodeType varchar(20),numberOfNodes INT,preferredMaintenanceWindow varchar(20),vpcId varchar(20),nodeRole varchar(150)," \
                                                            "parameterApplyStatus varchar(50),tags_Name varchar(10),tags_Env varchar(10),tags_Brand varchar(10),tags_Service varchar(10)," \
                                                            "tags_Segment varchar(10),tags_Domain varchar(10),tags_Role varchar(10),tags_Country varchar(10), PRIMARY KEY (ClusterID))"
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
        allEc2Region = EC2Client.describe_regions()
        Ec2Region = allEc2Region['Regions']

        filename = "redshift-static-mysql.txt"
        textfile = open(filename, 'a+')
        # textfile.write("ebs_volumeid|ebs_snap_id|ebs_size|ebs_region|ebs_state|ebs_create_date|ebs_volume_type|ebs_iops|ebs_instance_id|ebs_device|ebs_attachment_state|ebs_attach_time|ebs_delete_on_termination|ebs_service"+"\n")

        for eachRegion in Ec2Region:
            print(eachRegion['RegionName'])
            redshiftClient = boto3.client('redshift', region_name=eachRegion['RegionName'])
            allClusters = redshiftClient.describe_clusters()
            ToCheckForNextMarker(allClusters)
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