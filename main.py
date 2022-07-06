import json
import sys

import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

ip = ""
port = "8443"
username = ""
password = ""

authorization = ""
headerss = {}

def login(username, password):
    print(f"Login: {username} into https://{ip}:{port}")
    _json = {
        'username': username,
        'password': password,
        'remember': True
    }

    try:
        s = requests.Session()
        login_req = s.post('https://' + ip + ':' + port + '/api/login',  data = json.dumps(_json) , verify = False, timeout = 5)
    except:
        print(login_req)
        raise ValueError("Couldn't login!")

    if login_req.status_code == 200:
        authorization = login_req.cookies.get_dict()["unifises"]
        headers = {
            'Content-Type': 'application/json',
            'Accept': '*/*',
            'Authorization': 'Bearer ' + authorization,
        }
        return s, headers
    else:
        raise ValueError("Couldn't login!")

def get_sites(s, headers):
    print("Getting sites")
    sites = []
    try:
        sites_req = s.get('https://' + ip + ':' + port + '/api/self/sites', headers=headers, verify=False, timeout=5)
    except:
        print(sites_req)
        raise ValueError("Couldn't request sites!")
    if sites_req.status_code == 200:
        for site in json.loads(sites_req.content)["data"]:
            print("Found site: " + site["name"])
            sites.append(site["name"])
        return sites
    else:
        raise ValueError("Couldn't request sites!")

def get_devices(s, headers, site):
    print("Getting devices in " + site)
    devices = []
    try:
        devices_req = s.post('https://' + ip + ':' + port + '/api/s/' + site + '/stat/device', headers=headers, verify=False, timeout=5)
    except:
        print(devices_req)
        raise ValueError("Couldn't request devices!")
    if devices_req.status_code == 200:
        for device in json.loads(devices_req.content)["data"]:
            if device["adopted"] == True:
                print("Found: " + device["name"] + " (" + device["model"] + "). ID: " + device["device_id"] + " LED is " + device["led_override"] + ".")
                devices.append(device)
            else:
                print("Found: " + device["name"] + " (" + device["model"] + ") but not Adopted!")
        return devices
    else:
        raise ValueError("Couldn't request devices!")

def set_device(s, headers, site, device_id, state):
    print(f"Setting: {device_id} LED to {state}")
    data = {'led_override': state}
    try:
        config_req = s.put('https://' + ip + ':' + port + '/api/s/' + site + '/rest/device/' + device_id, headers=headers, data=json.dumps(data), verify=False, timeout=5)
    except:
        print(config_req)
        raise ValueError("Couldn't change device config!")
    if config_req.status_code == 200:
        return state
    else:
        raise ValueError("Couldn't change device config!")

session, headers = login(username, password)
sites = get_sites(session, headers)
for site in sites:
    devices = get_devices(session, headers, site)
    for device in devices:
        set_device(session, headers, site, device["device_id"], sys.argv[1])
session.close()