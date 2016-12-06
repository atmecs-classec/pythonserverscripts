#!/usr/bin/python
import boto3
import timeit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from  redshiftSchema import Base, redshiftModel


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
    counter = 0
    recordBuilder = list()
    for cluster in ListOfAllCluster:
        ClusterID = cluster['ClusterIdentifier']
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

        counter = counter + 1
        record = redshiftModel(ClusterID,allowVersionUpgrade,automatedSnapshotRetentionPeriod,availabilityZone,
                                  clusterCreateTime,clusterRevisionNumber,clusterStatus, clusterSubnetGroupName,
                                  clusterVersion, dbName, encrypted,enhancedVpcRouting,nodeType, numberOfNodes,
                                  preferredMaintenanceWindow,vpcId,nodeRole, parameterApplyStatus,tags_Name, tags_Env,
                                  tags_Brand, tags_Service, tags_Segment, tags_Domain, tags_Role, tags_Country)
        recordBuilder.append(record)

        if 500 == counter:
            session.bulk_save_objects(recordBuilder)
            session.commit()
            counter = 0
            recordBuilder = []

    session.bulk_save_objects(recordBuilder)
    session.commit()

if __name__ == '__main__':
    start_time = timeit.default_timer()
    global session
    engine = create_engine('mysql://root:root@110.110.110.164/cloud_assessment')
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    print "Creating table elb_static_data"
    if engine.dialect.has_table(engine, redshiftModel.__tablename__):
        redshiftModel.__table__.drop()
    redshiftModel.__table__.create()

    EC2Client = boto3.client('ec2')
    allEc2Region = EC2Client.describe_regions()
    Ec2Region = allEc2Region['Regions']

    for eachRegion in Ec2Region:
        print(eachRegion['RegionName'])
        redshiftClient = boto3.client('redshift', region_name=eachRegion['RegionName'])
        allClusters = redshiftClient.describe_clusters()
        ToCheckForNextMarker(allClusters)
    session.commit()
    elapsed = timeit.default_timer() - start_time
    print elapsed