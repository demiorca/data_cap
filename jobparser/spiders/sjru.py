import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class SjruSpider(scrapy.Spider):

    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=data']

    def parse(self, response: HtmlResponse):

        next_page = response.xpath("//a[@class='icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe']/@href").extract_first()
        job_links = response.xpath("//div[@class='_3mfro PlM3e _2JVkc _3LJqf']//@href").extract()

        for link in job_links:

            yield response.follow(link, callback=self.job_parse)

        yield response.follow(next_page, callback=self.parse)

    def job_parse(self, response: HtmlResponse):

        job_name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first()
        job_salary = response.xpath("//span[@class='_1OuF_ ZON4b']//text()").extract()
        job_link = response.url
        job_source = SjruSpider.allowed_domains[0]

        yield JobparserItem(name=job_name, salary=job_salary, link=job_link, source=job_source)
