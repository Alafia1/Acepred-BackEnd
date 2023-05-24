import requests

# Define the base URL of your API
base_url = "http://localhost:8000"

# Define the endpoint URL for fetching all leagues
endpoint = "/leagues"

# Send the GET request to fetch all leagues
response = requests.get(base_url + endpoint)

# Check the response status code
if response.status_code == 200:
    leagues = response.json()
    country = []
    print (len(leagues))
    for league in leagues:
        country.append(league['country'])
    set_country = set(country)
    unique_country = list(set_country)
    print(len(unique_country))
    unique_country.sort()
    print(unique_country)

else:
    # Error occurred
    print("Failed to fetch leagues. Status code:", response.status_code)
    print("Error message:", response.text)

