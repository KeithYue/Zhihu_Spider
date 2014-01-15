from zhihu_config import *

item_id_file = open(ZHIHU_ITEM_ID, 'r')
user_id_file = open(ZHIHU_USER_ID, 'r')

item_adj_file = codecs.open(ZHIHU_ITEM_ADJ, 'w', 'utf-8')
truth_file = codecs.open(ZHIHU_TRUTH_ADJ, 'w', 'utf-8')

a = json.loads(open(ZHIHU_A_PATH, 'r').read())

user_id = {}#key:user_url, value:uid

for line in user_id_file.xreadlines():
    raw_dat = line.strip()
    user_url, uid = raw_dat.split('\t')
    user_id[user_url] = int(uid)

def get_answers(qid):
    '''
    given a qid, return its answer item
    '''
    answers = []
    for answer in a:
        if answer['qid'] == qid:
            answerer = answer['asr']
            if answerer.has_key('url'):
                answers.append(answer)
    return answers

for line in item_id_file.readlines():
    raw_dat = line.strip()
    oqid = int(raw_dat.split('\t')[0])
    new_id = int(raw_dat.split('\t')[1])
    answers = get_answers(oqid)
    print new_id
    srted_answers = sorted(answers, key = lambda item:item['score'], reverse=True)

    # item_adj_file.write(str(new_id))
    # item_adj_file.write('\t')
    item_adj_file.write(str(len(srted_answers)))
    item_adj_file.write(' ')
    for answer in srted_answers:
        item_adj_file.write(''.join([
            str(user_id[answer['asr']['url']]),
            ' '
            ]))
        truth_file.write(''.join([
            str(user_id[answer['asr']['url']]),
            ' ',
            str(answer['score']),
            '\t'
            ]))
    item_adj_file.write('\n')
    truth_file.write('\n')

print 'over!!!'










