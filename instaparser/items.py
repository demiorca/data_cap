import scrapy

class InstaparserItem(scrapy.Item):

    _id = scrapy.Field()
    user_name = scrapy.Field()
    photos = scrapy.Field()
    db_info = scrapy.Field()
