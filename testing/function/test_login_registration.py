import requests
from bs4 import BeautifulSoup

address = "http://127.0.0.1:5000"
client = requests.session()
login_data = {}

def getid(html,id):
    extract = BeautifulSoup(html, "html.parser")
    data = extract.find(id=id)
    return data

def get_token(addr):
    r = client.get(addr)
    extract = BeautifulSoup(r.text, "lxml")
    token = extract.find(id="csrf_token")['value']
    return (token)

def login(user, pword, twofa, search, id_field ):
    addr = address + "/login"
    csrftoken = get_token(addr)
    login_data = {
        'csrf_token':csrftoken,
        'username': user,
        'password': pword,
        'twofapassword': twofa
    }

    r = client.post(addr, login_data)
    data = getid(r.text, id_field)
    assert data != None, "Missing id='success' in the html response"
    return ( search in data.text.lower() )

def registration(user, pword, twofa, search, id_field ):
    addr = address + "/register"
    csrftoken = get_token(addr)
    login_data = {
        'csrf_token':csrftoken,
        'username': user,
        'password': pword,
        'twofapassword': twofa
    }

    r = client.post(addr, login_data)
    data = getid(r.text, id_field) 
    assert data != None, "Missing id='success' in the html response"
    return ( search in data.text.lower() )

def test_login():
    resp = login("admin", "Administrator@1", "12345678901", "success","result")
    client.get(address + "/logout")
    assert resp, "Successfully logged in"

def test_registration():
    resp = registration("admin2", "test", "12345678901", "success","success")
    client.get(address + "/logout")
    assert resp, "Successfully registration"

    resp = registration("admin3", "", "12345678901", "failure","success")
    client.get(address + "/logout")
    assert resp, "Successfully failed registration - missing password"

    resp = registration("admin4", "test", "", "success","success")
    client.get(address + "/logout")
    assert resp, "Successfully Registered without 2FA"

    resp = registration("admin5", "test", "ABC", "failure","success")
    client.get(address + "/logout")
    assert resp, "Successfully failed 2FA registration - bad 2FA"

    resp = registration("admin", "test", "", "failure","success")
    client.get(address + "/logout")
    assert resp, "Successfully failed 2FA registration - User exists"



#def test_registration():
#    client = requests.session()
    # Retrieve the CSRF token first

#    a=client.get(address)
#    extract = BeautifulSoup(a.text, "lxml")
#    csrftoken = extract.find(id="csrf_token")['value']

#   payload = {
#        'csrf_token':csrftoken,
#        'username':'admin1',
#        'password':'Administrator@1',
#        'twofapassword':'12345678901'
#    }
#    print (payload)
#    r = client.post(address, payload)
#    print (r.text)
#    client.get("http://127.0.0.1:5000/logout")
#    assert (0)