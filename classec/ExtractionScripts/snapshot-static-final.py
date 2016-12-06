#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime

def ToCheckForNextMarker(retrieveNextSnap):
    if 'NextToken' in retrieveNextSnap:
        ToLoadDataOntoFile(retrieveNextSnap)
        withNextMarker = EC2.describe_snapshots(NextToken=retrieveNextSnap['NextToken'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextSnap)

def ToLoadDataOntoFile(Datatoload):
    ListOfAllSnap = Datatoload['Snapshots']  # getting all instances
    print(len(ListOfAllSnap))
    for snap in ListOfAllSnap:
		snap_id = snap['SnapshotId']
		vol_id = snap['VolumeId']
		vol_size = snap['VolumeSize']
	        state = snap['State']
        	start_time = (snap['StartTime']).date()
	        progress = snap['Progress']
		owner_id = snap['OwnerId']
		description = snap['Description']
		if "\'" in description:
			desc=description.replace("\'","")
		else:
			desc=description
		encrypted = snap['Encrypted']
		tag_Source = ''
		tag_Name = ''
		tag_Service = ''
		tag_Domain = ''
		tag_BackupType = ''
		tag_Date = ''
		if 'Tags' in snap:
            		tags = snap['Tags']
            		for tag in tags:
                		if tag['Key'] == 'Service':
                    			tag_Service = tag['Value']
				elif tag['Key'] == 'Name':
					tag_Name = tag['Value']
				elif tag['Key'] == 'Source':
					tag_Source = tag['Value']
				elif tag['Key'] == 'Domain':
					tag_Domain = tag['Value']
				elif tag['Key'] == 'BackupType':
					tag_BackupType = tag['Value']
				elif tag['Key'] == 'Date':
					tag_Date = tag['Value']
				
        	textfile.write(snap_id+'|'+vol_id+'|'+str(vol_size)+'|'+str(start_time)+'|'+state+'|'+str(progress)+'|'+str(encrypted)+'|'+owner_id+'|'+desc+'|'+tag_Name+'|'+tag_Domain+'|'+tag_Source+'|'+tag_Service+"|"+tag_BackupType+"|"+str(tag_Date)+"\n")

	        query = "insert into "+tbName+" values ('"+snap_id+"','"+vol_id+"','"+str(vol_size)+"','"+str(start_time)+"','"+state+"','"+str(progress)+"','"+str(encrypted)+"','"+owner_id+"','"+desc+"','"+tag_Name+"','"+tag_Domain+"','"+tag_Source+"','"+tag_Service+"','"+tag_BackupType+"','"+str(tag_Date)+"')"
	        cursor.execute(query)
		connection.commit()

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
        tbName = 'snapshot_static'
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        cursor.execute("use "+dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS "+tbName+"(snapshot_id varchar(50),volume_id varchar(50),volume_size INT," \
                   "start_time Date,state varchar(50),progress varchar(50),encrypted varchar(10),owner_id varchar(50)," \
                   "description varchar(500),tag_Name varchar(20),tag_Domain varchar(20),tag_Source varchar(20),tag_Service varchar(20)," \
		   "tag_BackupType varchar(20),tag_Date varchar(20))"
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

        textfile = open('snapshots-static-data.txt', 'a+')
        textfile.write("snapshot_id|volume-id|volume_size|start-time|state|progress|encrypted|owner-id|description|tag_Name|tag_Domain|tag_Source|tag_Service|tag_BackupType|tag_Date"+"\n")

        for eachRegion in Ec2Region:
            print(eachRegion['RegionName'])
            EC2 = boto3.client('ec2', region_name=eachRegion['RegionName'])
            DescSnap = EC2.describe_snapshots()
            ToCheckForNextMarker(DescSnap)
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
