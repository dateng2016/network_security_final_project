# read website_cookies.json from local directory 
import json

# Specify the path to your JSON file
file_path = 'website_output.json'

# Open and read the JSON file
with open(file_path, 'r') as file:
    data = json.load(file)  # Parse the JSON file into a Python dictionary or list

# Access the data

# output json data with domain and complaince of GDPR (if any is not functional or security then not compliant)
res = {}
for domain in data:
    cookies = data[domain]
    if not isinstance(cookies, list):
        continue
    compliance = True
    for cookie in cookies:
        classification = cookie["classification"]
        if classification not in ["Functional", "Security"]:
            compliance = False
            break
    res[domain] = compliance

with open("complianceResult.json", "w") as file:
    json.dump(res, file, indent=4)





    