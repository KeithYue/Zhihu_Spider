import nltk
import codecs
import json
import re
import gensim
from zhihu_config import *
from gensim import corpora, models, similarities

ZHIHU_Q_PATH = './zhihu_q.json'
ZHIHU_A_PATH = './zhihu_a.json'
ZHIHU_U_PATH = './zhihu_user.json'

ZHIHU_U_T_PATH = './zhihu_user_topic.dat'

ZHIHU_VOCAB_PATH = './zhihu_dat/vocab.dat'

ZHIHU_DICT_PATH = './zhihu_dat/zhihu.dict'

# id relationship
ZHIHU_ITEM_ID = './zhihu_dat/item_id.dat'
ZHIHU_USER_ID = './zhihu_dat/user_id.dat'

# this is for corpus data
ZHIHU_ITEM_PATH = './zhihu_dat/item.dat'
ZHIHU_USER_PATH = './zhihu_dat/users.dat'

# this for adj data
ZHIHU_ITEM_ADJ = './zhihu_dat/item_adj.dat'
ZHIHU_USER_ADJ = './zhihu_dat/user_adj.dat'

# this for truth data
ZHIHU_TRUTH_ADJ = './zhihu_dat/truth.dat'

# this for user profile
ZHIHU_USER_Q_NUMBER = './zhihu_dat/user_q_num.dat'
ZHIHU_USER_Q_SCORE = './zhihu_dat/user_q_score.dat'

dictionary = corpora.Dictionary.load(ZHIHU_DICT_PATH)

# formateed user topic dat
ZHIHU_USER_TOPIC_PATH = './zhihu_dat/zhihu_user_topic.dat'
