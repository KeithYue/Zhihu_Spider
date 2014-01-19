from __future__ import division
from zhihu_config import *
user_adj_file = open(ZHIHU_USER_ADJ, 'r')
q_adj_file = open(ZHIHU_TRUTH_ADJ, 'r')

u_q = {} # uid: qnum, qids
q_u_score = {}# qid, (uid, score)

# build u_q rel
for index, line in enumerate(user_adj_file.readlines()):
    u_q[index] = {
            'num':0,
            'qid':[]
            }

    item = line.strip().split(' ')
    q_num = int(item[0])
    u_q[index]['num'] = q_num
    for qid in item[1:]:
        u_q[index]['qid'].append(int(qid))

# build q score rel
for index, line in enumerate(q_adj_file.readlines()):
    q_u_score[index] = []
    raw_data = line.strip()
    if raw_data:
        items = raw_data.split('\t')
        for item in items:
            # print item
            uid, score = item.split(' ')
            q_u_score[index].append((int(uid), int(score)))

q_num_file = open(ZHIHU_USER_Q_NUMBER, 'w')
q_score_file = open(ZHIHU_USER_Q_SCORE, 'w')
for key in u_q.keys():
    num_of_q = u_q[key]['num']
    q_num_file.write(''.join([
        str(num_of_q),
        '\n'
        ]))
    sum_score = 0
    q_score_file.write(''.join([
        str(num_of_q),
        ' '
        ]))
    # calculate the scores
    for qid in u_q[key]['qid']:
        candidate_list = q_u_score[qid]
        for uid, score in candidate_list:
            if uid == key:
                sum_score += score
    if num_of_q != 0:
        avg = sum_score / num_of_q
    else:
        avg = 0
    print avg
    q_score_file.write(''.join([
        str(avg),
        '\n'
        ]))

q_num_file.close()
q_score_file.close()
