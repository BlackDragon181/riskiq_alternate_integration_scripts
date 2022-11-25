import requests
import urllib.parse
import pyfiglet

result = pyfiglet.figlet_format("SGO - ASM Defense Lab")
print(result)

headers = {
    'Accept': 'application/json',
    'Authorization': 'Basic MmYwODlkODAxYTdhNThhNzpXd0V2dW1lbjhpUHB6ZzJTVW1kYnRob3g5MTNxN0dzVg==',
    'Content-Type': 'application/json',
}
choice = int(input("Do you want to proceed with (1)Tag or (2)Organization Name ?"))
response = None
if choice == 1:
    d1 = input("Enter the tag name: ")
    data = '{"query":null,"filters":{"condition":"AND","value":[{"name":"state","operator":"IN","value":["CONFIRMED"]},{"name":"tag","operator":"EQ","value":"' + d1.strip() + '"}]}}'
    response = requests.post('https://api.riskiq.net/v1/globalinventory/search?mark=*&size=20', headers=headers, data=data)
elif choice == 2:
    d2 = input("Enter the Organization name: ")
    data1 = '{"query":null,"filters":{"condition":"AND","value":[{"name":"state","operator":"IN","value":["CONFIRMED"]},{"name":"organization","operator":"IN","value":["' + d2.strip() + '"]}]}}'
    response = requests.post('https://api.riskiq.net/v1/globalinventory/search?mark=*&size=20', headers=headers,data=data1)

database = response.json()
hostnames = []
for item in database['content']:
    parsed_url = urllib.parse.urlparse(item['name'])
    hostnames.append(parsed_url.netloc)

print("Hostname list: ")
hostnames_String = str(hostnames).replace("'",'')
hostnames_String = str(hostnames_String).replace(" ",'')
hostnames_String = hostnames_String.replace("[",'')
hostnames_String = hostnames_String.replace("]",'')
hostnames_String = hostnames_String.rstrip(",")

print(hostnames_String)
url = "https://qualysapi.qg3.apps.qualys.com/api/2.0/fo/asset/group/?action=edit"
name = input("Enter Asset Group ID: ")

headers = {'X-Requested-With': 'Curl',}
data = {'id': name,
        'action': 'edit',
        'set_dns_names': str(hostnames_String)
        }

response = requests.post(url=url, headers=headers, data=data, verify=False, auth=('dette3cl', 'm!$Mz7UuC#M!sDC3xn'))

print(response.text)
