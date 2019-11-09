import requests
import re
from bs4 import BeautifulSoup

address = "http://127.0.0.1:5000"
client = requests.session()
login_data = {}

def getid(html,id, parser):
    extract = BeautifulSoup(html, parser)
    data = extract.find(id=id)
    return (data)

def get_token(addr):
    r = client.get(addr)
    extract = BeautifulSoup(r.text, "lxml")
    token = extract.find(id="csrf_token")['value']
    return (token)

def login(user, pword, twofa, search, id_field ):
    addr = address + "/login"
    login_data = {
        'username': user,
        'password': pword,
        'twofapassword': twofa
    }

    r = client.post(addr, login_data)
    data = getid(r.text, id_field, "html.parser")
    assert data != None, "Missing id='success' in the html response"
    return ( search in data.text.lower() )

def registration(user, pword, twofa, search, id_field ):
    addr = address + "/register"
    login_data = {
        'username': user,
        'password': pword,
        'twofapassword': twofa
    }

    r = client.post(addr, login_data)
    data = getid(r.text, id_field, "html.parser") 
    assert data != None, "Missing id='success' in the html response"
    return ( search in data.text.lower() )

def get_history(user):
    addr = address + "/history"

    if ( len(user) > 0 ) :
        data = {
            'username': user    
        }
        r = client.post(addr, data)
    else :
        r = client.get(addr)
    
    numqueries  = getid(r.text, "numqueries", "lxml").find_all(text=True)[0]

    extract = BeautifulSoup(r.text, "lxml")
    data = extract.find_all(id=re.compile("^query"))
   
    return ( int(numqueries) == len(data))

def post_spell():
    addr = address + "/spell_check"
    data = {
        'content': "This is a test",
    }

    r = client.post(addr, data)
    return ()

def test_registration_history_nonadmin():
    resp = registration("admin32", "test", "", "success","success")
    assert resp, "Successfully registration"

    resp = login("admin32", "test", "", "success","result")
    assert resp, "Successfully logged in"

    post_spell()
    post_spell()
    resp = get_history("")
    client.get(address + "/logout")
    assert resp, "Correct number queries found for non-admin"
    
    resp = login("admin", "Administrator@1", "12345678901", "success","result")
    assert resp, "Admin successfully logged in"

    resp = get_history("admin32")
    client.get(address + "/logout")
    assert resp, "Correct number queries found for admin"
