from dbUtils import Base
from sqlalchemy import Column, String, BigInteger,Float


class CountByState(Base):
    __tablename__ = 'vw_countbystate'
    ec2_state = Column(String(50),primary_key=True)
    countid = Column(BigInteger)
    sumcost = Column(Float)


class CountVolByState(Base):
    __tablename__ = 'vw_countvolbystate'
    vol_state = Column(String(50),primary_key=True)
    countstate = Column(BigInteger)
