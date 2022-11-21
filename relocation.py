import codecs
import json
import os
from urllib.parse import unquote, quote

backup_file_path = "0.23.6_chrome_backup_2022-11-18-22-45_154.pagenote.txt"


vault_index_path = "vault_index.txt"
# source_base_path = "E:/diskstation/03_Clips/"  # 这个其实不用指定，只要把原路径中的头拿掉即可
# target_base_path = "D:/03_Clips/"  # 这个应该从vault index中获取，依据是从原路径中得到的index

with codecs.open(vault_index_path, mode='r', encoding='utf-8') as f:
    vault_index = json.load(f)

with codecs.open(backup_file_path, mode='r', encoding='utf-8') as f:
    content = f.read()
    clean_content = unquote(content)
    print(clean_content)
    page_note_main = json.loads(clean_content)
    page_note_list = page_note_main["pages"]

for page_note in page_note_list:
    if page_note["pageType"] == "file":  # or "http"
        # TODO: missing valid check.
        # encoded_relative_path = page_note["path"].replace(f"/{source_base_path}", "")
        file_title, file_index = page_note["path"].split("/")[-1].split("_")
        file_index = file_index.rstrip(".html")
        # decoded_relative_path = unquote(encoded_relative_path)
        # TODO: could support entire vault relocation, thus assign a new base path is enough.
        if file_index not in vault_index:
            continue
        target_path = vault_index[file_index]
        target_path = target_path.lstrip("D:")  #
        encoded_target_path = quote(target_path)
        encoded_target_path = "D:" + encoded_target_path
        # target_path = os.path.join(target_base_path, encoded_relative_path)
        page_note["key"] = f"file:///{encoded_target_path}"
        page_note["path"] = f"/{encoded_target_path}"
        page_note["url"] = f"file:///{encoded_target_path}"
        page_note["urls"] = page_note["url"].split("file://")

with codecs.open("modified_" + backup_file_path, mode="w", encoding="utf-8") as f:
    output = json.dumps(page_note_main)
    f.write(quote(output))

# pageType = "file"
# key = "file:///E:/diskstation/03_Clips/02%E6%8A%80%E6%9C%AF%E7%A7%AF%E7%B4%AF/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/CV/%E4%BD%A0%E4%B8%80%E5%AE%9A%E4%BB%8E%E6%9C%AA%E7%9C%8B%E8%BF%87%E5%A6%82%E6%AD%A4%E9%80%9A%E4%BF%97%E6%98%93%E6%87%82%E7%9A%84YOLO%E7%B3%BB%E5%88%97(%E4%BB%8Ev1%E5%88%B0v5)%E6%A8%A1%E5%9E%8B%E8%A7%A3%E8%AF%BB(%E4%B8%8A)_4db82c7855bfc02158b24ad6c00ef0a9ec526f45.html"
# path = "/E:/diskstation/03_Clips/02%E6%8A%80%E6%9C%AF%E7%A7%AF%E7%B4%AF/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/CV/%E4%BD%A0%E4%B8%80%E5%AE%9A%E4%BB%8E%E6%9C%AA%E7%9C%8B%E8%BF%87%E5%A6%82%E6%AD%A4%E9%80%9A%E4%BF%97%E6%98%93%E6%87%82%E7%9A%84YOLO%E7%B3%BB%E5%88%97(%E4%BB%8Ev1%E5%88%B0v5)%E6%A8%A1%E5%9E%8B%E8%A7%A3%E8%AF%BB(%E4%B8%8A)_4db82c7855bfc02158b24ad6c00ef0a9ec526f45.html"
# url = "file:///E:/diskstation/03_Clips/02%E6%8A%80%E6%9C%AF%E7%A7%AF%E7%B4%AF/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/CV/%E4%BD%A0%E4%B8%80%E5%AE%9A%E4%BB%8E%E6%9C%AA%E7%9C%8B%E8%BF%87%E5%A6%82%E6%AD%A4%E9%80%9A%E4%BF%97%E6%98%93%E6%87%82%E7%9A%84YOLO%E7%B3%BB%E5%88%97(%E4%BB%8Ev1%E5%88%B0v5)%E6%A8%A1%E5%9E%8B%E8%A7%A3%E8%AF%BB(%E4%B8%8A)_4db82c7855bfc02158b24ad6c00ef0a9ec526f45.html"
print("done")

