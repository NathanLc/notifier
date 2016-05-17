import requests, bs4, os

class NewsCrawler:
	"""
	This class aims at crawling a web page containing news or posts.
	"""

	def __init__(self, config):
		if(('url' not in config.keys()) or config['url'] is None):
			# TODO: log that
			print('url not provided.')
			raise Exception('url not provided.')
		if(('articleSelector' not in config.keys()) or config['articleSelector'] is None):
			print('articleSelector not provided.')
			raise Exception('articleSelector not provided.')
		if(('titleSelector' not in config.keys()) or config['titleSelector'] is None):
			print('titleSelector not provided.')
			raise Exception('titleSelector not provided.')

		self.url = config['url']
		self.articleSelector = config['articleSelector']
		self.titleSelector = config['titleSelector']
		self.bodySelector = config.get('bodySelector', None)
		self.soup = None
		self.articles = None

	def getRequest(self):
		res = requests.get(self.url)
		res.raise_for_status()
		return res

	def getSoup(self):
		if self.soup is not None:
			return self.soup

		res = self.getRequest()
		soup = bs4.BeautifulSoup(res.text, 'html.parser')
		self.soup = soup
		return self.soup

	def getArticlesList(self):
		if self.articles is not None:
			return self.articles

		articles = self.buildArticlesList()
		self.articles = articles
		return self.articles

	def buildArticlesList(self):
		soup = self.getSoup()
		articleTags = soup.select(self.articleSelector)
		articles = []

		for tag in articleTags:
			article = {}
			title = tag.select_one(self.titleSelector)
			body = tag.select_one(self.bodySelector)
			article['title'] = title.string
			article['link'] = title['href']
			article['body'] = body.string
			articles.append(article)

		return articles


class NewsTracker:
	"""
	This class aims at tracking updates of news or posts.
	"""

	def __init__(self, historyFile, newsCrawler):
		if historyFile is None:
			print('historyFile not provided.')
			raise Exception('historyFile not provided.')
		if not os.path.isfile(historyFile):
			print('historyFile is not a valid file.');
			raise Exception('historyFile is not a valid file.')
		if newsCrawler is None:
			print('newsCrawler not provided.')
			raise Exception('newsCrawler not provided.')
		if not isinstance(newsCrawler, NewsCrawler):
			print('newsCrawler is not an instance of NewsCrawler.')
			raise Exception('newsCrawler is not an instance of NewsCrawler.')

		self.historyFile = historyFile
		self.NewsCrawler = NewsCrawler
