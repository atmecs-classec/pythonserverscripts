from sqlalchemy import Column, ForeignKey, Integer, String, Date, Float,SmallInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class elbModel(Base):
    __tablename__ = 'elb_static'
    LoadBalancerName = Column(String(50),primary_key=True)
    DNSName = Column(String(100))
    CanonicalHostedZoneName = Column(String(100))
    CanonicalHostedZoneNameID = Column(String(50))
    VPCId = Column(String(50))
    Scheme = Column(String(50))
    CreatedTime = Column(Date)
    AvailabilityZones = Column(String(60))
    Subnets = Column(String(60))
    InstanceId = Column(String(20))
    SecurityGroups = Column(String(90))

    def __init__(self,LoadBalancerName = None, DNSName = None, CanonicalHostedZoneName = None,
                 CanonicalHostedZoneNameID = None, VPCId = None, Scheme = None, CreatedTime = None, AvailabilityZones = None,
                 Subnets = None, InstanceId = None, SecurityGroups = None):
        self.LoadBalancerName = LoadBalancerName
        self.DNSName = DNSName
        self.CanonicalHostedZoneName = CanonicalHostedZoneName
        self.CanonicalHostedZoneNameID = CanonicalHostedZoneNameID
        self.VPCId = VPCId
        self.Scheme = Scheme
        self.CreatedTime = CreatedTime
        self.AvailabilityZones = AvailabilityZones
        self.Subnets = Subnets
        self.InstanceId = InstanceId
        self.SecurityGroups = SecurityGroups