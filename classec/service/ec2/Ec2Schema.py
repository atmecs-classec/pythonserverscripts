from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float,SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class ec2DataWithCosting(Base):
    __tablename__ = 'ec2_static_cost'
    ec_id = Column(String(50), primary_key=True)
    ec2_amiid = Column(String(50))
    ec2_type = Column(String(50))
    ec2_state = Column(String(50))
    ec2_domain = Column(String(50))
    ec2_env = Column(String(50))
    ec2_name = Column(String(200))
    ec2_region = Column(String(50))
    ec2_launchdate = Column(Date)
    ec2_monitoring = Column(String(50))
    ec2_reserveid = Column(String(50))
    ec2_subnet = Column(String(50))
    ec2_hypervisor = Column(String(50))
    ec2_vpc = Column(String(50))
    ec2_EbsOptimized = Column(SmallInteger)
    ec2_Architecture = Column(String(50))
    ec2_platform = Column(String(30))
    cost = Column(Float)

    def __init__(self,ec_id = None, ec2_amiid = None, ec2_type = None,ec2_state = None, ec2_domain = None,
                 ec2_env = None,ec2_name = None,ec2_region = None,ec2_launchdate = None,ec2_monitoring = None,
                 ec2_reserveid = None,ec2_subnet = None,ec2_hypervisor = None,ec2_vpc = None,ec2_EbsOptimized=None,
                 ec2_Architecture=None,ec2_platform=None,cost=None):
        self.ec_id = ec_id
        self.ec2_amiid = ec2_amiid
        self.ec2_type = ec2_type
        self.ec2_state = ec2_state
        self.ec2_domain = ec2_domain
        self.ec2_env = ec2_env
        self.ec2_name = ec2_name
        self.ec2_region = ec2_region
        self.ec2_launchdate = ec2_launchdate
        self.ec2_monitoring = ec2_monitoring
        self.ec2_reserveid = ec2_reserveid
        self.ec2_subnet = ec2_subnet
        self.ec2_hypervisor = ec2_hypervisor
        self.ec2_vpc = ec2_vpc
        self.ec2_EbsOptimized = ec2_EbsOptimized
        self.ec2_Architecture = ec2_Architecture
        self.ec2_platform = ec2_platform
        self.cost = cost


class ec2Costing(Base):
    __tablename__= 'ec2_costing2016_11_14'
    name = Column(String(50))
    apiname = Column(String(20),primary_key=True)
    memory = Column(String(10))
    computeunits = Column(String(10))
    vcpus = Column(String(10))
    storage = Column(String(30))
    architecture = Column(String(10))
    networkperf = Column(String(20))
    ebs_max_bandwidth = Column(String(10))
    vpc_only = Column(String(10))
    cost_ondemand_linux_hourly = Column(Float)
    cost_reserved_linux_hourly = Column(Float)
    cost_ondemand_mswin_hourly = Column(Float)
    cost_reserved_mswin_hourly = Column(Float)
    Region = Column(String(10),primary_key=True)


