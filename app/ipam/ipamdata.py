import json, requests
from urllib.parse import urljoin

from datetime import datetime as dt
from datetime import timedelta

from flask import render_template, current_app
from app.utils.email import send_email

#print("IPAM",current_app.config['IPAM_HOST'])
ipam_host  = current_app.config['IPAM_HOST']
ipam_port = current_app.config['IPAM_PORT']
ipam_maxips = int(current_app.config['IPAM_MAXIPS'])

ipam_api = str("http://")+str(ipam_host)+str(":")+str(ipam_port)

print("IPAM API",ipam_api)
print("MAX IPs",current_app.config['IPAM_MAXIPS'])

# Confirm User on IPAM
def IpamConfirm(userId):
    print("IPAM: User Confirm")
    api_userconfirm = ipam_api + '/users/' + userId + '/confirm'
    headers = {'content-type': 'application/json' }
    r = requests.get(url=api_userconfirm)		#, headers=headers)
    jsondata = json.loads(r.text)
    #authtoken = jsondata['token']
    if r.status_code != 202:
        response = {
            'status':'failed',
            'data' : jsondata
        }
        return json.dumps(response)
    else:
        #ipamjson = IpamConfirm(jsondata['_id'])
        response = {
            'status':'success',
            'data' : jsondata
        }
        return json.dumps(response)        
    

# Register User on IPAM
def IpamRegister(payload):
    print("IPAM: User Create/Register")
    api_usercreate = ipam_api + '/users/create'
    headers = {'content-type': 'application/json' }
    r = requests.post(url=api_usercreate, data=json.dumps(payload), headers=headers)
    jsondata = json.loads(r.text)
    if r.status_code == 201:
        ipamjson = IpamConfirm(jsondata['_id'])
        response = {
            'status':'success',
            'data' : ipamjson
        }
        return json.dumps(response)
    else:
        
        response = {
            'status':'failed',
            'data' : jsondata
        }
        return json.dumps(response)

# Login endpoint
#@ipam_bp.route('/login', methods=['GET','POST'])		
def IpamLogin(payload):
    print("IPAM: User Login")
    api_userlogin = ipam_api + '/users/login'
    headers = {'content-type': 'application/json' }
    r = requests.patch(url=api_userlogin, data=json.dumps(payload), headers=headers)
    jsondata = json.loads(r.text)
    #authtoken = jsondata['token']
    #userid = jsondata['user']['_id']
    if r.status_code == 202:
        response = {
            'status':'success',
            'data' : jsondata
        }
        return json.dumps(response)
    else:
        #ipamjson = IpamConfirm(jsondata['_id'])
        response = {
            'status':'failed',
            'data' : jsondata
        }
        return json.dumps(response) 


def AddressCheckout(payload):
    print("IPAM: Address Checkout")
    #reqdata = json.loads(payload)
    
    network = payload['network']
    fqdn = payload['fqdn']
    token = payload['ipam_token']
    ipcount = int(payload['ipcount'])
    
    api_addresscheckout = str(ipam_api) +str(r'/addresses/checkout?network=') +str(network)+ str(r'&fqdn=') +str(fqdn)
    
    print(api_addresscheckout)
    print("Access Token",token)
    print("IPs Requested",ipcount)
    headers = {'content-type': 'application/json','Authorization': 'Bearer ' + token }
    
    '''
    if ipcount > 0 and ipcount < ipam_maxips:
        ipamResult = []
        for _ in range(ipcount):
            r = requests.get(url=api_addresscheckout, headers=headers)
            
            jsondata = json.loads(r.text)
            
            addressId = jsondata['addresses']['_id']
            address = jsondata['addresses']['address']
            #print("IP Issued",address)
            #print("")
            
            
            ipamItem = {
                'fqdn': fqdn,
                'ipaddress': address,		
                'network': network,
                'ipaddressid': addressId
            }
            ipamResult.append(ipamItem)
    
        return ipamResult
        
    else:
        response = {
            'ok' : False,
            'message' : 'Invalid ip count requested, max 10 ips.'
        }
        return response
    '''
    response = {
        'ok' : True,
        'message' : 'Here\'s your IP\'s.'
    }    
    return response 

def IpamConnect(payload):
    ipamCreds = {
        'emailAddress': payload.email, 
        'password': payload.ipam
    }
    ipamResponse = IpamLogin(payload)
    if ipamResponse['status'] == "success":
        ipamtoken = ipamResponse['data']['token']
        ipamconnect = {
            'status': 'success',
            'message' : 'Connected to IPAM.',
            'data': ipamtoken
        }            
        return json.dumps(ipamconnect)
    else:
        if ipamResponse['data']['error'] == "User Not Found":
            ipamReg = {
                'userName': payload.username, 
                'emailAddress': payload.email, 
                'firstname': payload.firstname, 
                'lastname': payload.surname, 
                'mobilePhone': payload.mobile, 
                'password': payload.ipam
            }
            ipamreg = IpamRegister(ipamReg)         
            ipamtoken = IpamLogin(ipamCreds)
            ipamconnect = {
                'status': 'success',
                'message' : 'Registered and Connected to IPAM.',
                'data': ipamtoken
            }            
            return json.dumps(ipamconnect)
        else:
            data = ipamResponse['data']['error']
            ipamconnect = {
                'status': 'failed',
                'message' : 'Connected to IPAM.',
                'data': data
            }            
            return json.dumps(ipamconnect)
