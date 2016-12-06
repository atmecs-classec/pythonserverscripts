from sqlalchemy import Column, String,Date,Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class elasticCacheModel(Base):
    __tablename__ = 'elasticache_static'
    CacheClusterId = Column(String(50),primary_key=True)
    CacheClusterCreateTime = Column(Date)
    CacheClusterStatus = Column(String(50))
    CacheNodeType = Column(String(50))
    CacheSubnetGroupName = Column(String(50))
    ClientDownloadLandingPage = Column(String(250))
    Engine = Column(String(50))
    EngineVersion = Column(String(60))
    NumCacheNodes = Column(Integer)
    PreferredMaintenanceWindow = Column(String(20))
    PreferredAvailabilityZone = Column(String(90))
    ReplicationGroupId = Column(String(50))
    SnapshotRetentionLimit = Column(String(50))
    SnapshotWindow = Column(String(50))
    AutoMinorVersionUpgrade = Column(String(50))
    CacheParameterGroupName = Column(String(50))
    ParameterApplyStatus = Column(String(50))
    SecurityGroupId = Column(String(50))
    Status = Column(String(50))

    def __init__(self,CacheClusterId,CacheClusterCreateTime,CacheClusterStatus,CacheNodeType,CacheSubnetGroupName,
                 ClientDownloadLandingPage,Engine, EngineVersion,NumCacheNodes,PreferredMaintenanceWindow,
                 PreferredAvailabilityZone,ReplicationGroupId,SnapshotRetentionLimit, SnapshotWindow,
                 AutoMinorVersionUpgrade, CacheParameterGroupName, ParameterApplyStatus, SecurityGroupId, Status):
        self.CacheClusterId = CacheClusterId
        self.CacheClusterCreateTime = CacheClusterCreateTime
        self.CacheClusterStatus = CacheClusterStatus
        self.CacheNodeType = CacheNodeType
        self.CacheSubnetGroupName = CacheSubnetGroupName
        self.ClientDownloadLandingPage = ClientDownloadLandingPage
        self.Engine = Engine
        self.EngineVersion = EngineVersion
        self.NumCacheNodes = NumCacheNodes
        self.PreferredMaintenanceWindow = PreferredMaintenanceWindow
        self.PreferredAvailabilityZone = PreferredAvailabilityZone
        self.ReplicationGroupId = ReplicationGroupId
        self.SnapshotRetentionLimit = SnapshotRetentionLimit
        self.SnapshotWindow = SnapshotWindow
        self.AutoMinorVersionUpgrade = AutoMinorVersionUpgrade
        self.CacheParameterGroupName = CacheParameterGroupName
        self.ParameterApplyStatus = ParameterApplyStatus
        self.SecurityGroupId = SecurityGroupId
        self.Status = Status
