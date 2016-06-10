import requests, json, bs4, os, datetime, time, threading, copy

# TODO: Create an article class to have the same format in NewsCrawler and Tracker

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
		if(('linkSelector' not in config.keys()) or config['linkSelector'] is None):
			print('titleSelector not provided.')
			raise Exception('titleSelector not provided.')

		self.url = config['url']
		self.articleSelector = config['articleSelector']
		self.titleSelector = config['titleSelector']
		self.linkSelector = config['linkSelector']
		self.imageSelector = config.get('imageSelector', None)
		self.bodySelector = config.get('bodySelector', None)
		# self.pageTitleSelector = config.get('pageTitleSelector', None)
		# self.pageIconSelector = config.get('pageIconSelector', None)
		self.soup = None
		self.articles = None
		self.isWatching = False
		self.watchThread = None

	def getRequest(self):
		""" Check if targeted url is accessible. Raises an exception if not. """
		# Adding user agent to simulate request past by a browser to avoid request to be blocked.
		headers = {'user-agent': 'Mozilla/5.0'}
		res = requests.get(self.url, headers=headers)
		res.raise_for_status()
		return res

	def getSoup(self):
		""" Get the content of the targeted url. """
		try:
			res = self.getRequest()
			soup = bs4.BeautifulSoup(res.text, 'html.parser')
		except Exception as exc:
			print('getSoup, exception occured: '+str(exc))
			soup = ''

		self.soup = soup

		return self.soup

	def getArticlesList(self):
		""" Get the list of articles adapted, from the page. """
		articles = self.buildArticlesList()
		self.articles = articles
		return self.articles

	def stripAndReplace(self, text):
		text = text.strip(' \t\n\r')
		text = text.replace('\n', ' ')
		text = text.replace('\r', ' ')
		text = text.replace('\r\n', ' ')
		return text

	def sanitizeForText(self, tag):
		copyTag = copy.copy(tag)
		text = copyTag.get_text()
		text = self.stripAndReplace(text)
		return text

	def removeTagAttrs(self, tag):
		if not hasattr(tag, 'attrs'):
			return

		attrToDelete = []
		for attr in tag.attrs.keys():
			if attr not in ['src', 'href']:
				attrToDelete.append(attr)
		for attr in attrToDelete:
			del tag[attr]

	def sanitizeForHtml(self, tag):
		copyTag = copy.copy(tag)
		self.removeTagAttrs(copyTag)

		for descendant in copyTag.descendants:
			self.removeTagAttrs(descendant)

		htmlString = str(copyTag)
		return htmlString

	def buildArticle(self, tag):
		""" Build an article object from the tag representing the article in HTML. """
		article = {}

		title = tag.select_one(self.titleSelector)
		titleStr = self.sanitizeForText(title)
		titleHtml = self.sanitizeForHtml(title)

		link = tag.select_one(self.linkSelector)
		if link is None:
			linkStr = ''
		else:
			linkStr = link.get('href', '');
			linkStr = self.stripAndReplace(linkStr)

		if self.imageSelector is None:
			image = ''
		else:
			image = tag.select_one(self.imageSelector)
			if image is None:
				image = ''
			else:
				image = image.get('src', None)

		if self.bodySelector is None:
			bodyStr = ''
			bodyHtml = ''
		else:
			body = tag.select_one(self.bodySelector)
			if body is None:
				bodyStr = ''
				bodyHtml = ''
			else:
				bodyStr = self.sanitizeForText(body)
				bodyHtml = self.sanitizeForHtml(body)

		article['title'] = titleStr
		article['titleHtml'] = titleHtml
		article['link'] = linkStr
		article['image'] = image
		article['body'] = bodyStr
		article['bodyHtml'] = bodyHtml

		return article

	def buildArticlesList(self):
		""" Extract articles from the targeted page and build an adapted list of these articles for later easier treatment. """
		soup = self.getSoup()

		if soup == '':
			return []

		articleTags = soup.select(self.articleSelector)
		articles = []

		for tag in articleTags:
			article = self.buildArticle(tag)
			articles.append(article)

		reversedArticles = reversed(articles)

		return reversedArticles


