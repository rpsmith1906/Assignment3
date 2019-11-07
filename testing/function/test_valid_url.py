#!/usr/bin/python3
import requests

address = "http://127.0.0.1:5000"

def test_port():
    assert requests.get(address).status_code == 200

def test_url():
    for page in ["/", "/register", "/login", "/spell_check", "/logout", "/history", "/history/query1", "/login_history"]:
        print("testing page, "+ page + "\n")
        assert requests.get(address + page).status_code == 200