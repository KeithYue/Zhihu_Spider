import nltk
import codecs
import json
import re
import gensim
from zhihu_config import *
from gensim import corpora, models, similarities

vocab_file = codecs.open(ZHIHU_VOCAB_PATH, 'r')

text = []
for line in vocab_file.readlines():
    word = line.strip()
    text.append([word])

dictionary = corpora.Dictionary(text)
dictionary.save(ZHIHU_DICT_PATH)
print dictionary
