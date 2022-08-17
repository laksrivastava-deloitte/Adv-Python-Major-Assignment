import requests
import json

url = "http://127.0.0.1:5001/register"

payload = json.dumps({
  "username": "ab",
  "password": "ab",
  "is_admin": True
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)