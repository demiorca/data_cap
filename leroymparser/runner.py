from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from leroymparser.spiders.leroymerlinru import LeroymSpider
from leroymparser import settings

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymSpider, search='рассада цветов')

    process.start()
