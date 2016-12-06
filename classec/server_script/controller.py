import dbConn,service
from flask import Flask,request

app = Flask(__name__)


@app.route('/')
def hello():
    return "Welcome to the world of cloud"


@app.route('/ec2stopped')
def ec2stoppedroute():
    ep = dbConn.getEc2StoppedData()
    return str(ep)


@app.route('/ec2')
def ec2route():
    ep = dbConn.getEc2Data()
    return str(ep)


@app.route('/dbcountstate')
def countByStateRoute():
    res = dbConn.getCountByState()
    return str(res)


@app.route('/dbcountvolstate')
def countVolStateRoute():
    res = dbConn.getCountVolstate()
    return str(res)


@app.route('/dashboard')
def dashboardRoute():
    res = dbConn.getDashBoard()
    return str(res)

@app.route('/oorequest',methods=['POST'])
def getPostValues():
    instanceId = request.form['instanceId']
    region = request.form['region']
    action = request.form['action']
    return service.sendRequestToOO(instanceId,action,region)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9001)