class NewsTracker:
	"""
	This class aims at tracking updates of news or posts.
	"""

	def __init__(self, newsCrawler, category, historyFile, api = None):
		if historyFile is None:
			print('historyFile not provided.')
			raise Exception('historyFile not provided.')
		if category is None:
			print('category not provided.')
			raise Exception('category not provided.')
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
		self.newsCrawler = newsCrawler
		self.category = category
		self.category_id = None
		self.api = api
		self.separator = ' ||| '

		self.category_id = self.getRemoteCategoryId()

	def isApiReachable(self):
		""" Check if the API is reachable. """
		if self.api is None:
			return False

		r = requests.get(self.api)
		try:
			r.raise_for_status()
			return True
		except Exception as exc:
			return False

	def getRemoteCategoryId(self):
		if self.category_id is not None:
			return self.category_id

		if not self.isApiReachable:
			return None

		r = requests.get(self.api+'/categories?shortName='+self.category)
		result = r.json()
		category = result[0]
		cat_id = category['_id']
		self.category_id = cat_id
		return cat_id

	def saveArticleLocally(self, article):
		""" Saves an article to the history file. """
		nowObj = datetime.datetime.now()
		dateStr = nowObj.strftime("%Y-%m-%d %H:%M:%S")
		historyLine = self.separator.join([dateStr, article['title'], article['link'], article['body']])

		with open(self.historyFile, 'a') as file:
			file.write(historyLine+'\n')
	
	def saveArticleRemotely(self, article):
		""" Saves the article in the api. """
		payload = {
			'title': article['title'],
			'titleHtml': article['titleHtml'],
			'category_id': self.getRemoteCategoryId(),
			'link': article['link'],
			'image': article['image'],
			'body': article['body'],
			'bodyHtml': article['bodyHtml']
		}

		r = requests.post(self.api+'/articles', data=payload)

	def extractArticleFromLocalHistory(self, historyLine):
		""" Build an article from an history line. """
		lineSplit = historyLine.split(self.separator)
		article = {}
		article['createdAt'] = lineSplit[0]
		article['title'] = lineSplit[1]
		article['link'] = lineSplit[2]
		article['body'] = lineSplit[3]

		return article

	def getLocalArticlesHistory(self):
		""" Get the list of former articles from the history. """
		historyLines = []
		with open(self.historyFile, 'r') as file:
			for line in file:
				historyLines.append(line)

		oldArticles = []
		for line in historyLines:
			article = self.extractArticleFromLocalHistory(line)
			oldArticles.append(article)

		return oldArticles

	def getRemoteArticlesHistory(self):
		""" Get the list of former articles from the api. """
		category_id = self.getRemoteCategoryId()
		if category_id is None:
			return None

		if not self.isApiReachable():
			return None

		r = requests.get(self.api+'/categories/'+category_id)
		result = r.json()
		return result['articles']

	def isSameArticle(self, oldArticle, newArticle):
		""" Compare if 2 articles are the same. """
		if (newArticle['title'] == oldArticle['title'] and newArticle['link'] == oldArticle['link']):
			return True
		else:
			return False

	def updateLocally(self, onlineArticles):
		""" Update the list of articles locally. """
		oldLocalArticles = self.getLocalArticlesHistory()

		for onlineA in onlineArticles:
			articleInLocalHistory = False

			for oldLocalA in oldLocalArticles:
				articleInLocalHistory = self.isSameArticle(oldLocalA, onlineA)
				if articleInLocalHistory:
					break

			if not articleInLocalHistory:
				self.saveArticleLocally(onlineA)

	def updateRemotely(self, onlineArticles):
		""" Update the list of articles with the api. """
		oldRemoteArticles = self.getRemoteArticlesHistory()

		for onlineA in onlineArticles:
			articleInRemoteHistory = False

			for oldRemoteA in oldRemoteArticles:
				articleInRemoteHistory = self.isSameArticle(oldRemoteA, onlineA)
				if articleInRemoteHistory:
					break

			if not articleInRemoteHistory:
				self.saveArticleRemotely(onlineA)

	def update(self):
		""" Get list of articles thanks to the NewsCrawler and update history if needed. """
		onlineArticles = self.newsCrawler.getArticlesList()

		self.updateLocally(onlineArticles)

		if self.api is not None:
			self.updateRemotely(onlineArticles)

	def updateAndSleep(self, timeInterval):
		while True:
			self.update()
			time.sleep(timeInterval)
	
	def stopWatching(self):
		self.watchThread.stop()
		self.isWatching = False

	def watch(self, timeInterval):
		updateThread = threading.Thread(target=self.updateAndSleep, args=[timeInterval])
		self.watchThread = updateThread
		updateThread.start()
		self.isWatching = True
