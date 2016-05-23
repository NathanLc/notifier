#!/usr/bin/python3
# -*-coding:Utf-8 -*

import notifier

configs = [{
	'url': 'http://eune.leagueoflegends.com/en/news',
	'articleSelector': '.node-article',
	'titleSelector': 'h4 a',
	'bodySelector': '.teaser-content',
	'logFile': '/Users/nathan/sandbox/Notifier/logs/log.notifier'
}, {
	'url': 'http://www.markknopfler.com/news',
	'articleSelector': 'article.post',
	'titleSelector': 'h3 a',
	'bodySelector': 'p + p',
	'logFile': '/Users/nathan/sandbox/Notifier/logs/log.mk'
}]


for conf in configs:
	# try:
	nc = notifier.NewsCrawler(conf)
	tracker = notifier.NewsTracker(conf['logFile'], nc)
	tracker.update()
	# except Exception as exc:
		# print('Coin')
		# print('watch script, exception occured: '+str(exc))
