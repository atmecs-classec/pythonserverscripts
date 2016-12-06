#!/usr/bin/python
import timeit
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from elbSchema import Base,elbModel

def ToCheckForNextMarker(retrieveNextELB):
    if 'Marker' in retrieveNextELB:
        ToLoadDataOntoFile(retrieveNextELB)
        withNextMarker = ELB.describe_load_balancers(Marker=retrieveNextELB['Marker'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextELB)


def ToLoadDataOntoFile(Datatoload):
    # Initialize all the variable which will hold json values
    ListOfAllLoadBalancers = Datatoload['LoadBalancerDescriptions']  # getting all LoadBalancer
    print len(ListOfAllLoadBalancers)
    counter = 0
    recordBuilder = list()
    for LoadBalancer in ListOfAllLoadBalancers:

        LoadBalancerName = str(LoadBalancer['LoadBalancerName']) if 'LoadBalancerName' in LoadBalancer else ''
        DNSName = str(LoadBalancer['DNSName']) if 'DNSName' in LoadBalancer else ''
        VPCId = str(LoadBalancer['VPCId']) if 'VPCId' in LoadBalancer else ''
        CanonicalHostedZoneName = str(LoadBalancer['CanonicalHostedZoneName']) if 'CanonicalHostedZoneName' in LoadBalancer else ''
        CreatedTime = str((LoadBalancer['CreatedTime']).date()) if 'CreatedTime' in LoadBalancer else ''
        CanonicalHostedZoneNameID = str(LoadBalancer['CanonicalHostedZoneNameID']) if 'CanonicalHostedZoneNameID' in LoadBalancer else ''
        Scheme = str(LoadBalancer['Scheme']) if 'Scheme' in LoadBalancer else ''

        AvailabilityZones = ''
        if 'AvailabilityZones' in LoadBalancer:
            zonelist = LoadBalancer['AvailabilityZones']
            # print zonelist
            for i in range(len(zonelist)):
                AvailabilityZones += zonelist[i] + ' |'

        Subnets = ''
        if 'Subnets' in LoadBalancer:
            Subnetlist = LoadBalancer['Subnets']
            for ii in range(len(Subnetlist)):
                Subnets += Subnetlist[ii] + ' |'

        InstanceId = ''
        if 'Instances' in LoadBalancer:
            Instancelist = LoadBalancer['Instances']
            for j in range(len(Instancelist)):
                for key, value in Instancelist[j].iteritems():
                    InstanceId = value

        SecurityGroups = ''
        if 'SecurityGroups' in LoadBalancer:
            list = LoadBalancer['SecurityGroups']
            for k in range(len(list)):
                SecurityGroups += list[k] + ' |'

        counter = counter + 1
        record = elbModel(LoadBalancerName, DNSName, CanonicalHostedZoneName, CanonicalHostedZoneNameID, VPCId, Scheme,
                    CreatedTime, AvailabilityZones,Subnets, InstanceId, SecurityGroups)
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
    #    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    print "Creating table elb_static_data"
    if engine.dialect.has_table(engine, elbModel.__tablename__):
        elbModel.__table__.drop()
    elbModel.__table__.create()

    EC2Client = boto3.client('ec2')
    allELBRegion = EC2Client.describe_regions()
    ELBRegion = allELBRegion['Regions']

    for eachRegion in ELBRegion:
        print(eachRegion['RegionName'])
        ELB = boto3.client('elb', region_name=eachRegion['RegionName'])
        DescELB = ELB.describe_load_balancers()
        ToCheckForNextMarker(DescELB)
    session.commit()
    elapsed = timeit.default_timer() - start_time
    print elapsed

