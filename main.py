import codecs
import json
from urllib.parse import unquote

with codecs.open("0.23.6_chrome_backup_2022-11-18-22-45_154.pagenote.txt", mode='r', encoding='utf-8') as f:
    content = f.read()
    clean_content = unquote(content)
    print(clean_content)
    definition = json.loads(clean_content)
print("done")