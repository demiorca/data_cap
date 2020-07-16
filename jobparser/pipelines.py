from pymongo import MongoClient
import re

class JobparserPipeline:

    def __init__(self):

        self.client = MongoClient('localhost', 27017)
        self.mongo_base = self.client.jobs_db

    def process_item(self, item, spider):

        collection = self.mongo_base[spider.name]

        if spider.name == 'hhru':
            salary = ''.join(item['salary']).replace('\xa0', '')
            item['salary_min'], item['salary_max'] = self.process_salary_hh(salary)
            del item['salary']

        else:
            salary = ''.join(item['salary']).replace('\xa0', '').replace('/месяц', '')
            item['salary_min'], item['salary_max'] = self.process_salary_sj(salary)
            del item['salary']

        collection.insert_one(item)

        return item

    def __del__(self):

        self.client.close()

    def process_salary_hh(self, salary):

        min_salary_reg_hh = '^\d*\s\d*|^[от]+\s(\d*\s\d*)'
        max_salary_reg_hh = '-(\d*\s\d*)|^[до]+\s(\d*\s\d*)'

        min_salary_pattern_hh = re.compile(min_salary_reg_hh)
        max_salary_pattern_hh = re.compile(max_salary_reg_hh)

        min_salary_hh = min_salary_pattern_hh.search(salary)
        max_salary_hh = max_salary_pattern_hh.search(salary)

        if min_salary_hh:
            min_salary_hh = min_salary_hh.group(0).replace('от', '').replace(' ', '')
        if max_salary_hh:
            max_salary_hh = max_salary_hh.group(0).replace('-', '').replace(' ', '')

        return min_salary_hh, max_salary_hh

    def process_salary_sj(self, salary):

        min_salary_reg_sj = '-(\d*\d*)|^[от]+(\d*\d*)|^(\d*\d*)'
        max_salary_reg_sj = '-(\d*\d*)|^[до]+(\d*\d*)'

        min_salary_pattern_sj = re.compile(min_salary_reg_sj)
        max_salary_pattern_sj = re.compile(max_salary_reg_sj)

        min_salary_sj = min_salary_pattern_sj.search(salary)
        max_salary_sj = max_salary_pattern_sj.search(salary)

        if min_salary_sj:
            min_salary_sj = min_salary_sj.group(0).replace('от', '').replace('о', 'None')
        if max_salary_sj:
            max_salary_sj = max_salary_sj.group(0).replace('до', '').replace('о', 'None').replace('—', '')

        return min_salary_sj, max_salary_sj
