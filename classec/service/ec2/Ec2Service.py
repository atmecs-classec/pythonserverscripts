import timeit
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Ec2Schema import ec2DataWithCosting,Base, ec2Costing


#engine = create_engine('mysql://root:root@110.110.110.170/test_govind')

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
            ec2_EbsOptimized = 1 if instDetails['EbsOptimized'] else 0
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

#            query = "insert into "+tbName+" values ('"+ec_id+"','"+ec2_amiid+"','"+ec2_type+"','"+ec2_state+"','"+ec2_domain+"','"+ec2_env+"','"+ec2_name+"','"+ec2_region+"','"+str(ec2_launchdate)+"','"+ec2_monitoring+"','"+ec2_reserveid+"','"+ec2_subnet+"','"+ec2_hypervisor+"','"+ec2_vpc+"','"+str(ec2_EbsOptimized)+"','"+ec2_Architecture+"','"+ec2_platform+"')"
#            session.add(ec2DataWithCosting(ec_id, ec2_amiid, ec2_type,ec2_state, ec2_domain,ec2_env, ec2_name,
#                                            ec2_region, str(ec2_launchdate), ec2_monitoring, ec2_reserveid, ec2_subnet,
#                                            ec2_hypervisor,ec2_vpc,ec2_EbsOptimized, ec2_Architecture,ec2_platform))

            cost = 0
            for eachEc2record in CostingData:
                if ec2_type == eachEc2record.apiname and ec2_region[:-1] == eachEc2record.Region:
                    if ec2_platform == 'windows':
                        if ec2_reserveid != None:
                            cost = eachEc2record.cost_reserved_mswin_hourly
                        else:
                            cost = eachEc2record.cost_ondemand_mswin_hourly
                    else:
                        if ec2_reserveid != None:
                            cost = eachEc2record.cost_reserved_linux_hourly
                        else:
                            cost = eachEc2record.cost_ondemand_linux_hourly

                    session.add(ec2DataWithCosting(ec_id, ec2_amiid, ec2_type, ec2_state, ec2_domain, ec2_env, ec2_name,
                                                   ec2_region, str(ec2_launchdate), ec2_monitoring, ec2_reserveid,
                                                   ec2_subnet,ec2_hypervisor, ec2_vpc, ec2_EbsOptimized, ec2_Architecture,
                                                   ec2_platform,cost))



def gettingEc2Costing(ModelClassName=None):
    queryResult = session.query(ModelClassName).all()
    return queryResult


if __name__ == '__main__':
    start_time = timeit.default_timer()
    global session, CostingData
    engine = create_engine('mysql://root:root@110.110.110.164/cloud_assessment')
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    print "Creation table ebs_static_data"
    ec2DataWithCosting.__table__.drop()
    ec2DataWithCosting.__table__.create()

    print 'getting Data'
    CostingData = gettingEc2Costing(ModelClassName=ec2Costing)

    EC2Client = boto3.client('ec2')

    allEc2Region = EC2Client.describe_regions()
    Ec2Region = allEc2Region['Regions']

    for eachRegion in Ec2Region:
        print(eachRegion['RegionName'])
        EC2 = boto3.client('ec2', region_name=eachRegion['RegionName'])
        DescEC2 = EC2.describe_instances()
        ToCheckForNextMarker(DescEC2)

    session.commit()
    elapsed = timeit.default_timer() - start_time
    print elapsed
