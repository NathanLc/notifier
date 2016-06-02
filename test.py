import requests, json

r = requests.get('http://localhost:3030/categories')
r.raise_for_status()

result = r.json()
data = result['data']

for cat in data:
	print(cat['shortName'])
