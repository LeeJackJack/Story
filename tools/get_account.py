import os
import requests
import json

api_host = os.getenv('API_HOST', 'https://api.stability.ai')
url = f"{api_host}/v1/user/account"

os.environ['STABILITY_KEY'] = 'sk-3S1WkcRKxkQ5iyeHbWGXKLlqFjNonH8EfwN6Z1JZrJi3sPfw'
api_key = os.environ['STABILITY_KEY']

if api_key is None:
    raise Exception("Missing Stability API key.")

response = requests.get(url, headers={
    "Authorization": f"Bearer {api_key}"
})

if response.status_code != 200:
    raise Exception("Non-200 response: " + str(response.text))

# Do something with the payload...
payload = response.json()
print(json.dumps(payload, indent=4))

