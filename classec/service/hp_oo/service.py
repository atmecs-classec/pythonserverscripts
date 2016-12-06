import requests,json

def responceFromOO(url,uuid,instanceId,region):
    status = ""
    try:

        items = {"uuid": uuid,
                 "inputs":
                     {
                         "instanceId": instanceId,
                         "accessKeyId": "AKIAI7O5RSG5I4DJE7PA",
                         "accessKey": "JWdRgUi5PGmnvzkiSKFXruc/EXFm/uowWQfpMFwQ",
                         "serviceEndpoint": "ec2."+region+".amazonaws.com"
                     }
                 }
        params = json.dumps(items).encode('utf8')
        s = requests.session()
        print "Get Request"
        s.auth = ('atmecs', 'atmecs')
        r = s.get(url, verify=False)
        resp = s.get(url, verify=False)
        s.headers.update({'X-CSRF-TOKEN': resp.headers['X-CSRF-TOKEN']})
        s.headers.update({'Content-Type' : 'application/json'})

        fresp = s.post(url, data=params, verify=False)
        if fresp.status_code == 201 or fresp.status_code == 200:
            status = "Success"
        else:
            status = fresp.content

    except Exception as e:
        print "Exception"
        status = str(e)
    return status


def sendRequestToOO(instanceId,action,region):
    url = "https://110.110.110.198:8443/oo/rest/v1/executions"

    if action == 'stop':
	    uuid = "d5f9bfbb-0633-4c5f-8af1-0db25501e00d"
	    return responceFromOO(url,uuid,instanceId,region)
    elif action == 'terminate':
	    uuid = "1903f85c-5bda-4637-b1f3-140b7bf5182a"
	    return responceFromOO(url,uuid,instanceId,region)

   
