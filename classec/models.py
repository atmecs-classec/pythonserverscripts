from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

BASE = declarative_base()
engine = create_engine('mysql://root:root@110.110.110.170/cloud_assessment', echo=False)

class Ec2Static(BASE):
    __tablename__ = 'ec2_static'
    ec_id = Column(String(50), primary_key=True)
    ec2_amiid = Column(String(50))
    ec2_type = Column(String(50))
    ec2_state = Column(String(50))
    ec2_domain = Column(String(50))
    ec2_env = Column(String(50))
    ec2_name = Column(String(50))
    ec2_region = Column(String(50))
    ec2_launchdate = Column(Date)
    ec2_monitoring = Column(String(50))
    ec2_reserveid = Column(String(50))
    ec2_subnet = Column(String(50))
    ec2_hypervisor = Column(String(50))
    ec2_vpc = Column(String(50))
    ec2_EbsOptimized = Column(Integer)
    ec2_Architecture = Column(String(50))
    ec2_platform = Column(String(30))
   

def loadSession():
    metadata = BASE.metadata
    Session = sessionmaker(bind = engine)
    session = Session()
    return session
    
def ec2Data():
    sess = loadSession()
    res = sess.query(Ec2Static).all()
    return res
