import re
import json
import time
import random
import warnings
import requests

import core.config

warnings.filterwarnings('ignore') # Disable SSL related warnings

def requester(url, data, headers, GET, delay, cookie):
    if core.config.globalVariables['jsonData']:
        data = json.dumps(data)
    if core.config.globalVariables['stable']:
        delay = random.choice(range(6, 12))
    time.sleep(delay)
    #headers['Host'] = re.search(r'https?://([^/]+)', url).group(1)
    if GET:
        if cookie:
            response = requests.get(url, params=data, headers=headers, verify=False, cookies=cookie)
        else:
            response = requests.get(url, params=data, headers=headers, verify=False)
    elif core.config.globalVariables['jsonData']:
        if cookie:
            response = requests.post(url, json=data, headers=headers, verify=False, cookies=cookie)
        else:
            response = requests.post(url, json=data, headers=headers, verify=False)
    else:
        if cookie:
            response = requests.post(url, data=data, headers=headers, verify=False, cookies=cookie)
        else:
            response = requests.post(url, data=data, headers=headers, verify=False)
    return response
