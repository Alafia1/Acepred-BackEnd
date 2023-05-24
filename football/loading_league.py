import json
import requests
from . import secret

url = "https://api-football-v1.p.rapidapi.com/v3/leagues"

headers = {
	"X-RapidAPI-Key": secret.KEY,
	"X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
}

# Define the base URL of your API
base_url = "http://localhost:8000"

# Define the endpoint URL for creating leagues
endpoint = "/leagues"

response = requests.get(url, headers=headers)

response_data = response.content.decode("utf-8")
res = json.loads(response_data)

li = []
for data in res['response']:
    id = data['league']['id']
    name = data['league']['name']
    country = data['country']['name']

    league = {
        "id": id,
        "name": name,
        'country': country
    }

    responses = requests.post(base_url + endpoint, json=league)

    if responses.status_code == 200:
        # League creation successful
        created_league = responses.json()
        print("League created successfully:")
        print(created_league)
    else:
        # Error occurred
        print("League creation failed. Status code:", responses.status_code)
        print("Error message:", responses.text)

