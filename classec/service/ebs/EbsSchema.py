from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float,SmallInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class ebsDataWithCosting(Base):
    __tablename__ = 'ebs_static_cost'
    ebs_volumeid = Column(String(50),primary_key=True)
    ebs_snap_id = Column(String(50))
    ebs_size = Column(String(50))
    ebs_iops = Column(String(10))
    ebs_region = Column(String(50))
    ebs_state = Column(String(50))
    ebs_create_date = Column(Date)
    ebs_volume_type = Column(String(50))
    ebs_instance_id = Column(String(20))
    ebs_device = Column(String(50))
    ebs_attachment_state = Column(String(50))
    ebs_attach_time = Column(Date)
    ebs_delete_on_termination = Column(String(50))
    ebs_service = Column(String(50))
    cost = Column(Float)


    def __init__(self, ebs_volumeid, ebs_snap_id, ebs_size, ebs_iops, ebs_region, ebs_state, ebs_create_date,
                 ebs_volume_type, ebs_instance_id, ebs_device, ebs_attachment_state, ebs_attach_time, ebs_delete_on_termination,
                 ebs_service, cost):
        self.ebs_volumeid = ebs_volumeid
        self.ebs_snap_id = ebs_snap_id
        self.ebs_size = ebs_size
        self.ebs_iops = ebs_iops
        self.ebs_region = ebs_region
        self.ebs_state = ebs_state
        self.ebs_create_date = ebs_create_date
        self.ebs_volume_type = ebs_volume_type
        self.ebs_instance_id = ebs_instance_id
        self.ebs_device = ebs_device
        self.ebs_attachment_state = ebs_attachment_state
        self.ebs_attach_time = ebs_attach_time
        self.ebs_delete_on_termination = ebs_delete_on_termination
        self.ebs_service = ebs_service
        self.cost = cost

class ebsCosting(Base):
    __tablename__= 'ebs_cost'
    Region = Column(String(30),primary_key=True)
    GP2 = Column(Float)
    IO1 = Column(Float)
    HDD_ST1 = Column(Float)
    HDD_SC1 = Column(Float)
    Snapshot = Column(Float)
    Storage_Cost_OR_IOPS = Column(String(20),primary_key=True)


