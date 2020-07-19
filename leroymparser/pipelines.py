from scrapy.pipelines.images import ImagesPipeline
import scrapy
from pymongo import MongoClient

class DataBasePipeline:

    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.leroym

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item

    def __del__(self):
        self.client.close()

class LeroymPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):

        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta=item)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None):

        item = request.meta
        return f'full/{item["name"]}/{item["photos"].index(request.url)}.jpg'

    def item_completed(self, results, item, info):

        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
