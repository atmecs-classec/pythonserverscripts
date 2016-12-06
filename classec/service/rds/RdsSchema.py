from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float,SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class rdsDataWithCosting(Base):
    __tablename__ = 'rds_static_cost'
    DBInstanceIdentifier = Column(String(50), primary_key=True)
    DBInstanceClass = Column(String(50))
    StorageType = Column(String(50))
    Engine = Column(String(50))
    EngineVersion = Column(String(50))
    DBName = Column(String(50))
    MultiAZ = Column(String(50))
    AllocatedStorage = Column(String(50))
    BackupRetentionPeriod = Column(String(50))
    AvailabilityZone = Column(String(50))
    InstanceCreateTime = Column(Date)
    ReadReplicaDBInstanceIdentifiers = Column(String(250))
    cost_On_Demand = Column(Float)
    cost_On_Reserved = Column(Float)

    def __init__(self,DBInstanceIdentifier = None,DBInstanceClass = None,StorageType = None,Engine = None,
                 EngineVersion = None,DBName = None,MultiAZ = None,AllocatedStorage = None,BackupRetentionPeriod = None,
                 AvailabilityZone = None,InstanceCreateTime = None,ReadReplicaDBInstanceIdentifiers = None,
                 cost_On_Demand = None, cost_On_Reserved = None):
        self.DBInstanceIdentifier = DBInstanceIdentifier
        self.DBInstanceClass = DBInstanceClass
        self.StorageType = StorageType
        self.Engine = Engine
        self.EngineVersion = EngineVersion
        self.DBName = DBName
        self.MultiAZ = MultiAZ
        self.AllocatedStorage = AllocatedStorage
        self.BackupRetentionPeriod = BackupRetentionPeriod
        self.AvailabilityZone = AvailabilityZone
        self.InstanceCreateTime = InstanceCreateTime
        self.ReadReplicaDBInstanceIdentifiers = ReadReplicaDBInstanceIdentifiers
        self.cost_On_Demand = cost_On_Demand
        self.cost_On_Reserved = cost_On_Reserved

class rdsCosting(Base):
    __tablename__= 'rds_costing2016_11_15'
    Name = Column(String(30))
    API_Name = Column(String(30),primary_key=True)
    Memory = Column(String(30))
    Storage = Column(String(30))
    vCPUs = Column(String(30))
    Network_Performance = Column(String(30))
    Arch = Column(String(30))
    Processor = Column(String(50))
    Amazon_Aurora_On_Demand_cost = Column(Float)
    Amazon_Aurora_Reserved_cost = Column(Float)
    MariaDB_On_Demand_cost = Column(Float)
    MariaDB_Reserved_cost = Column(Float)
    MySQL_On_Demand_cost = Column(Float)
    MySQL_Reserved_cost = Column(Float)
    Oracle_On_Demand_cost = Column(Float)
    Oracle_Reserved_cost = Column(Float)
    PostgreSQL_On_Demand_cost = Column(Float)
    PostgreSQL_Reserved_cost = Column(Float)
    SQL_Server_On_Demand_cost = Column(Float)
    SQL_Server_Reserved_cost = Column(Float)
    Region = Column(String(30),primary_key=True)


