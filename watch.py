#!/usr/bin/python3
# -*-coding:Utf-8 -*

import notifier, os
import localConfig

api = localConfig.api
logsFolder = localConfig.logsFolder

configs = [{
	'category': 'mk',
	'url': 'http://www.markknopfler.com/news',
	'articleSelector': 'article.post',
	'titleSelector': 'h3',
	'linkSelector': 'h3 a',
	'bodySelector': 'p + p',
	'logFile': os.path.join(logsFolder, 'log.mk')
}, {
	'category': 'sog',
	'url': 'http://www.secretsofgrindea.com/index.php/dev-blog',
	'articleSelector': '#posts div.post',
	'titleSelector': 'div.header',
	'linkSelector': 'div.header a',
	'imageSelector': 'div.post-content div.edited-content img',
	'bodySelector': 'div.post-content div.edited-content',
	'logFile': os.path.join(logsFolder, 'log.sog')
}, {
	'category': 'sog',
	'url': 'https://twitter.com/hashtag/SecretsofGrindea?src=hash&lang=en',
	'articleSelector': 'div.stream ol li.stream-item div.tweet div.content',
	'titleSelector': 'div.js-tweet-text-container p',
	'linkSelector': 'div.js-tweet-text-container p a',
	'imageSelector': 'div.AdaptiveMedia img',
	'bodySelector': None,
	'logFile': os.path.join(logsFolder, 'log.tweeter.sog')
}, {
	'category': 'lh',
	'url': 'https://twitter.com/lifehacker',
	'articleSelector': 'div.stream ol li.stream-item div.tweet div.content',
	'titleSelector': 'div.js-tweet-text-container p',
	'linkSelector': 'div.js-tweet-text-container p a',
	'imageSelector': 'div.AdaptiveMedia img',
	'bodySelector': None,
	'logFile': os.path.join(logsFolder, 'log.tweeter.lh')
}, {
	'category': 'candh',
	'url': 'http://explosm.net/comics/archive',
	'articleSelector': 'div.archive-list-item',
	'titleSelector': 'div.meta-data > h3',
	'linkSelector': 'div.meta-data > h3 > a',
	'imageSelector': 'img.comic-thumbnail',
	'bodySelector': 'div.meta-data .author-credit-name',
	'logFile': os.path.join(logsFolder, 'log.cyanide')
}, {
	'category': 'blocket',
	'url': 'https://www.blocket.se/goteborg?q=tangentbord&cg=5000&w=1&st=s&ca=15&is=1&l=0&md=th',
	'articleSelector': '#item_list article.item_row',
	'titleSelector': 'div.media-body.desc > h1',
	'linkSelector': 'div.media-body.desc > h1 > a',
	'imageSelector': 'a > img.item_image',
	'bodySelector': 'div.media-body.desc p.list_price',
	'logFile': os.path.join(logsFolder, 'log.blocket.keyboard')
}, {
	'category': 'blocket',
	'url': 'https://www.blocket.se/goteborg?q=tangentbord&cg=5020&w=1&st=s&c=5023&ca=15&is=1&l=0&md=th',
	'articleSelector': '#item_list article.item_row',
	'titleSelector': 'div.media-body.desc > h1',
	'linkSelector': 'div.media-body.desc > h1 > a',
	'imageSelector': 'a > img.item_image',
	'bodySelector': 'div.media-body.desc p.list_price',
	'logFile': os.path.join(logsFolder, 'log.blocket.keyboard')
}]

for conf in configs:
	# try:
	nc = notifier.NewsCrawler(conf)
	tracker = notifier.NewsTracker(nc, conf['category'], conf['logFile'], api)
	tracker.watch(90)
	# except Exception as exc:
		# print('watch script, exception occured: '+str(exc))
