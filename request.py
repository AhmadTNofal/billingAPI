import requests

url = 'http://localhost:5000/billing/api/v1/bi'
headers = {
    'Authorization': '887c89ccdc5fc85472748f47a591ee88',
    'Content-Type': 'application/json'
}
data = {
    "bill_number": "12345",
    "reference_number": "67890",
    "service_code": "155"
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())
