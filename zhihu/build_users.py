from zhihu_config import *

q = json.loads(open(ZHIHU_Q_PATH, 'r').read())

q_content_adj = {}

for question in q:
    q_content_adj[question['id']] = ''.join([
        question['title'],
        question['content']
        ])

qid = {}
qid_file = open(ZHIHU_ITEM_ID, 'r')

for line in qid_file.readlines():
    raw_data = line.strip()
    oid, nid = raw_data.split('\t')
    qid[int(nid)] = int(oid)

user_corpus = []
user_adj_file = open(ZHIHU_USER_ADJ, 'r')
for line in user_adj_file.readlines():
    nqids = line.strip().split(' ')[1:]
    this_user_text_list = [
            q_content_adj[qid[int(nid)]] for nqid in nqids
            ]
    this_texts = ''.join(this_user_text_list)
    bow = dictionary.doc2bow(list(this_texts))
    print bow
    user_corpus.append(bow)

corpora.BleiCorpus.serialize(ZHIHU_USER_PATH, user_corpus)
