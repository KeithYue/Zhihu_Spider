from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import BaseSpider
from zhihu.items import ZhihuItem, ZhiHuA, ZhiHuQ, ZhiHuU, ZhiHuU_T
from scrapy.contrib.loader import XPathItemLoader
from scrapy.selector import Selector
from scrapy.http import FormRequest, Request
import exceptions
import json
import re

def get_all_url_list():
    user_path = './zhihu_user.json'
    users = json.load(open(user_path, 'r'))
    for user in users:
        if user.has_key('url'):
            yield user['url']

class ZhizhuUserTopicSpiderSpider(BaseSpider):
    name = "zhihu_topic_spider"
    allowed_domains = ["zhihu.com"]

    def start_requests(self):
        return [FormRequest(
            "http://www.zhihu.com/login",
            formdata = {'email':'xxx@gmail.com',
                'password':'123456'
                },
            callback = self.after_login
            )]

    def after_login(self, response):
        print 'after_login'
        # print response.headers
        # deal with the csrf filed within the form field
        self.xsrf = response.headers['Set-Cookie'].split(';')[0].split('=')[-1]
        print self.xsrf
        for url in get_all_url_list():
            post_url = ''.join([
                'http://www.zhihu.com',
                url,
                '/topics'
                ])
            yield Request(post_url, callback=self.gen_topic_form)

    def gen_topic_form(self, response):
        # yield the beginning topics
        sel = Selector(response)
        for topic_sel in sel.xpath('//div[@id="zh-profile-topic-list"]/div[contains(@class, "zm-profile-section-item")]'):
            # new user-topic relationship
            yield self.get_UT_item(topic_sel, response.url)

        # get the number of topics of one user
        num_topic = sel.xpath('//div[contains(@class, "zm-profile-section-wrap")]/div[contains(@class, "zm-profile-section-head")]//span[contains(@class, "zm-profile-section-name")]/text()')
        number_str = num_topic.extract()[0]
        # print number_str
        p = re.compile(r'\d+')
        m = p.findall(number_str)
        if m:
            num_topic = int(m[0])
            # crawl the remainding topics of a user
            base_line = 20
            if num_topic > 20:
                while  num_topic > 0:
                    yield FormRequest(
                            url = response.url,
                            formdata = {
                                'start': '0',
                                'offset': str(base_line),
                                '_xsrf': self.xsrf
                                },
                            callback=self.parse
                            )
                    num_topic = num_topic - 20
                    base_line += 20

    def get_UT_item(self, sel, user_url):
        '''
        given the selector of topic and user url, generate the u_t relationship
        '''
        ut_loader = XPathItemLoader(item=ZhiHuU_T(), selector = sel)
        ut_loader.add_value('crawled_from', user_url)
        ut_loader.add_value('user_url', '/'+'/'.join(user_url.split('/')[-3:-1]))
        ut_loader.add_xpath('topic_url', './/a[contains(@class, "zm-list-avatar-link")]/@href')

        return  ut_loader.load_item()


    def parse(self, response):
        r_text = json.loads(response.body)
        if r_text['msg'][0] > 0:
            # print r_text['msg'][1]
            sel = Selector(text = r_text['msg'][1])
            for topic_sel in sel.xpath('.//div[contains(@class, "zm-profile-section-item")]'):
                # new user-topic relationship
                # print 'find extra topic'
                yield self.get_UT_item(topic_sel, response.url)
