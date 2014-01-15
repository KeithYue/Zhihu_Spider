from zhihu_config import *

qs = json.loads(open(ZHIHU_Q_PATH, 'r').read())

qids_file = codecs.open('./zhihu_dat/item_id.dat', 'w', 'utf-8')

question_corpus = []
for index, item in enumerate(qs):
    q_text = item['title'] + item['content']
    qid = item['id']
    bow = dictionary.doc2bow(list(q_text))
    print bow
    question_corpus.append(bow)
    qids_file.write(''.join([
        str(qid),
        '\t',
        str(index),
        '\n'
        ]))

corpora.BleiCorpus.serialize(ZHIHU_ITEM_PATH, question_corpus)
qids_file.close()
