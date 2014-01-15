from zhihu_config import *

user_file = open(ZHIHU_U_PATH, 'r')

user_id_file = codecs.open(ZHIHU_USER_ID, 'w', 'utf-8')

users = json.loads(user_file.read())

have_saved = set()

i = 0
for index, user in enumerate(users):
    if user.has_key('url'):
        if user['url'] not in have_saved:
            have_saved.add(user['url'])
            print user['url']
            user_id_file.write(''.join([
                user['url'],
                '\t',
                str(i),
                '\n'
                ]))
            i += 1

user_file.close()
user_id_file.close()
