from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float,SmallInteger
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class snapshotModel(Base):
    __tablename__ = 'snapshot_static'

    snapshot_id = Column(String(50),primary_key=True)
    volume_id = Column(String(50))
    volume_size = Column(Integer)
    start_time = Column(Date)
    state = Column(String(50))
    progress = Column(String(50))
    encrypted = Column(String(10))
    owner_id = Column(String(50))
    description = Column(String(500))
    tag_Name = Column(String(20))
    tag_Domain = Column(String(20))
    tag_Source = Column(String(20))
    tag_Service = Column(String(20))
    tag_BackupType = Column(String(20))
    tag_Date = Column(String(20))

    def __init__(self, snapshot_id,volume_id,volume_size,start_time,state,progress,encrypted,owner_id,description,
                 tag_Name,tag_Domain ,tag_Source ,tag_Service,tag_BackupType,tag_Date):
        self.snapshot_id = snapshot_id
        self.volume_id = volume_id
        self.volume_size = volume_size
        self.start_time = start_time
        self.state = state
        self.progress = progress
        self.encrypted = encrypted
        self.owner_id = owner_id
        self.description = description
        self.tag_Name = tag_Name
        self.tag_Domain = tag_Domain
        self.tag_Source = tag_Source
        self.tag_Service = tag_Service
        self.tag_BackupType = tag_BackupType
        self.tag_Date = tag_Date



