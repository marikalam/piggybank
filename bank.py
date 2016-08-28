import requests
import pprint

url = 'http://api108087sandbox.gateway.akana.com:80/AccountDetailRESTService/account/details'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

json =  {
"getAccountDetailRequest": {
    "getAccountDetail": {
      "accountKeyIdentifier": {
        "operatingCompanyIdentifier": "125",
        "productCode": "DDA",
        "primaryIdentifier": "4444444444444444"
      },
      "returnFiveStarPackageCodeSwitch": "true",
      "includeAddressSwitch": "true"
    }
  }
}



response = requests.post(url, json=json, headers=headers)

return response.json()['DetailAccountList']['BasicAccountDetail']['BalanceAmount']
