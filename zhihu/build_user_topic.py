import json
import sys

input_file_path = sys.argv[1]
outpu_file_path = sys.argv[2]

input_file = open(input_file_path, 'r')
output_file = open(outpu_file_path, 'w')

u_t = {}
for line in input_file.xreadlines():
    item = json.loads(line.strip())
    if not u_t.has_key(item['user_url']):
        u_t[item['user_url']] = []
    if not item['topic_url'] in u_t[item['user_url']]:
        u_t[item['user_url']].append(item['topic_url'])

# output the result

for key, value in u_t.iteritems():
    output_file.write(str(key))
    output_file.write('\t')
    for herf in value:
        output_file.write(''.join([
            herf,
            ' '
            ]))
    output_file.write('\n')

print 'Over!!!!'
# print u_t['/people/qin-hao-59']
