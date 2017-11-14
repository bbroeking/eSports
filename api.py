import urllib.request
import urllib.parse

import json

PandaScoreAPIKey = 'YKbfULoCD_OJaWO9psnXOew9DfVrB2G8CvjOBSA1nlAWziCkNMk'

url = 'https://api.pandascore.co/leagues.json?token=' + PandaScoreAPIKey
print(url)
json_obj = urllib.request.urlopen(url)

data = json.load(json_obj)
print(json.dumps(data, indent=4, sort_keys=True))

print(data)
