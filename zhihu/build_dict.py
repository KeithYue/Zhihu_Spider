import nltk
import codecs
import json
import re
import gensim
from zhihu_config import *

q = open(ZHIHU_Q_PATH, 'r')
qs = json.loads(q.read())
q.close()

vocab_file = codecs.open(ZHIHU_VOCAB, 'w', 'utf-8')

text = []
def get_question():
    for item in qs:
        yield item['title'] + item['content']

for question in get_question():
    for word in list(question):
        text.append(word)

fdist = nltk.FreqDist(text)

for word in fdist.keys():
    print word
    vocab_file.write(word + '\n')

print 'vocab over!!!'
