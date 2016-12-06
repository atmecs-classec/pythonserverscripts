#!/usr/bin/python
import boto3
import timeit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from snapshotSchema import Base,snapshotModel


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
    counter = 0
    recordBuilder = list()
    for snap in ListOfAllSnap:
        snapshot_id = snap['SnapshotId']
        volume_id = snap['VolumeId']
        volume_size = snap['VolumeSize']
        state = snap['State']
        start_time = str(snap['StartTime'])
        progress = snap['Progress']
        owner_id = snap['OwnerId']
        desc = snap['Description']
        if "\'" in desc:
            description = desc.replace("\'", "")
        else:
            description = desc
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

        print(snapshot_id,volume_id,volume_size,start_time,state,progress,encrypted,owner_id,description,
                 tag_Name,tag_Domain ,tag_Source ,tag_Service,tag_BackupType,tag_Date)
        session.add(snapshotModel(snapshot_id,volume_id,volume_size,start_time,state,progress,encrypted,owner_id,description,
                 tag_Name,tag_Domain ,tag_Source ,tag_Service,tag_BackupType,tag_Date))

        counter = counter + 1
        record = snapshotModel(snapshot_id,volume_id,volume_size,start_time,state,progress,encrypted,owner_id,description,
                 tag_Name,tag_Domain ,tag_Source ,tag_Service,tag_BackupType,tag_Date)
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
    engine = create_engine('mysql://root:root@110.110.110.164/test_govind')
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    print "Creating table elb_static_data"
    if engine.dialect.has_table(engine, snapshotModel.__tablename__):
        snapshotModel.__table__.drop()
    snapshotModel.__table__.create()


    EC2Client = boto3.client('ec2')
    allEc2Region = EC2Client.describe_regions()
    Ec2Region = allEc2Region['Regions']

    for eachRegion in Ec2Region:
        print(eachRegion['RegionName'])
        EC2 = boto3.client('ec2', region_name=eachRegion['RegionName'])
        DescSnap = EC2.describe_snapshots()
        ToCheckForNextMarker(DescSnap)
    session.commit()
    elapsed = timeit.default_timer() - start_time
    print elapsed