#!/usr/bin/python3
# -*-coding:Utf-8 -*

import notifier

config = {
	'url': 'http://eune.leagueoflegends.com/en/news',
	'articleSelector': '.node-article',
	'titleSelector': 'h4 a',
	'bodySelector': '.teaser-content'
}

nc = notifier.NewsCrawler(config)

tracker = notifier.NewsTracker('/Users/nathan/sandbox/Notifier/logs/log.notifier', nc)
tracker.update()
