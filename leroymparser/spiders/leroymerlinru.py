import scrapy
from scrapy.http import HtmlResponse
from leroymparser.items import LeroymparserItem
from scrapy.loader import ItemLoader

class LeroymSpider(scrapy.Spider):

    name = 'leroymerlinru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):

        self.start_urls = [f'https://spb.leroymerlin.ru/search/?q={search}']

    def parse(self, response):

        new_items = response.css("a.paginator-button.next-paginator-button::attr(href)").extract_first()
        links = response.xpath("//a[@class='black-link product-name-inner']")
        for link in links:
           yield response.follow(link, callback=self.parse_links)
        yield response.follow(new_items, callback=self.parse)

    def parse_links(self, response: HtmlResponse):

        loader = ItemLoader(item=LeroymparserItem(), response=response)
        loader.add_xpath('name', "//h1[@class='header-2']/text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@src")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_value('url', response.url)

        characteristics = response.xpath("//dl[@class='def-list']")
        for characteristic in characteristics:
            key = characteristic.xpath("//dt[@class='def-list__term']/text()").extract()
            value = characteristic.xpath("//dd[@class='def-list__definition']/text()").extract()
            characteristics_dict = dict(zip(key, value))
            characteristics_dict = str(characteristics_dict)
            characteristics_dict = characteristics_dict.replace('\n', '').replace('\\n', '')
            characteristics_dict = ' '.join(characteristics_dict.split())
            characteristics_dict = eval(characteristics_dict)
        loader.add_value('characteristics_dict', characteristics_dict)

        yield loader.load_item()
