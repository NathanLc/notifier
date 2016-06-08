import requests, json
payload = {
	'title': 'New SoG Post',
	'category_id': 'rHKPhIJnugW8nluH',
	'link': 'http://www.secretsofgrindea.com/index.php/dev-blog',
	'image': 'http://lorempixel.com/400/200/',
	'body': 'This is a test blablabla'
}

r = requests.post('http://localhost:3030/articles', data=payload)
