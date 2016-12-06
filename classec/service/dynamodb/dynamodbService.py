#!/usr/bin/python
import boto3
import timeit
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dynamodbSchema import Base,dynamodbModel


def ToCheckForNextTable(AllTables):
    if 'LastEvaluatedTableName' in AllTables :
        TableNames = AllTables['TableNames']
        for i in range(len(TableNames)):
            TableName = str(TableNames[i])
            TableData = DynamoDb.describe_table(TableName = TableName)
            loadData(TableData)


def loadData(AllTableData):
    # Initialize all the variable which will hold json values
    counter = 0
    recordBuilder = list()
    print'length of table ' + str(len(AllTableData['Table']))
    table = AllTableData['Table']
    TableName = ''
    TableStatus = ''
    TableSizeBytes = ''
    TableArn = ''
    CreationDateTime = ''
    ItemCount = ''
    LastIncreaseDateTime = ''
    LastDecreaseDateTime = ''
    NumberOfDecreasesToday = ''
    ReadCapacityUnits = ''
    WriteCapacityUnits = ''

    for key, value in table.iteritems():
        if 'TableName' == key:
            TableName = str(value)

        if 'TableStatus' == key:
            TableStatus = str(value)

        if 'TableSizeBytes' == key:
            TableSizeBytes = str(value)

        if 'TableArn' == key:
            TableArn = str(value)

        if 'CreationDateTime' == key:
            CreationDateTime = str(value)

        if 'ItemCount' == key:
            ItemCount = str(value)

        if 'ProvisionedThroughput' == key:
            for i, j in value.iteritems():
                if i == 'LastIncreaseDateTime':
                    LastIncreaseDateTime = str(j)

                elif i == 'LastDecreaseDateTime':
                    LastDecreaseDateTime = str(j)

                elif i == 'NumberOfDecreasesToday':
                    NumberOfDecreasesToday = str(j)

                elif i == 'ReadCapacityUnits':
                    ReadCapacityUnits = str(j)

                elif i == 'WriteCapacityUnits':
                    WriteCapacityUnits = str(j)
                else:
                    print ''

        counter = counter + 1
        record = dynamodbModel(TableName,TableStatus ,TableArn ,TableSizeBytes ,ItemCount ,CreationDateTime ,
                                  LastIncreaseDateTime ,LastDecreaseDateTime ,NumberOfDecreasesToday ,ReadCapacityUnits,
                                  WriteCapacityUnits)
        recordBuilder.append(record)

        if 500 == counter:
            session.bulk_save_objects(recordBuilder)
            session.commit()
            counter = 0
            recordBuilder = []

    session.bulk_save_objects(recordBuilder)
    session.commit()


if __name__ == '__main__':
    start_time = timeit.default_timer()
    global session
    engine = create_engine('mysql://root:root@110.110.110.164/cloud_assessment')
    Base.metadata.bind = engine
    DBsession = sessionmaker(bind=engine)
    session = DBsession()

    print "Creating table elb_static_data"
    if engine.dialect.has_table(engine, dynamodbModel.__tablename__):
        dynamodbModel.__table__.drop()
    dynamodbModel.__table__.create()


    EC2Client = boto3.client('ec2')
    allELBRegion = EC2Client.describe_regions()
    ELBRegion = allELBRegion['Regions']

    for eachRegion in ELBRegion:
        print(eachRegion['RegionName'])
        DynamoDb = boto3.client('dynamodb', region_name=eachRegion['RegionName'])
        ListOfAllTable = DynamoDb.list_tables()
        ToCheckForNextTable(ListOfAllTable)
    session.commit()
    elapsed = timeit.default_timer() - start_time
    print elapsed