from sqlalchemy import Column, String, Date, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class dynamodbModel(Base):
    __tablename__ = 'dynamodb_static'
    id = Column(Integer,primary_key=True,autoincrement=True)
    TableName = Column(String(50),primary_key=True)
    TableStatus = Column(String(50))
    TableArn = Column(String(150))
    TableSizeBytes = Column(String(50))
    ItemCount = Column(String(50))
    CreationDateTime = Column(DateTime)
    LastIncreaseDateTime = Column(DateTime)
    LastDecreaseDateTime = Column(DateTime)
    NumberOfDecreasesToday = Column(String(50))
    ReadCapacityUnits = Column(String(60))
    WriteCapacityUnits = Column(String(50))

    def __init__(self,TableName = None,TableStatus = None,TableArn = None,TableSizeBytes = None,ItemCount = None,
                 CreationDateTime = None,LastIncreaseDateTime= None,LastDecreaseDateTime = None,
                 NumberOfDecreasesToday = None,ReadCapacityUnits= None,WriteCapacityUnits= None):
        self.TableName = TableName
        self.TableStatus = TableStatus
        self.TableArn = TableArn
        self.TableSizeBytes = TableSizeBytes
        self.ItemCount = ItemCount
        self.CreationDateTime = CreationDateTime
        self.LastIncreaseDateTime = LastIncreaseDateTime
        self.LastDecreaseDateTime = LastDecreaseDateTime
        self.NumberOfDecreasesToday = NumberOfDecreasesToday
        self.ReadCapacityUnits = ReadCapacityUnits
        self.WriteCapacityUnits = WriteCapacityUnits
