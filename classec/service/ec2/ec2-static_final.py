#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime

def ToCheckForNextMarker(retrieveNextEC2):
    if 'NextToken' in retrieveNextEC2:
        ToLoadDataOntoFile(retrieveNextEC2)
        withNextMarket = EC2.describe_instances(NextToken=retrieveNextEC2['NextToken'])
        ToCheckForNextMarker(withNextMarket)
    else:
        ToLoadDataOntoFile(retrieveNextEC2)

def ToLoadDataOntoFile(Datatoload):
    ListOfAllInst = Datatoload['Reservations']  # getting all instances
    print(len(ListOfAllInst))
    for Inst in ListOfAllInst:
        EachInst = Inst['Instances']
        for instDetails in EachInst:
            ec_id = instDetails['InstanceId']
            ec2_amiid = instDetails['ImageId']
            ec2_type = instDetails['InstanceType']
            ec2_state = instDetails['State']['Name']
            ec2_launchdate = (instDetails['LaunchTime']).date()
            #ec2_launchdate = (dateutil.parser.parse(instDetails['LaunchTime'])).strftime('%Y-%m-%d')
            ec2_monitoring = instDetails['Monitoring']['State']
            ec2_reserveid = ''
            if 'ReservationId' in Inst:
                ec2_reserveid = Inst['ReservationId']
            ec2_subnet = ''
            if 'SubnetId' in instDetails:
                ec2_subnet = instDetails['SubnetId']
            ec2_hypervisor = instDetails['Hypervisor']
            ec2_vpc = ''
            if 'VpcId' in instDetails:
                ec2_vpc = instDetails['VpcId']
            ec2_region = instDetails['Placement']['AvailabilityZone']
            ec2_EbsOptimized = instDetails['EbsOptimized']
            ec2_Architecture = instDetails['Architecture']
            ec2_platform = ''
            if 'Platform' in instDetails:
                ec2_platform = instDetails['Platform']
            ec2_domain = ''
            ec2_env = ''
            ec2_name = ''
            if 'Tags' in instDetails:
                tags = instDetails['Tags']
                for tag in tags:
                    if tag['Key'] == 'Domain':
                        ec2_domain = tag['Value']
                    if tag['Key'] == 'Env':
                        ec2_env = tag['Value']
                    if tag['Key'] == 'Name':
                        ec2_name = tag['Value']
            textfile.write(ec_id+'|'+ec2_amiid+'|'+ec2_type+'|'+ec2_state+'|'+ec2_domain+'|'+ec2_env+'|'+ec2_name+'|'+ec2_region+'|'+str(ec2_launchdate)+'|'+ec2_monitoring+'|'+ec2_reserveid+'|'+ec2_subnet+'|'+ec2_hypervisor+'|'+ec2_vpc+'|'+str(ec2_EbsOptimized)+'|'+ec2_Architecture+'|'+ec2_platform+"\n")

            query = "insert into "+tbName+" values ('"+ec_id+"','"+ec2_amiid+"','"+ec2_type+"','"+ec2_state+"','"+ec2_domain+"','"+ec2_env+"','"+ec2_name+"','"+ec2_region+"','"+str(ec2_launchdate)+"','"+ec2_monitoring+"','"+ec2_reserveid+"','"+ec2_subnet+"','"+ec2_hypervisor+"','"+ec2_vpc+"','"+str(ec2_EbsOptimized)+"','"+ec2_Architecture+"','"+ec2_platform+"')"
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
        #dbName = 'ec2_staticDB_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))
        dbName = 'cloud_assessment'
        tbName = 'ec2_static_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        connection.set_database(dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS "+tbName+"(ec_id varchar(50),ec2_amiid varchar(50),ec2_type varchar(50)," \
                   "ec2_state varchar(50),ec2_domain varchar(50),ec2_env varchar(50),ec2_name varchar(50)," \
                   "ec2_region varchar(50),ec2_launchdate date,ec2_monitoring varchar(50)," \
                   "ec2_reserveid varchar(50),ec2_subnet varchar(50),ec2_hypervisor varchar(50)," \
                   "ec2_vpc varchar(50),ec2_EbsOptimized BOOLEAN,ec2_Architecture varchar(50),ec2_platform varchar(30),PRIMARY KEY (ec_id))"
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
        textfile = open('Ec2Metrics_mysqlimport_1.txt', 'a+')
        textfile.write("ec_id|ec2_amiid|ec2_type|ec2_state|ec2_domain|ec2_env|ec2_name|ec2_region|ec2_launchdate|ec2_monitoring|ec2_reserveid|ec2_subnet|ec2_hypervisor|ec2_vpc|ec2_EbsOptimized|ec2_Architecture|ec2_platform"+"\n")

        for eachRegion in Ec2Region:
            print(eachRegion['RegionName'])
            EC2 = boto3.client('ec2', region_name=eachRegion['RegionName'])
            DescEC2 = EC2.describe_instances()
            ToCheckForNextMarker(DescEC2)
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
