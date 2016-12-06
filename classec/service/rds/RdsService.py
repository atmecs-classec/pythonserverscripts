#!/usr/bin/python
import timeit
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from RdsSchema import rdsDataWithCosting, rdsCosting, Base

def ToCheckForNextMarker(retrieveNextRDS):
    if 'Marker' in retrieveNextRDS:
        ToLoadDataOntoFile(retrieveNextRDS)
        withNextMarker = RDS.describe_db_instances(Marker=retrieveNextRDS['Marker'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextRDS)


def ToLoadDataOntoFile(Datatoload):
    # Initialize all the variable which will hold json values
    ListOfAllInstances = Datatoload['DBInstances']
    print len(ListOfAllInstances)
    for Instance in ListOfAllInstances:
        DBInstanceIdentifier = str(Instance['DBInstanceIdentifier']) if 'DBInstanceIdentifier' in Instance else ''
        DBInstanceClass = str(Instance['DBInstanceClass']) if 'DBInstanceClass' in Instance else ''
        AvailabilityZone = str(Instance['AvailabilityZone']) if 'AvailabilityZone' in Instance else ''
        DBName = str(Instance['DBName']) if 'DBName' in Instance else ''
        StorageType = str(Instance['StorageType']) if 'StorageType' in Instance else ''
        InstanceCreateTime = str((Instance['InstanceCreateTime']).date()) if 'InstanceCreateTime' in Instance else ''
        Engine = str(Instance['Engine']) if 'Engine' in Instance else ''
        MultiAZ = str(Instance['MultiAZ']) if 'MultiAZ' in Instance else ''
        BackupRetentionPeriod = str(Instance['BackupRetentionPeriod']) if 'BackupRetentionPeriod' in Instance else ''
        AllocatedStorage = str(Instance['AllocatedStorage']) if 'AllocatedStorage' in Instance else ''
        if 'ReadReplicaDBInstanceIdentifiers' in Instance:
            RDBIIList = Instance['ReadReplicaDBInstanceIdentifiers']
            ReadReplicaDBInstanceIdentifiers = ''
            for i in range(len(RDBIIList)):
               ReadReplicaDBInstanceIdentifiers += RDBIIList[i]+','
        else:
            ReadReplicaDBInstanceIdentifiers = ''
        EngineVersion = str(Instance['EngineVersion']) if 'EngineVersion' in Instance else ''

        for eachRdsrecord in CostingData:
            if DBInstanceClass == eachRdsrecord.API_Name and AvailabilityZone[:-1] == eachRdsrecord.Region:
                cost_On_Demand = 0.0
                cost_On_Reserved = 0.0
                if 'postgre' in Engine.lower():
                    cost_On_Demand = eachRdsrecord.PostgreSQL_On_Demand_cost
                    cost_On_Reserved = eachRdsrecord.PostgreSQL_Reserved_cost
                elif 'mysql' in Engine.lower():
                    cost_On_Demand = eachRdsrecord.MySQL_On_Demand_cost
                    cost_On_Reserved = eachRdsrecord.MySQL_Reserved_cost
                elif 'oracle' in Engine.lower():
                    cost_On_Demand = eachRdsrecord.Oracle_On_Demand_cost
                    cost_On_Reserved = eachRdsrecord.Oracle_Reserved_cost
                elif 'aurora' in Engine.lower():
                    cost_On_Demand = eachRdsrecord.Amazon_Aurora_On_Demand_cost
                    cost_On_Reserved = eachRdsrecord.Amazon_Aurora_Reserved_cost
                elif 'maria' in Engine.lower():
                    cost_On_Demand = eachRdsrecord.MariaDB_On_Demand_cost
                    cost_On_Reserved = eachRdsrecord.MariaDB_Reserved_cost
                elif 'sqlserver' in Engine.lower():
                    cost_On_Demand = eachRdsrecord.SQL_Server_On_Demand_cost
                    cost_On_Reserved = eachRdsrecord.SQL_Server_Reserved_cost

                session.add(rdsDataWithCosting(DBInstanceIdentifier ,DBInstanceClass ,StorageType ,Engine ,EngineVersion,
                                               DBName, MultiAZ, AllocatedStorage, BackupRetentionPeriod,
                                               AvailabilityZone ,InstanceCreateTime ,ReadReplicaDBInstanceIdentifiers,
                                               cost_On_Demand, cost_On_Reserved ))

def gettingEc2Costing(ModelClassName=None):
    queryResult = session.query(ModelClassName).all()
    return queryResult


if __name__ == '__main__':
    start_time = timeit.default_timer()
    global session, CostingData
    engine = create_engine('mysql://root:root@110.110.110.164/cloud_assessment')
#    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    print "Creating table rds_static_data"
    rdsDataWithCosting.__table__.drop()
    rdsDataWithCosting.__table__.create()

    print 'getting Data'
    CostingData = gettingEc2Costing(ModelClassName=rdsCosting)

    EC2Client = boto3.client('ec2')
    allRDSRegion = EC2Client.describe_regions()
    RDSRegion = allRDSRegion['Regions']

    for eachRegion in RDSRegion:
        print(eachRegion['RegionName'])
        RDS = boto3.client('rds', region_name=eachRegion['RegionName'])
        DescRDS = RDS.describe_db_instances()
        ToCheckForNextMarker(DescRDS)
    session.commit()
    elapsed = timeit.default_timer() - start_time
    print elapsed
