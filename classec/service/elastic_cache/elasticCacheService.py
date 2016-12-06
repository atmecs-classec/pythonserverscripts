#!/usr/bin/python
import boto3

from sqlalchemy import create_engine
import timeit
from sqlalchemy.orm import sessionmaker
from elasticCacheSchema import Base,elasticCacheModel

def ToCheckForNextMarker(retrieveNextElastiCache):
    if 'Marker' in retrieveNextElastiCache:
        ToLoadDataOntoFile(retrieveNextElastiCache)
        withNextMarker = ElastiCache.describe_cache_clusters(Marker=retrieveNextElastiCache['Marker'])
        ToCheckForNextMarker(withNextMarker)
    else:
        ToLoadDataOntoFile(retrieveNextElastiCache)


def ToLoadDataOntoFile(Datatoload):
    # Initialize all the variable which will hold json values
    ListOfAllElastiCacheClusters = Datatoload['CacheClusters']  # getting all elasticache
    counter = 0
    recordBuilder = list()
    print'length of all elasticache ' + str(len(ListOfAllElastiCacheClusters))
    for ElastiCache in ListOfAllElastiCacheClusters:
        if 'CacheClusterId' in ElastiCache:
            CacheClusterId = str(ElastiCache['CacheClusterId'])
        else:
            CacheClusterId = ''

        if 'CacheClusterCreateTime' in ElastiCache:
            CacheClusterCreateTime = str((ElastiCache['CacheClusterCreateTime']).date())
        else:
            CacheClusterCreateTime = ''

        if 'CacheClusterStatus' in ElastiCache:
            CacheClusterStatus = str(ElastiCache['CacheClusterStatus'])
        else:
            CacheClusterStatus = ''

        if 'CacheNodeType' in ElastiCache:
            CacheNodeType = str(ElastiCache['CacheNodeType'])
        else:
            CacheNodeType = ''

        if 'CacheSubnetGroupName' in ElastiCache:
            CacheSubnetGroupName = str(ElastiCache['CacheSubnetGroupName'])
        else:
            CacheSubnetGroupName = ''
        if 'ClientDownloadLandingPage' in ElastiCache:
            ClientDownloadLandingPage = str(ElastiCache['ClientDownloadLandingPage'])
        else:
            ClientDownloadLandingPage = ''

        if 'Engine' in ElastiCache:
            Engine = str(ElastiCache['Engine'])
        else:
            Engine = ''

        if 'EngineVersion' in ElastiCache:
            EngineVersion = str(ElastiCache['EngineVersion'])
        else:
            EngineVersion = ''

        if 'NumCacheNodes' in ElastiCache:
            NumCacheNodes = str(ElastiCache['NumCacheNodes'])
        else:
            NumCacheNodes = ''

        if 'PreferredMaintenanceWindow' in ElastiCache:
            PreferredMaintenanceWindow = str(ElastiCache['PreferredMaintenanceWindow'])
        else:
            PreferredMaintenanceWindow = ''

        if 'PreferredAvailabilityZone' in ElastiCache:
            PreferredAvailabilityZone = ElastiCache['PreferredAvailabilityZone']
        else:
            PreferredAvailabilityZone = ''

        if 'ReplicationGroupId' in ElastiCache:
            ReplicationGroupId = str(ElastiCache['ReplicationGroupId'])
        else:
            ReplicationGroupId = ''

        if 'SnapshotRetentionLimit' in ElastiCache:
            SnapshotRetentionLimit = str(ElastiCache['SnapshotRetentionLimit'])
        else:
            SnapshotRetentionLimit = ''

        if 'SnapshotWindow' in ElastiCache:
            SnapshotWindow = str(ElastiCache['SnapshotWindow'])
        else:
            SnapshotWindow = ''

        if 'AutoMinorVersionUpgrade' in ElastiCache:
            AutoMinorVersionUpgrade = str(ElastiCache['AutoMinorVersionUpgrade'])
        else:
            AutoMinorVersionUpgrade = ''

        CacheParameterGroupName = ''
        ParameterApplyStatus = ''
        if 'CacheParameterGroup' in ElastiCache:
            ParameterGroupList = ElastiCache['CacheParameterGroup']
            for key, value in ParameterGroupList.iteritems():
                if 'CacheParameterGroupName' == key:
                    CacheParameterGroupName = value
                if 'ParameterApplyStatus' == key:
                    ParameterApplyStatus = value

        SecurityGroupId = ''
        Status = ''
        if 'SecurityGroups' in ElastiCache:
            SecurityGroupsList = ElastiCache['SecurityGroups']
            for k in range(len(SecurityGroupsList)):
                for key, value in SecurityGroupsList[k].iteritems():
                    if 'SecurityGroupId' == key:
                        SecurityGroupId = value
                    if 'Status' == key:
                        Status = value

        counter = counter + 1
        record = elasticCacheModel(CacheClusterId,CacheClusterCreateTime,CacheClusterStatus,CacheNodeType,
                                      CacheSubnetGroupName,ClientDownloadLandingPage,Engine, EngineVersion,NumCacheNodes,
                                      PreferredMaintenanceWindow,PreferredAvailabilityZone,ReplicationGroupId,
                                      SnapshotRetentionLimit, SnapshotWindow, AutoMinorVersionUpgrade,
                                      CacheParameterGroupName, ParameterApplyStatus, SecurityGroupId, Status)
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
    #    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    if engine.dialect.has_table(engine, elasticCacheModel.__tablename__):
        elasticCacheModel.__table__.drop()
    elasticCacheModel.__table__.create()

    EC2Client = boto3.client('ec2')
    allElastiCacheRegion = EC2Client.describe_regions()
    ElastiCacheRegion = allElastiCacheRegion['Regions']

    for eachRegion in ElastiCacheRegion:
        print(eachRegion['RegionName'])
        ElastiCache = boto3.client('elasticache', region_name=eachRegion['RegionName'])
        DescElastiCache = ElastiCache.describe_cache_clusters()
        ToCheckForNextMarker(DescElastiCache)
    session.commit()
    elapsed = timeit.default_timer() - start_time
    print elapsed
