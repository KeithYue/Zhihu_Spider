from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import BaseSpider
from zhihu.items import ZhihuItem, ZhiHuA, ZhiHuQ, ZhiHuU
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import Selector
from scrapy.http import FormRequest
import exceptions
import json
import re

def generate_uid(user_name):
    return hash(user_name)

def get_all_qurl_list():
    q = []
    q_path = './zhihu_q.dat'
    q_file = open(q_path, 'r')
    for line in q_file.xreadlines():
        q.append(line.strip())
    return q

class ZhihuSpiderSpider(BaseSpider):
    name = "zhihu_spider"
    allowed_domains = ["zhihu.com"]
    # start_urls = get_all_qurl_list()

    def start_requests(self):
        return [FormRequest(
            "http://www.zhihu.com/login",
            formdata = {'email':'example.com',
                'password':'123456'
                },
            callback = self.after_login
            )]

    def after_login(self, response):
        print 'after login'
        requests = []
        for url in get_all_qurl_list():
            yield self.make_requests_from_url(url)

    def parse(self, response):
        sel = Selector(response)
        answers_xpath = '//div[@id="zh-question-answer-wrap"]/div[contains(@class, "zm-item-answer")]'
        asker_xpath = '//div[contains(@class, "zh-question-followers-sidebar")]//a[contains(@class, "zm-item-link-avatar")]'
        answer_number = 0

        # use Itemloader to populate the data
        # question
        q_id = int(response.url.split('/')[-1])
        q_loader = XPathItemLoader(item = ZhiHuQ(), selector=sel)
        q_loader.add_xpath('title', '//div[@id="zh-question-title"]/h2/text()')
        q_loader.add_xpath('content', '//div[@id="zh-question-detail"]//text()')
        q_loader.add_value('id', q_id)

        # asker information
        asker_loader = XPathItemLoader(item = ZhiHuU(), selector=sel)
        asker_loader.add_xpath('name', '//div[contains(@class, "zh-question-followers-sidebar")]//a[contains(@class, "zm-item-link-avatar")][1]/@title')
        asker_loader.add_xpath('url', '//div[contains(@class, "zh-question-followers-sidebar")]//a[contains(@class, "zm-item-link-avatar")][1]/@href')
        asker_loader.add_value('id', generate_uid(asker_loader.get_output_value('name')))
        print asker_loader.get_output_value('name')

        # add user to question field
        q_loader.add_value('user', asker_loader.load_item())

        # yiled question and asker
        yield q_loader.load_item()
        yield asker_loader.load_item()

        # generate answer information
        for ans_selector in sel.xpath(answers_xpath):
            answer_loader = XPathItemLoader(item =  ZhiHuA(), selector = ans_selector)
            answer_loader.add_xpath('id', './@data-aid')
            answer_loader.add_value('qid', q_loader.get_output_value('id'))
            answer_loader.add_xpath('content', './/div[contains(@class, "zm-item-rich-text")]//text()')
            answer_loader.add_xpath('score', './/div[contains(@class, "zm-item-vote")]/a[contains(@class, "zm-item-vote-count")]/@data-votecount')

            # answerer info
            user_loader = XPathItemLoader(item = ZhiHuU(), selector = ans_selector)
            # some user is anonymity
            user_loader.add_xpath('name', './/div[contains(@class, "zm-item-answer-author-info")]/h3//a[2]/text()')
            user_loader.add_xpath('url', './/div[contains(@class, "zm-item-answer-author-info")]/h3//a[2]/@href')
            if user_loader.get_output_value('name') is not None:
                # print user_loader.get_output_value('name').encode('utf-8')

                # add answer_number
                answer_number += 1
                user_loader.add_value('id', generate_uid(user_loader.get_output_value('name')))
                answer_loader.add_value('asr', user_loader.load_item())
                yield answer_loader.load_item()
                yield user_loader.load_item()
            else:
                continue

        q_loader.add_value('num', answer_number)
        print q_loader.get_output_value('num')

