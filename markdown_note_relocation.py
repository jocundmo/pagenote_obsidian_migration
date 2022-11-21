import codecs
import json
import re

vault_index_path = "vault_index.txt"


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
        target_link = f"[本地知识库](file:///{target_path})"
        content = content.replace(link[0], target_link)

with codecs.open("modified_" + note_path, mode="w", encoding="utf-8") as f:
    # output = json.dumps(content, ensure_ascii=False)
    f.write(content)

    # clean_content = unquote(content)
    # print(clean_content)
    # page_note_main = json.loads(clean_content)
    # page_note_list = page_note_main["pages"]