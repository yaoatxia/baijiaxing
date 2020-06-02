# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from Baijiaxing.items import BaijiaxingItem
import requests
import re
import json

class BaijiaxingSpider(Spider):
    name = 'baijiaxing'
    allowed_domains = ['baijiaxing.51240.com']
    start_urls = ['http://baijiaxing.51240.com']


    def __init__(self):
        self.site_domain = 'https://baijiaxing.51240.com/'
        self.items = []
        self.item = BaijiaxingItem()
        self.numb = 0


    def parse(self, response):
        print(type(response))
        sel = Selector(response)

        sites1 = sel.xpath('//body//div[@class="kuang"]//span[@class="asdasd1"]/a')
        print(len(sites1))



        for site in sites1:
            topic = site.xpath('text()').extract()
            print(len(topic))
            print("topic end")

            for top in topic:
                print("top start")
                print(top)
                itemi = {}
                itemi['name'] = top
                url = site.xpath('@href').extract()[0]
                itemi['url'] = self.site_domain + url.encode('utf-8')
                self.handle_detail(itemi['url'], itemi)
                self.items.append(itemi)
        self.item['baijiaxing'] = self.items
        return self.items

    def handle_detail(self, response, itemi):
        print(response)
        response = response.strip()
        html_requests_item = requests.get(response)
        html_requests = html_requests_item.text.encode('utf-8')


        html_response = HtmlResponse(url=response, body=html_requests, headers={'Connection': 'close'})
        html_all = Selector(html_response)

        print(json.dumps(itemi, encoding="UTF-8", ensure_ascii=False))


        itemi['from'] = html_all.xpath('//body//div[@class="kuang"]//div[@class="neirong"]/text()').extract()
        item_list_temp = []
        for item_list in itemi['from']:
            temp = item_list.encode('utf-8')
            temp = re.sub(r'\"', "“", temp)
            temp = re.sub(r'\n', "", temp)
            temp = re.sub(r'\r', "", temp)
            temp = re.sub(r'\t', "", temp)
            item_list_temp.append(temp)
        itemi['from'] = item_list_temp