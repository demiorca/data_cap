BOT_NAME = 'leroymparser'

SPIDER_MODULES = ['leroymparser.spiders']
NEWSPIDER_MODULE = 'leroymparser.spiders'

IMAGES_STORE = 'photo'
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.119 Safari/537.36'

LOG_ENABLED = True
LOG_LEVEL = 'DEBUG'

ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 16

DOWNLOAD_DELAY = 1

COOKIES_ENABLED = False

ITEM_PIPELINES = {
   'leroymparser.pipelines.DataBasePipeline': 300,
   'leroymparser.pipelines.LeroymPhotosPipeline': 200
}
