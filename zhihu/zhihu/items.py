# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Compose
from scrapy.utils.markup import remove_entities
from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst, Compose

class ZhihuItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

# zhihu question
class ZhiHuQ(Item):
    title = Field(
            input_processor = MapCompose(remove_entities, unicode.strip),
            output_processor = Join()
            )
    content = Field(
            input_processor = MapCompose(remove_entities, unicode.strip),
            output_processor = Join()
            )
    id = Field(
            output_processor = TakeFirst()
            )
    user = Field(
            output_processor = TakeFirst()
            )
    num = Field(
            output_processor = TakeFirst()
            )

# zhihu user
class ZhiHuU(Item):
    id = Field(
            output_processor = TakeFirst()
            )
    name = Field(
            output_processor = TakeFirst()
            )
    url = Field(
            output_processor = TakeFirst()
            )

# zhihu answer
class ZhiHuA(Item):
    id = Field(
            input_processor = MapCompose(lambda x: int(x)),
            output_processor = TakeFirst()
            )
    qid = Field(
            output_processor = TakeFirst()
            )
    asr = Field(
            output_processor = TakeFirst()
            )
    content = Field(
            input_processor = MapCompose(remove_entities, unicode.strip),
            output_processor = Join()
            )
    score = Field(
            input_processor = MapCompose(lambda x: int(x)),
            output_processor = TakeFirst()
            )

class ZhiHuU_T(Item):
    '''
    Zhihu user topic relationship
    '''
    crawled_from = Field(
            output_processor = TakeFirst()
            )
    user_url = Field(
            output_processor = TakeFirst()
            )
    topic_url = Field(
            output_processor = TakeFirst()
            )

