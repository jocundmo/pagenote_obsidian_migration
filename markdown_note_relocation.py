import codecs
import json
import os
import re
from urllib.parse import unquote, quote

vault_index_path = "vault_index.txt"


# from urllib.parse import urlencode
# params2 = {
#     'name': "王二",
#     'extra': "/",
#     'special': '&',
#     'equal': '='}
# base_url = "file:///E:\diskstation\03_Clips\39综合收藏\小米手机 解锁及线刷教程_167d24a570d126e5b5182c7f805dda7d54e814e1.html"
# url2 = base_url + urlencode(params2)
# print("done")

def encode_min(url):
    return url.replace(" ", "%20").replace(":", "%3A").replace("/", "%2F").replace("?", "%3F")\
        .replace("#", "%23").replace("[", "%5B").replace("]", "%5D").replace("@", "%40")\
        .replace("!", "%21").replace("$", "%24").replace("&", "%26").replace("'", "%27").replace("(", "%28").replace("(", "%29")\
        .replace("*", "%2A").replace("+", "%2B").replace(",", "%2C").replace(";", "%3B").replace("?", "%3F")

def fregex(pattern, text, index=0):
    pattern = re.compile(pattern, flags=re.IGNORECASE)
    res = pattern.search(text)
    lst = []
    while res:
        start, end = res.span()
        lst.append(res.group(index))
        res = pattern.search(text, start + 1)

    return lst


with codecs.open(vault_index_path, mode='r', encoding='utf-8') as f:
    vault_index = json.load(f)

note_path = "小米手机MIX2解锁刷机.md"
with codecs.open(note_path, mode='r', encoding='utf-8') as f:
    content = f.read()
    vault_links = fregex(r"\[本地知识库\]\(file:///(.*\.html)\)", content, 0)
    vault_path = fregex(r"\[本地知识库\]\(file:///(.*\.html)\)", content, 1)
    vault_links_zipped = list(zip(vault_links, vault_path))
    for link in vault_links_zipped:
        index = link[1].split("_")[-1].rstrip(".html")
        target_path = vault_index[index]
        dir = "/".join(target_path.split("/")[0:-1])
        filename = target_path.split("/")[-1]
        encoded_filename = encode_min(filename)  # TODO: 这里最好优化成只encode敏感字符，不处理中文
        encoded_target_path = os.path.join(dir, encoded_filename).replace("\\", "/")
        target_link = f"[本地知识库](file:///{encoded_target_path})"
        content = content.replace(link[0], target_link)

with codecs.open("modified_" + note_path, mode="w", encoding="utf-8") as f:
    # output = json.dumps(content, ensure_ascii=False)
    f.write(content)

    # clean_content = unquote(content)
    # print(clean_content)
    # page_note_main = json.loads(clean_content)
    # page_note_list = page_note_main["pages"]