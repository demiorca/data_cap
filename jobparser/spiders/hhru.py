import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):

    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://spb.hh.ru/search/vacancy?area=113&st=searchVacancy&fromSearch=true&text=data']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@class='bloko-button HH-Pager-Controls-Next HH-Pager-Control']/@href").extract_first()
        job_links = response.xpath("//a[@class='bloko-link HH-LinkModifier']/@href").extract()

        for link in job_links:

            yield response.follow(link, callback=self.job_parse)

        yield response.follow(next_page, callback=self.parse)

    def job_parse(self, response: HtmlResponse):

        job_name = response.xpath("//h1[@class='bloko-header-1']/text()").extract_first()
        job_salary = response.xpath("//span[@class='bloko-header-2 bloko-header-2_lite']/text()").extract()
        job_link = response.url
        job_source = HhruSpider.allowed_domains[0]

        yield JobparserItem(name=job_name, salary=job_salary, link=job_link, source=job_source)
