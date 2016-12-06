import timeit
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from EbsSchema import ebsDataWithCosting,Base, ebsCosting


def ToCheckForNextMarker(retrieveNextEbs):
    if 'NextToken' in retrieveNextEbs:
        ToLoadDataOntoFile(retrieveNextEbs)
        withNextMarker = EC2.describe_volumes(NextToken=retrieveNextEbs['NextToken'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextEbs)


def insertEbsStaticWithCost(ebsObject):
    session.add(ebsObject)


def ToLoadDataOntoFile(Datatoload):
    ListOfAllVol = Datatoload['Volumes']  # getting all instances


    print(len(ListOfAllVol))
    for vol in ListOfAllVol:
        ebs_vid = vol['VolumeId']
        ebs_snap_id = vol['SnapshotId']
        ebs_size = vol['Size']
        ebs_region = vol['AvailabilityZone'][:-1]
        ebs_state = vol['State']
        ebs_create_date = (vol['CreateTime']).date()
        ebs_volume_type = vol['VolumeType']
        ebs_iops = ''
        if 'Iops' in vol:
            ebs_iops = vol['Iops']
        ebs_instance_id = ''
        ebs_attachment_state = ''
        ebs_attach_time = None
        ebs_delete_on_termination = ''
        ebs_device = ''
        if 'Attachments' in vol:
            attachments = vol['Attachments']
            for attach in attachments:
                ebs_instance_id = attach['InstanceId']
                ebs_attachment_state = attach['State']
                ebs_attach_time = (attach['AttachTime']).date()
                ebs_delete_on_termination = attach['DeleteOnTermination']
                ebs_device = attach['Device']
        ebs_service = ''
        if 'Tags' in vol:
            tags = vol['Tags']
            for tag in tags:
                if tag['Key'] == 'Service':
                    ebs_service = tag['Value']

        cost = 0
        cost1 = 0
        cost2 = 0
        #print "Outer " + ebs_region + " " + ebs_volume_type
        for eachEbsrecord in CostingData:
            if ebs_region == eachEbsrecord.Region and ebs_volume_type == 'gp2':
                if eachEbsrecord.Storage_Cost_OR_IOPS == 'Storage_Cost':
                    cost = eachEbsrecord.GP2
            elif ebs_region == eachEbsrecord.Region and ebs_volume_type == 'io1':
                if eachEbsrecord.Storage_Cost_OR_IOPS == 'Storage_Cost':
                    cost1 = eachEbsrecord.IO1
                elif eachEbsrecord.Storage_Cost_OR_IOPS == 'IOPS':
                    cost2 = eachEbsrecord.IO1
                cost = cost1 + cost2
            elif ebs_region == eachEbsrecord.Region and ebs_volume_type == 'standard':
                if eachEbsrecord.Storage_Cost_OR_IOPS == 'Storage_Cost':
                    cost = eachEbsrecord.HDD_ST1

        insertEbsStaticWithCost(ebsDataWithCosting(ebs_vid,ebs_snap_id,ebs_size,ebs_iops,ebs_region,ebs_state,ebs_create_date,ebs_volume_type,ebs_instance_id,                                                   ebs_device, ebs_attachment_state, ebs_attach_time,
                                                   ebs_delete_on_termination, ebs_service, cost))



def gettingEbsCosting(ModelClassName):
    queryResult = session.query(ModelClassName).all()
    return queryResult


if __name__ == '__main__':
    start_time = timeit.default_timer()
    global session, CostingData
    engine = create_engine('mysql://root:root@110.110.110.164/cloud_assessment')
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    print "Creation table ebs_static_data"
    ebsDataWithCosting.__table__.drop()
    ebsDataWithCosting.__table__.create()
    print 'getting Data of ebs_cost'
    CostingData = gettingEbsCosting(ModelClassName=ebsCosting)

    EC2Client = boto3.client('ec2')

    allEc2Region = EC2Client.describe_regions()
    Ec2Region = allEc2Region['Regions']
    print "Loading data in database...."
    for eachRegion in Ec2Region:
        print(eachRegion['RegionName'])
        EC2 = boto3.client('ec2', region_name=eachRegion['RegionName'])
        DescEbs = EC2.describe_volumes()
        ToCheckForNextMarker(DescEbs)

    session.commit()
    elapsed = timeit.default_timer() - start_time
    print elapsed