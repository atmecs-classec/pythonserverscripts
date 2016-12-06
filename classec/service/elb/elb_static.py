#!/usr/bin/python
import boto3
import mysql.connector
from mysql.connector import Error
import datetime


def ToCheckForNextMarker(retrieveNextELB) :
    if 'Marker' in retrieveNextELB :
        ToLoadDataOntoFile(retrieveNextELB)
        withNextMarker = ELB.describe_load_balancers(Marker=retrieveNextELB['Marker'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextELB)


def ToLoadDataOntoFile(Datatoload):
    # Initialize all the variable which will hold json values
    ListOfAllLoadBalancers = ' '
    LoadBalancer = ''
    ListOfAllLoadBalancers = Datatoload['LoadBalancerDescriptions']  # getting all LoadBalancer
    print'length of LoadBalancers ' + str(len(ListOfAllLoadBalancers))
    for LoadBalancer in ListOfAllLoadBalancers:
        if 'LoadBalancerName' in LoadBalancer:
            LoadBalancerName = str(LoadBalancer['LoadBalancerName'])
        else:
            LoadBalancerName = ''

        if 'DNSName' in LoadBalancer:
            DNSName = str(LoadBalancer['DNSName'])
        else:
            DNSName = ''

        if 'VPCId' in LoadBalancer:
            VPCId = str(LoadBalancer['VPCId'])
        else:
            VPCId = ''
        if 'CanonicalHostedZoneName' in LoadBalancer:
            CanonicalHostedZoneName = str(LoadBalancer['CanonicalHostedZoneName'])
        else:
            CanonicalHostedZoneName = ''

        if 'CreatedTime' in LoadBalancer:
            CreatedTime = str((LoadBalancer['CreatedTime']).date())
        else:
            CreatedTime = ''
        if 'CanonicalHostedZoneNameID' in LoadBalancer:
            CanonicalHostedZoneNameID = str(LoadBalancer['CanonicalHostedZoneNameID'])
        else:
            CanonicalHostedZoneNameID = ''
        if 'Scheme' in LoadBalancer:
            Scheme = str(LoadBalancer['Scheme'])
        else:
            Scheme = ''			
			
	AvailabilityZones = ''	   
        if 'AvailabilityZones' in LoadBalancer:
            zonelist = LoadBalancer['AvailabilityZones']
	    #print zonelist
            for i in range(len(zonelist)):
                AvailabilityZones += zonelist[i]+' ,'
		print AvailabilityZones
        else:
            AvailabilityZones = ''
        
        Subnets = ''
        if 'Subnets' in LoadBalancer:
            Subnetlist = LoadBalancer['Subnets']
            for ii in range(len(Subnetlist)):
                Subnets += Subnetlist[ii]+' ,'
                print Subnets
        
        else:
            Subnets = ''
        
        if 'Instances' in LoadBalancer:
            Instancelist = LoadBalancer['Instances']
            #print Instancelist	
            for j in range(len(Instancelist)):
                for key,value in Instancelist[j].iteritems():
		    #print value
                     InstanceId = value		    
        else:
            Instances = ''
        
        SecurityGroups = ''
        if 'SecurityGroups' in LoadBalancer:
            list = LoadBalancer['SecurityGroups']
            for k in range(len(list)):
                SecurityGroups += list[k]+' ,'
                print SecurityGroups

        else:
            SecurityGroups = ''

        textfile.write(LoadBalancerName + '|' + DNSName + '|' +
                       CanonicalHostedZoneName + '|' + CanonicalHostedZoneNameID + '|' +
                       VPCId + '|' + Scheme + '|' + CreatedTime + '|' + AvailabilityZones +
                       '|'+ Subnets + '|'+ InstanceId + '|' + SecurityGroups +"\n")

        query = "insert into " + tbName + " values('" + LoadBalancerName + \
                "','" + DNSName + "','" + CanonicalHostedZoneName + "','" +\
                CanonicalHostedZoneNameID + "','" + VPCId + "','" + Scheme +\
                "','" + CreatedTime + "','" + AvailabilityZones + "',' " +\
                Subnets + "','" + InstanceId + "','" + SecurityGroups + "')"

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
        tbName = 'elb_static'
        createDB = 'CREATE DATABASE IF NOT EXISTS ' + DBName
        cursor.execute(createDB)
        connection.set_database(DBName)
        dropQuery = 'DROP TABLE IF EXISTS ' + tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS " + tbName + "(LoadBalancerName varchar(50),\
                   DNSName varchar(50),CanonicalHostedZoneName varchar(50),\
                   CanonicalHostedZoneNameID varchar(50),VPCId varchar(50),\
                   Scheme varchar(50),CreatedTime date,AvailabilityZones varchar(60),\
                   Subnets varchar(60),InstanceId varchar(20),SecurityGroups varchar(90),\
                   PRIMARY KEY (LoadBalancerName))"

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

        textfile = open('ELB_LoadBalancer_mysqlimport_' + str(datetime.datetime.now()) + '.txt', 'a+')
        textfile.write("LoadBalancerName|DNSName|CanonicalHostedZoneName|CanonicalHostedZoneNameID|"
                       "VPCId|Scheme|CreatedTime|AvailabilityZones|Subnets|InstanceId|SecurityGroups" + "\n")

        for eachRegion in ELBRegion:
            print(eachRegion['RegionName'])
            ELB = boto3.client('elb', region_name=eachRegion['RegionName'])
            DescELB = ELB.describe_load_balancers()
            ToCheckForNextMarker(DescELB)
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
