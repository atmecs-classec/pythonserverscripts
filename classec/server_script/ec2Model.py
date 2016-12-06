from dbUtils import Base
from sqlalchemy import Column, String, Float


class Ec2View(Base):
    __tablename__ = 'vw_ec2withcost'
    ec_id = Column(String(50), primary_key=True)
    ec2_name = Column(String(50))
    ec2_domain = Column(String(50))
    ec2_state = Column(String(50))
    ec2_env = Column(String(50))
    ec2_type = Column(String(50))
    Ec2_platform = Column(String(30))
    cost = Column(Float)


