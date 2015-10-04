import sys
import requests
import json
import uuid
import time
import random


class iot_kit(object):
    host = "dashboard.us.enableiot.com"

    proxies = {

    }

    username = "gaiar@baimuratov.ru"
    password = "1Q2w3e4r!@"
    account_name = "gaiar3"

    device_id = "02-00-86-66-0b-13"
    account_id = ""

    observations_per_hour = 1
    days_of_data = 1

    verify = True

    api_root = "/v1/api"
    base_url = "https://{0}{1}".format(host, api_root)
    device_name = "Device-{0}".format(device_id)

    g_user_token = ""
    g_device_token = ""

    def __init__(self):
        global g_user_token, g_device_token, g_device_token

        g_user_token = self.get_token(self.username, self.password)

        uid = self.get_user_id()
        print("UserId: {0}".format(uid))

        self.account_id = self.get_account_id(uid, self.account_name)
        print("AccountId: {0}".format(self.account_id))


        # self.create_device(self.account_id, self.device_id, self.device_name)


        ac = self.generate_activation_code(self.account_id)
        print("Activation code: {0}".format(ac))

        g_device_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJqdGkiOiJmODY3YWE1Zi05ZWNhLTQzNzQtYTliZC0wZDA1NGVlMDNkNGMiLCJpc3MiOiJodHRwOi8vZW5hYmxlaW90LmNvbSIsInN1YiI6IjAyLTAwLTg2LTY2LTBiLTEzIiwiZXhwIjoiMjAyNS0wOS0zMFQxMzoxNDo0Ny40MjNaIn0.LLk9zaeEXCPgFVpTKTqFUhbd7j8FdLLDGJppKH1hKpUQcc_lk_aMVT9XocsfYfqJI43i4U_QQPNr5hRlEcmsUGWYaymh8W9duhS--p2hWvZZZOimt4rc7xXt2QrEDBDFgxAcOsEw06GrXCTB_Fpzw6gFISyXQ31FqVTFdFJOw-fm4QTpwNfrt2aefI7mopgIw2LAlMFvhQCfKlnAY29Vbcqg665gcUxPVg7udCbiL_mFAJXhDL49HLFbzl2pBQZAwHHPs-z3gYlrt2syVMmRmsXYE6wHQxo69IQBfwWi_PbRP8vw8F4mKQAFmjWVKHfLlxw7-Mhh0o-1KpY76_-yBw"
        # g_device_token = self.activate(self.account_id, self.device_id, ac)

        # cid = self.create_component(self.account_id, self.device_id, "temperature.v1.0", "temp1")
        # print ("ComponentID (cid): {0}".format(cid))

        # cid = self.create_component(self.account_id, self.device_id, "humidity.v1.1", "humidity1")
        # print ("ComponentID (cid): {0}".format(cid))

        # cid = self.create_component(self.account_id, self.device_id, "light.v1.0", "light1")
        # print ("ComponentID (cid): {0}".format(cid))

        # cid = self.create_component(self.account_id, self.device_id, "uv.v1.0", "ultraviolet1")
        # print ("ComponentID (cid): {0}".format(cid))



        print("Device token: {0}".format(g_device_token))

    def get_user_headers(self):
        headers = {
            'Authorization': 'Bearer ' + g_user_token,
            'content-type': 'application/json'
        }
        return headers

    def get_device_headers(self):
        headers = {
            'Authorization': 'Bearer ' + g_device_token,
            'content-type': 'application/json'
        }

        return headers

    def check(self, resp, code):
        if resp.status_code != code:
            print("Expected {0}. Got {1} {2}".format(code, resp.status_code, resp.text))
            sys.exit(1)

    def get_token(self, username, password):
        url = "{0}/auth/token".format(self.base_url)
        headers = {'content-type': 'application/json'}
        payload = {"username": username, "password": password}
        data = json.dumps(payload)
        resp = requests.post(url, data=data, headers=headers, proxies=self.proxies, verify=self.verify)
        self.check(resp, 200)
        js = resp.json()
        token = js['token']
        return token

    def get_user_id(self):
        url = "{0}/auth/tokenInfo".format(self.base_url)
        resp = requests.get(url, headers=self.get_user_headers(), proxies=self.proxies, verify=self.verify)
        self.check(resp, 200)
        js = resp.json()
        user_id = js["payload"]["sub"]
        return user_id

    def get_account_id(self, user_id, account_name):
        url = "{0}/users/{1}".format(self.base_url, user_id)
        resp = requests.get(url, headers=self.get_user_headers(), proxies=self.proxies, verify=self.verify)
        self.check(resp, 200)
        js = resp.json()
        if 'accounts' in js:
            accounts = js["accounts"]
            for k, v in accounts.iteritems():
                if 'name' in v and v["name"] == account_name:
                    return k
        print("Account name {0} not found.".format(account_name))
        print("Available accounts are: {0}".format([v["name"] for k, v in accounts.iteritems()]))
        return None

    def create_device(self, account, device_id, device_name):
        url = "{0}/accounts/{1}/devices".format(self.base_url, account)
        device = {
            "deviceId": str(device_id),
            "gatewayId": str(device_id),
            "name": device_name,
            "tags": ["Russia", "Moscow", "RoadShow"],
            "attributes": {
                "vendor": "intel",
                "platform": "x86",
                "os": "linux"
            }
        }
        data = json.dumps(device)
        resp = requests.post(url, data=data, headers=self.get_user_headers(), proxies=self.proxies, verify=self.verify)
        self.check(resp, 201)
        return resp

    def generate_activation_code(self, account_id):
        url = "{0}/accounts/{1}/activationcode/refresh".format(self.base_url, account_id)
        resp = requests.put(url, headers=self.get_user_headers(), proxies=self.proxies, verify=self.verify)
        self.check(resp, 200)
        js = resp.json()
        activation_code = js["activationCode"]
        return activation_code

    def activate(self, account_id, device_id, activation_code):
        url = "{0}/accounts/{1}/devices/{2}/activation".format(self.base_url, account_id, device_id)
        activation = {
            "activationCode": activation_code
        }
        data = json.dumps(activation)
        resp = requests.put(url, data=data, headers=self.get_user_headers(), proxies=self.proxies, verify=self.verify)
        self.check(resp, 200)
        js = resp.json()
        if "deviceToken" in js:
            token = js["deviceToken"]
            return token
        else:
            print(js)
            sys.exit(1)

    def create_component(self, account_id, device_id, component_type_name, name):
        url = "{0}/accounts/{1}/devices/{2}/components".format(self.base_url, account_id, device_id)
        component = {
            "type": component_type_name,
            "name": name,
            "cid": str(uuid.uuid4())
        }
        data = json.dumps(component)
        resp = requests.post(url, data=data, headers=self.get_device_headers(), proxies=self.proxies,
                             verify=self.verify)
        self.check(resp, 201)
        js = resp.json()
        return js["cid"]

    def create_observations(self, cid, val, on):
        url = "{0}/data/{1}".format(self.base_url, self.device_id)
        body = {
            "accountId": self.account_id,
            "data": [],
            "on": int(round(time.time() * 1000))
        }
        o = {
            "on": on,
            "componentId": cid,
            "value": str(val),
        }
        body["data"].append(o)
        data = json.dumps(body)
        print("Data: {0}".format(data))
        resp = requests.post(url, data=data, headers=self.get_device_headers(), proxies=self.proxies,
                             verify=self.verify)
        self.check(resp, 201)

    def get_observations(self, account_id, device_id, component_id):
        url = "{0}/accounts/{1}/data/search".format(self.base_url, account_id)
        search = {
            "from": 0,
            "targetFilter": {
                "deviceList": [device_id]
            },
            "metrics": [
                {
                    "id": component_id
                }
            ]
        }
        data = json.dumps(search)
        resp = requests.post(url, data=data, headers=self.get_user_headers(), proxies=self.proxies, verify=self.verify)
        self.check(resp, 200)
        js = resp.json()
        return js

    def print_observation_counts(self, js):
        if 'series' in js:
            series = js["series"]
            series = sorted(series, key=lambda v: v["deviceName"])
            for v in series:
                print("Device: {0} Count: {1}".format(v["deviceName"], len(v["points"])))
