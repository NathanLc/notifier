#!/usr/bin/python3
# -*-coding:Utf-8 -*

import notifier

configs = [{
	'url': 'http://eune.leagueoflegends.com/en/news',
	'articleSelector': '.node-article',
	'titleSelector': 'h4 a',
	'bodySelector': '.teaser-content',
	'logFile': '/Users/nathan/sandbox/Notifier/logs/log.notifier'
}]


for conf in configs:
	nc = notifier.NewsCrawler(conf)
	tracker = notifier.NewsTracker(conf['logFile'], nc)
	tracker.update()
