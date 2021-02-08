BOT_NAME = 'lacassa'

SPIDER_MODULES = ['lacassa.spiders']
NEWSPIDER_MODULE = 'lacassa.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'lacassa.pipelines.LacassaPipeline': 100,

}