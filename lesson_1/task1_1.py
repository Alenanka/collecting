import requests
import json

user = 'Alenanka'
responce = requests.get(f'https://api.github.com/users/{user}/repos')
j_data = responce.json()

with open('data.json', 'w') as f:
  json.dump(j_data, f, ensure_ascii=False)

for data in (j_data):
    print(data.get('name'))
