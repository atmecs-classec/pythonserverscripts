#!/var/lib/python
import boto3
import datetime
import mysql.connector
from mysql.connector import Error

def getdata():
    global textfile
    print "getting data into file......"
    filename='/var/lib/mysql-files/govind-data/ec2-dynamic-data-'+str(datetime.datetime.now().strftime('%Y_%m_%d'))+'.txt'
    textfile=open(filename,'a+')
    end_date=datetime.datetime.now()
    start_date=datetime.datetime.now() - datetime.timedelta(days=14)
    ec2_client=boto3.client('ec2')
    region_json=ec2_client.describe_regions()
    regions=region_json['Regions']
    for region in regions:
        regionname=region['RegionName']
        ec2client=boto3.client('ec2',region_name=regionname)
        instance_json=ec2client.describe_instances()
        reservations=instance_json['Reservations']
        for instances in reservations:
            instance_data=instances['Instances']
            for instance in instance_data:
                instanceid=instance['InstanceId']
                monitoring=instance['Monitoring']
                monitoring_state=monitoring['State']
                if monitoring_state == 'enabled':
                    cwClient=boto3.client('cloudwatch',region_name=regionname)
                    instMetrics=cwClient.list_metrics(Namespace = 'AWS/EC2')
        #metricList=volMetrics['Metrics']
        #for metricName in metricList:
                    instCPUUtilization=cwClient.get_metric_statistics(
                        Namespace='AWS/EC2',
                        MetricName='CPUUtilization',
                        Dimensions=[
                                {
                                        'Name': 'InstanceId',
                                        'Value': instanceid
                                },
                        ],
                        StartTime=start_date.strftime('%Y-%m-%dT%H:%M:%S'),
                        EndTime=end_date.strftime('%Y-%m-%dT%H:%M:%S'),
                        Period=1209600,
                        Statistics=[
                                'Average','Minimum','Maximum',
                        ],
                    )
#       textfile.write(volumeid+"|")

                    if len(instCPUUtilization['Datapoints']) == 1:
                        for instCPUUtil in instCPUUtilization['Datapoints']:
                            textfile.write(instanceid+"|"+str(instCPUUtil['Maximum'])+"|"+str(instCPUUtil['Minimum'])+"|"+str(instCPUUtil['Average']))
                    else:
                        textfile.write(instanceid+"|"+str(0.0)+"|"+str(0.0)+"|"+str(0.0))

                    textfile.write("|"+start_date.strftime('%Y-%m-%d')+"|"+end_date.strftime('%Y-%m-%d')+"\n")
    textfile.close()


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
        tbName = 'ec2_dynamic_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        cursor.execute("use "+dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS "+tbName+"(inst_id varchar(50),ec2_cpu_util_max double,ec2_cpu_util_min double," \
                   "ec2_cpu_util_avg double,ec2_start_time Date,ec2_end_time Date,PRIMARY KEY (inst_id))"
        cursor.execute(createTB)
		
	query="load data local infile '/var/lib/mysql-files/govind-data/ec2-dynamic-data-"+str(datetime.datetime.now().strftime('%Y_%m_%d'))+".txt' into table "+tbName+" fields terminated by '|'"
	cursor.execute(query)
	print "file loaded successfully"
	connection.commit()

    except Error as e:
        print(e)
        cursor.close()
        connection.close()

if __name__ == '__main__':
    print 'Hello'
    getdata()
    connect()

