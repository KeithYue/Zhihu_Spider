from zhihu_config import *

user_id_file = open(ZHIHU_USER_ID, 'r')
ut_file = open(ZHIHU_U_T_PATH, 'r')
username_topic = {}

ut_output = open(ZHIHU_USER_TOPIC_PATH, 'w')

for line in user_id_file.readlines():
    name, id = line.strip().split('\t')
    username_topic[name] = []

for line in ut_file.readlines():
    username, topics = line.strip().split('\t')
    topics = topics.split(' ')
    if not username_topic.has_key(username):
        username_topic[username] = []
    for topic in topics:
        username_topic[username].append(topic)

user_id_file.seek(0)
# print username_topic
for line in user_id_file.readlines():
    name, id = line.strip().split('\t')
    this_topics = username_topic[name]
    print this_topics
    ut_output.write(' '.join(this_topics))
    ut_output.write('\n')




