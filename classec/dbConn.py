from ec2Model import Ec2View
from awsCountModel import CountByState ,CountVolByState
from dbUtils import Session, serialize_label, FormattingOutputInDict

session = Session()


def getEc2StoppedData():
    result = session.query(Ec2View).filter(Ec2View.ec2_state == 'stopped').all()
    return serialize_label(result)


def getEc2Data():
    result = session.query(Ec2View).all()
    return serialize_label(result)


def getCountByState():
    result = session.query(CountByState).all()
    return serialize_label(result)


def getCountVolstate():
    result = session.query(CountVolByState).all()
    return serialize_label(result)


def getDashBoard():
    result = session.execute('call sp_dashboard()')
    return  FormattingOutputInDict(result.keys(),result.fetchall())

