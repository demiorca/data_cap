import scrapy

class JobparserItem(scrapy.Item):

    _id = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field()
    salary_min = scrapy.Field()
    salary_max = scrapy.Field()
    link = scrapy.Field()
    source = scrapy.Field()
