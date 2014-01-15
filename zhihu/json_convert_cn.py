# the original json is encoded in utf-8 and is shown in ascii in text editor,
# This script is used to convert the json in utf-8 shown, notice that the encoding of both files is utf-8
import json
import sys
import codecs

file_path = sys.argv[1]
file_output_path = ''.join(sys.argv[1].split('.')[:-1]) + '.cn.json'

json_file = codecs.open(file_path, 'r', encoding='utf-8')
json_output_file = codecs.open(file_output_path, 'w', encoding='utf-8')

json_obj = json.loads(json_file.read())

json.dump(json_obj, json_output_file, ensure_ascii=False)
