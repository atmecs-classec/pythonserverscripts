#!/usr/bin/python
import boto3
import sys
from datetime import datetime, timedelta
from mysql.connector import Error
import mysql.connector

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
        tbName = 'rds_dynamics_'+str(datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        connection.set_database(dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)
        queryList = []
        for metricCol in MetricsList:
            queryList.append(metricCol+'_min DOUBLE')
            queryList.append(metricCol+'_max DOUBLE')
            queryList.append(metricCol+'_avg  DOUBLE')
        createTB = "CREATE TABLE "+tbName+" (DBInstanceIdentifier varchar(50),StartTime DATETIME,EndTime DATETIME," \
                                          "Period BIGINT,"+','.join(metric for metric in queryList)+", PRIMARY KEY (DBInstanceIdentifier))"
        cursor.execute(createTB)

    except Error as e:
        print(e)
        cursor.close()
        connection.close()

def GettingCloudWth(DBInstIdentifier,startTimeRef,endTimeRef,periodRef,CloudWatch):
    cloudWatchMetricInfo=[]
    for metrics in MetricsList:
        ResponseOut = CloudWatch.get_metric_statistics(
            Namespace='AWS/RDS',
            MetricName=metrics,
            Dimensions=[
                {
                    'Name': 'DBInstanceIdentifier',
                    'Value': DBInstIdentifier
                },
            ],
            StartTime=startTimeRef,
            EndTime=endTimeRef,
            Period=periodRef,
            Statistics=[
                'Average', 'Minimum', 'Maximum'
            ]
        )
        Datapoints = ResponseOut['Datapoints']
        if len(Datapoints) > 2:
            print "program getting close reasons: it contain 2 DataPoints"
            sys.exit()
        if len(Datapoints) == 0:
            for i in range(3):
                cloudWatchMetricInfo.append('')
        for datapt in Datapoints:
            cloudWatchMetricInfo.append(datapt['Minimum'] if 'Minimum' in datapt else '')
            cloudWatchMetricInfo.append(datapt['Maximum'] if 'Maximum' in datapt else '')
            cloudWatchMetricInfo.append(datapt['Average'] if 'Average' in datapt else '')

    metricAvgMinMax = "','".join([str(val) for val in cloudWatchMetricInfo])
#   print metricAvgMinMax
    query = "insert into "+tbName+" values('"+DBInstIdentifier+"','"+str(startTimeRef)+"','"+str(endTimeRef)+"','"+str(periodRef)+"','"+metricAvgMinMax+"')"
    cursor.execute(query)
def ToCheckForNextMarker(retrieveNextRDS,RdsRef,CloudWCRef):
    if 'Marker' in retrieveNextRDS:
        DBInstances = retrieveNextRDS['DBInstances']
        print len(DBInstances)
        for DBInstance in DBInstances:
            DBInstanceIdentifier = DBInstance['DBInstanceIdentifier']
            GettingCloudWth(DBInstanceIdentifier, strtTimeRef1, endTimeRef1, periodRef1, CloudWCRef)
        withNextMarker = RdsRef.describe_db_instances(Marker=retrieveNextRDS['Marker'])
        ToCheckForNextMarker(withNextMarker,RdsRef,CloudWCRef)
    else:
        DBInstances = retrieveNextRDS['DBInstances']
        print len(DBInstances)
        for DBInstance in DBInstances:
            DBInstanceIdentifier = DBInstance['DBInstanceIdentifier']
            GettingCloudWth(DBInstanceIdentifier, strtTimeRef1, endTimeRef1, periodRef1, CloudWCRef)


if __name__ == '__main__':
    global MetricsList,strtTimeRef1,endTimeRef1,periodRef1
    MetricsList = ['BinLogDiskUsage','CPUUtilization','CPUCreditUsage','CPUCreditBalance','DatabaseConnections',
                   'DiskQueueDepth','FreeableMemory','FreeStorageSpace','ReplicaLag','SwapUsage','ReadIOPS','WriteIOPS',
                   'ReadLatency','WriteLatency','ReadThroughput','WriteThroughput','NetworkReceiveThroughput',
                   'NetworkTransmitThroughput']
    connect()
    EC2Client = boto3.client('ec2')
    allEc2Region = EC2Client.describe_regions()
    Ec2Region = allEc2Region['Regions']
    strtTimeRef1 = datetime.today() - timedelta(days=14)
    endTimeRef1 = datetime.today()
    periodRef1 = 1209600
    for eachRegion in Ec2Region:
            print(eachRegion['RegionName'])
            CloudWatchRef = boto3.client('cloudwatch', region_name=eachRegion['RegionName'])
            Rds = boto3.client('rds', region_name=eachRegion['RegionName'])
            RdsDescInst = Rds.describe_db_instances()
            ToCheckForNextMarker(RdsDescInst,Rds,CloudWatchRef)
    connection.commit()
    cursor.close()
    connection.close()
