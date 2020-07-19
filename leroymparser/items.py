import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_price(value):

    try:
        value = value.replace(' ', '')
        value = int(value)
        return value
    except:
        return value

class LeroymparserItem(scrapy.Item):

    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(cleaner_price), output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    characteristics_dict = scrapy.Field()
