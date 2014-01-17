from zhihu_config import *

a_file = open(ZHIHU_A_PATH, 'r')
uid_file = open(ZHIHU_USER_ID, 'r')
qids_file = open(ZHIHU_ITEM_ID, 'r')

answers = json.loads(a_file.read())

user_adj_file = open(ZHIHU_USER_ADJ, 'w')

u_q_pair = {}
qid = {}
uid = {}

for line in qids_file.readlines():
    raw_dat = line.strip()
    oid, nid = raw_dat.split('\t')
    qid[int(oid)] = nid

for answer in answers:
    if answer['asr'].has_key('url'):
        u_q_pair.setdefault(answer['asr']['url'], []).append(answer['qid'])

# for line in uid_file.readlines():
#     raw_dat = line.strip()
#     user_url = raw_dat.split('\t')[0]
#     user, his_answers =  user_url, u_q_pair.get(user_url, [])
#     print user, his_answers
#     user_adj_file.write(''.join([
#         str(len(his_answers)),
#         ' '
#         ]))
#     for ans in his_answers:
#         user_adj_file.write(''.join([
#             str(qid[ans]),
#             ' '
#             ]))
#     user_adj_file.write('\n')
#
#     # a = input('please input a integer')

print 'over!!!'
