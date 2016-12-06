#!/var/lib/python
import boto3
import datetime
import mysql.connector
from mysql.connector import Error

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
        tbName = 'ebs_dynamic_'+str(datetime.datetime.now().strftime('%Y_%m_%d'))
        createDB = 'CREATE DATABASE IF NOT EXISTS '+dbName
        cursor.execute(createDB)
        cursor.execute("use "+dbName)
        dropQuery = 'DROP TABLE IF EXISTS '+tbName
        cursor.execute(dropQuery)

        createTB = "CREATE TABLE IF NOT EXISTS "+tbName+"(vol_id varchar(50),ebs_read_ops_max double,ebs_read_ops_min double," \
                   "ebs_read_ops_avg double,ebs_write_ops_max double,ebs_write_ops_min double,ebs_write_ops_avg double," \
                   "ebs_idle_time_max double,ebs_idle_time_min double,ebs_idle_time_avg double,ebs_q_len_max double," \
                   "ebs_q_len_min double,ebs_q_len_avg double,ebs_burst_bal_max double,ebs_burst_bal_min double," \
                   "ebs_burst_bal_avg double,ebs_start_time Date,ebs_end_time Date,PRIMARY KEY (vol_id))"
        cursor.execute(createTB)
	query="load data infile '/var/lib/mysql-files/ebs-dynamic-data-"+str(datetime.datetime.now().strftime('%Y_%m_%d'))+".txt' into table "+tbName+" fields terminated by '|'"
	cursor.execute(query)
	connection.commit()

    except Error as e:
        print(e)
        cursor.close()
        connection.close()

if __name__ == '__main__':
    global textfile
    filename="/var/lib/mysql-files/ebs-dynamic-data-"+str(datetime.datetime.now().strftime('%Y_%m_%d'))+".txt"
    textfile=open(filename,'a+')
    end_date=datetime.datetime.now()
    start_date=datetime.datetime.now() - datetime.timedelta(days=14)
    ec2_client=boto3.client('ec2')
    region_json=ec2_client.describe_regions()
    regions=region_json['Regions']
    for region in regions:
        regionname=region['RegionName']
        ec2client=boto3.client('ec2',region_name=regionname)
        volume_json=ec2client.describe_volumes()
        volumes=volume_json['Volumes']
        for volume in volumes:
            volumeid=volume['VolumeId']
            cwClient=boto3.client('cloudwatch',region_name=regionname)
	    volMetrics=cwClient.list_metrics(Namespace = 'AWS/EBS')
	#metricList=volMetrics['Metrics']
	#for metricName in metricList:
	    volReadOps=cwClient.get_metric_statistics(
		    Namespace='AWS/EBS',
		    MetricName='VolumeReadOps',
		    Dimensions=[
			    {
				    'Name': 'VolumeId',
				    'Value': volumeid
			    },
		    ],
		    StartTime=start_date.strftime('%Y-%m-%dT%H:%M:%S'),
		    EndTime=end_date.strftime('%Y-%m-%dT%H:%M:%S'),
		    Period=1209600,
		    Statistics=[
			    'Average','Minimum','Maximum',
		    ], 
	        )
#	textfile.write(volumeid+"|")

	    if len(volReadOps['Datapoints']) == 1:
	        for volROps in volReadOps['Datapoints']:
		    textfile.write(volumeid+"|"+str(volROps['Maximum'])+"|"+str(volROps['Minimum'])+"|"+str(volROps['Average']))
	    else:
	        textfile.write(volumeid+"|"+str(0.0)+"|"+str(0.0)+"|"+str(0.0))
	
	    volWriteOps=cwClient.get_metric_statistics(
                    Namespace='AWS/EBS',
                    MetricName='VolumeWriteOps',
                    Dimensions=[
                            {
                                    'Name': 'VolumeId',
                                    'Value': volumeid
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

            if len(volWriteOps['Datapoints']) == 1:
                for volWOps in volWriteOps['Datapoints']:
                    textfile.write("|"+str(volWOps['Maximum'])+"|"+str(volWOps['Minimum'])+"|"+str(volWOps['Average']))
            else:
                textfile.write("|"+str(0.0)+"|"+str(0.0)+"|"+str(0.0))

	    volIdleTime=cwClient.get_metric_statistics(
                    Namespace='AWS/EBS',
                    MetricName='VolumeIdleTime',
                    Dimensions=[
                            {
                                    'Name': 'VolumeId',
                                    'Value': volumeid
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

            if len(volIdleTime['Datapoints']) == 1:
                for volIdleT in volIdleTime['Datapoints']:
                    textfile.write("|"+str(volIdleT['Maximum'])+"|"+str(volIdleT['Minimum'])+"|"+str(volIdleT['Average']))
            else:
                textfile.write("|"+str(0.0)+"|"+str(0.0)+"|"+str(0.0))

	    volQLength=cwClient.get_metric_statistics(
                    Namespace='AWS/EBS',
                    MetricName='VolumeQueueLength',
                    Dimensions=[
                            {
                                    'Name': 'VolumeId',
                                    'Value': volumeid
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

            if len(volQLength['Datapoints']) == 1:
                for volQLen in volQLength['Datapoints']:
                    textfile.write("|"+str(volQLen['Maximum'])+"|"+str(volQLen['Minimum'])+"|"+str(volQLen['Average']))
            else:
                textfile.write("|"+str(0.0)+"|"+str(0.0)+"|"+str(0.0))

	    volBurstBalance=cwClient.get_metric_statistics(
                    Namespace='AWS/EBS',
                    MetricName='VolumeBurstBalance',
                    Dimensions=[
                            {
                                    'Name': 'VolumeId',
                                    'Value': volumeid
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

            if len(volBurstBalance['Datapoints']) == 1:
                for volBurstBal in volBurstBalance['Datapoints']:
                    textfile.write("|"+str(volBurstBal['Maximum'])+"|"+str(volBurstBal['Minimum'])+"|"+str(volBurstBal['Average']))
            else:
                textfile.write("|"+str(0.0)+"|"+str(0.0)+"|"+str(0.0))
    	
            textfile.write("|"+start_date.strftime('%Y-%m-%d')+"|"+end_date.strftime('%Y-%m-%d')+"\n")        
    textfile.close()
    connect()

