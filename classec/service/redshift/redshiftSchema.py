from sqlalchemy import Column, String, SmallInteger, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class redshiftModel(Base):
    __tablename__ = 'redshift_static'
    ClusterID = Column(String(100),primary_key=True)
    allowVersionUpgrade = Column(SmallInteger)
    automatedSnapshotRetentionPeriod = Column(Integer)
    availabilityZone = Column(String(20))
    clusterCreateTime = Column(DateTime)
    clusterRevisionNumber = Column(Integer)
    clusterStatus = Column(String(10))
    clusterSubnetGroupName = Column(String(50))
    clusterVersion = Column(String(10))
    dbName = Column(String(20))
    encrypted = Column(SmallInteger)
    enhancedVpcRouting = Column(SmallInteger)
    nodeType = Column(String(20))
    numberOfNodes = Column(Integer)
    preferredMaintenanceWindow = Column(String(20))
    vpcId = Column(String(20))
    nodeRole = Column(String(150))
    parameterApplyStatus = Column(String(50))
    tags_Name = Column(String(30))
    tags_Env = Column(String(10))
    tags_Brand = Column(String(10))
    tags_Service = Column(String(20))
    tags_Segment = Column(String(10))
    tags_Domain = Column(String(20))
    tags_Role = Column(String(10))
    tags_Country = Column(String(10))

    def __init__(self,ClusterID= None,allowVersionUpgrade= None,automatedSnapshotRetentionPeriod= None,
                 availabilityZone = None,clusterCreateTime= None,clusterRevisionNumber= None,clusterStatus= None,
                 clusterSubnetGroupName= None,clusterVersion= None, dbName= None, encrypted= None,enhancedVpcRouting= None,
                 nodeType= None, numberOfNodes= None,preferredMaintenanceWindow= None,vpcId= None,nodeRole= None,
                 parameterApplyStatus= None,tags_Name= None, tags_Env= None, tags_Brand= None, tags_Service= None,
                 tags_Segment= None, tags_Domain= None, tags_Role= None, tags_Country = None):
        self.ClusterID = ClusterID
        self.allowVersionUpgrade = allowVersionUpgrade
        self.automatedSnapshotRetentionPeriod = automatedSnapshotRetentionPeriod
        self.availabilityZone = availabilityZone
        self.clusterCreateTime = clusterCreateTime
        self.clusterRevisionNumber = clusterRevisionNumber
        self.clusterStatus = clusterStatus
        self.clusterSubnetGroupName = clusterSubnetGroupName
        self.clusterVersion = clusterVersion
        self.dbName = dbName
        self.encrypted = encrypted
        self.enhancedVpcRouting = enhancedVpcRouting
        self.nodeType = nodeType
        self.numberOfNodes = numberOfNodes
        self.preferredMaintenanceWindow = preferredMaintenanceWindow
        self.vpcId = vpcId
        self.nodeRole = nodeRole
        self.parameterApplyStatus = parameterApplyStatus
        self.tags_Name = tags_Name
        self.tags_Env = tags_Env
        self.tags_Brand = tags_Brand
        self.tags_Service = tags_Service
        self.tags_Segment = tags_Segment
        self.tags_Domain = tags_Domain
        self.tags_Role = tags_Role
        self.tags_Country = tags_Country
