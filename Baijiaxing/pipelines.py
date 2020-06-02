# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json

class BaijiaxingPipeline(object):
    def __init__(self):
        self.file = codecs.open('data/baijiaxing.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item))
        self.file.write(line.decode("unicode_escape"))
        return item
