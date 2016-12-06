#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime

def ToCheckForNextMarker(retrieveNextEBS):
    if 'NextToken' in retrieveNextEBS:
        ToLoadDataOntoFile(retrieveNextEBS)
        withNextMarket = EC2.describe_volumes(NextToken=retrieveNextEBS['NextToken'])
        ToCheckForNextMarker(withNextMarket)
    else:
        ToLoadDataOntoFile(retrieveNextEBS)

def ToLoadDataOntoFile(Datatoload):
    ListOfAllVol = Datatoload['Volumes']  # getting all instances
    print(len(ListOfAllVol))
    for vol in ListOfAllVol:
		ebs_vid = vol['VolumeId']
		ebs_snap_id = vol['SnapshotId']
		ebs_size = vol['Size']
		ebs_region = vol['AvailabilityZone']
	        ebs_state = vol['State']
        	ebs_create_date = (vol['CreateTime']).date()
	        ebs_volume_type = vol['VolumeType']
	#       	iops = vol['Iops']
#		ebs_iops = str(iops)
		ebs_iops = ''
		if 'Iops' in vol:
			ebs_iops = vol['Iops']
		ebs_instance_id = ''
		ebs_attachment_state = ''
		ebs_attach_time = ''
		ebs_delete_on_termination = ''
		ebs_device = ''
		if 'Attachments' in vol:
			attachments = vol['Attachments']
			for attach in attachments:
				ebs_instance_id = attach['InstanceId']
				ebs_attachment_state = attach['State']
				ebs_attach_time = attach['AttachTime']
				ebs_delete_on_termination = attach['DeleteOnTermination']
				ebs_device = attach['Device']
		ebs_service = ''
		if 'Tags' in vol:
            		tags = vol['Tags']
            		for tag in tags:
                		if tag['Key'] == 'Service':
                    			ebs_service = tag['Value']
				
        	textfile.write(ebs_vid+'|'+ebs_snap_id+'|'+str(ebs_size)+'|'+str(ebs_iops)+'|'+ebs_region+'|'+ebs_state+'|'+str(ebs_create_date)+'|'+ebs_volume_type+'|'+ebs_instance_id+'|'+ebs_device+'|'+ebs_attachment_state+'|'+str(ebs_attach_time)+'|'+str(ebs_delete_on_termination)+'|'+ebs_service+"\n")

	        query = "insert into "+tbName+" values ('"+ebs_vid+"','"+ebs_snap_id+"','"+str(ebs_size)+"','"+str(ebs_iops)+"','"+ebs_region+"','"+ebs_state+"','"+str(ebs_create_date)+"','"+ebs_volume_type+"','"+ebs_instance_id+"','"+ebs_device+"','"+ebs_attachment_state+"','"+str(ebs_attach_time)+"','"+str(ebs_delete_on_termination)+"','"+ebs_service+"')"
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
        tbName = 'ebs_static_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        connection.set_database(dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS "+tbName+"(ebs_volumeid varchar(50),ebs_snap_id varchar(50),ebs_size varchar(50)," \
                   "ebs_iops varchar(10),ebs_region varchar(50),ebs_state varchar(50),ebs_create_date date,ebs_volume_type varchar(50)," \
                   "ebs_instance_id varchar(20),ebs_device varchar(50)," \
                   "ebs_attachment_state varchar(50),ebs_attach_time date,ebs_delete_on_termination varchar(50)," \
                   "ebs_service varchar(50))"
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

	filename = "/var/lib/mysql-files/govind-data/ebs-static-data-"+str(datetime.datetime.now().strftime('%Y_%m_%d'))+".txt"
        textfile = open(filename, 'a+')
        textfile.write("ebs_volumeid|ebs_snap_id|ebs_size|ebs_region|ebs_state|ebs_create_date|ebs_volume_type|ebs_iops|ebs_instance_id|ebs_device|ebs_attachment_state|ebs_attach_time|ebs_delete_on_termination|ebs_service"+"\n")

        for eachRegion in Ec2Region:
            print(eachRegion['RegionName'])
            EC2 = boto3.client('ec2', region_name=eachRegion['RegionName'])
            DescEBS = EC2.describe_volumes()
            ToCheckForNextMarker(DescEBS)
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
