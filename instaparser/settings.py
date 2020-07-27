BOT_NAME = 'instaparser'

SPIDER_MODULES = ['instaparser.spiders']
NEWSPIDER_MODULE = 'instaparser.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.119 Safari/537.36'

ROBOTSTXT_OBEY = False
LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

#CONCURRENT_REQUESTS = 32

DOWNLOAD_DELAY = 1.25

ITEM_PIPELINES = {
    'instaparser.pipelines.InstagramcomPhotosPipeline': 200,
    'instaparser.pipelines.DataBasePipeline': 300,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = True
