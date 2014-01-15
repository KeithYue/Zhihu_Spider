# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.contrib.exporter import JsonLinesItemExporter, JsonItemExporter, XmlItemExporter
from zhihu.items import ZhihuItem, ZhiHuA, ZhiHuQ, ZhiHuU
from scrapy import signals
import codecs

class ZhihuPipeline(object):
    def __init__(self):
        self.files_path = {}
        self.files = {}
        self.exporters = {}
        self.files_path['user_file'] = './zhihu_user.json'
        self.files_path['question_file'] = './zhihu_q.json'
        self.files_path['answer_file'] = './zhihu_a.json'

    def open_spider(self, spider):
        print 'Opening spider.'
        self.files['question'] = codecs.open(self.files_path['question_file'], 'w', encoding='utf-8')
        self.files['answer'] = codecs.open(self.files_path['answer_file'], 'w', encoding='utf-8')
        self.files['user'] = codecs.open(self.files_path['user_file'], 'w', encoding='utf-8')

        self.exporters['question'] = JsonItemExporter(self.files['question'])
        self.exporters['answer'] = JsonItemExporter(self.files['answer'])
        self.exporters['user'] = JsonItemExporter(self.files['user'])

        for exporter in self.exporters.itervalues():
            exporter.start_exporting()

    def close_spider(self, spider):
        print 'Closing spider'
        for exporter in self.exporters.itervalues():
            exporter.finish_exporting()

        for opened_file in self.files.itervalues():
            opened_file.close()

    def process_item(self, item, spider):
        if isinstance(item, ZhiHuQ):
            # print 'It is question'
            self.exporters['question'].export_item(item)
        elif isinstance(item, ZhiHuA):
            # print 'It is answer'
            self.exporters['answer'].export_item(item)
        elif isinstance(item, ZhiHuU):
            # print 'It is user'
            self.exporters['user'].export_item(item)
        else:
            pass
        return item
