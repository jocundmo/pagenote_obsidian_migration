import codecs
import json
import os
import re

from src import util
from urllib.parse import unquote, quote

vault_index_path = "../vault_index.txt"
# backup_file_path = "../0.23.6_chrome_backup_2022-11-18-22-45_154.pagenote.txt"
backup_file_path = "../2022-11-22_13_41_34_fixed.pagenote.bak"
pagenote_ver = 24  # 23 or 24

with codecs.open(vault_index_path, mode='r', encoding='utf-8') as f:
    vault_index = json.load(f)


def walk_and_fixed_pagenotes(pagenote_path):
    invalid_htmls = list()
    with codecs.open(pagenote_path, mode='r', encoding='utf-8') as f:
        content = f.read()
        if pagenote_ver < 24:
            content = unquote(content)
        page_note_main = json.loads(content)
        page_note_list = page_note_main["pages"]

    # build "lights" index
    light_index = dict()
    for light in page_note_main["lights"]:
        if light["pageKey"] in light_index:
            light_index[light["pageKey"]].append(light)  # 这里的light应该是个列表
        else:
            light_index[light["pageKey"]] = [light]

    for page_note in page_note_list:
        if page_note["pageType"] == "http":  # or "http"
            # health check
            pageKey_in_light = page_note["key"]  # backup the origin key before replace it with updated one
            decoded_key = unquote(page_note["key"])
            decoded_filename = decoded_key.split("/")[-1]

            # decoded_path = unquote(page_note["path"])
            # decoded_filename = decoded_path.split("/")[-1]
            is_health, reason = util.valid_check(decoded_filename)
            if not is_health:
                invalid_htmls.append((decoded_filename, reason))
                continue
            file_title, file_index = page_note["key"].split("/")[-1].rsplit("_", maxsplit=1)
            file_index = file_index.rstrip(".html")
            # TODO: could support entire vault relocation, thus assign a new base path is enough.
            if file_index not in vault_index:  # 若pagenote中的标注所指的原文章在vault中不存在
                invalid_htmls.append((unquote(page_note["path"]), "此标注在vault中不存在"))
                continue
            target_path = vault_index[file_index]
            driver = util.fregex(r"^[A-Z]:", target_path, 0)[0]
            # print(f"driver is {driver}...")
            target_path = target_path.lstrip(driver)  # strip driver bcoz colon could be quoted
            encoded_target_path = util.quote_safe(target_path)
            encoded_target_path = driver + encoded_target_path
            # target_path = os.path.join(target_base_path, encoded_relative_path)
            page_note["key"] = f"file:///{encoded_target_path}"
            page_note["path"] = f"/{encoded_target_path}"
            page_note["url"] = f"file:///{encoded_target_path}"
            page_note["urls"] = page_note["url"].split("file://")

            if pagenote_ver > 23:
                for light in light_index[pageKey_in_light]:
                    light["pageKey"] = f"file:///{encoded_target_path}"
                    light["url"] = f"file:///{encoded_target_path}"

    print(f"{len(invalid_htmls)} html files are invalid")

    dir_name = os.path.dirname(pagenote_path)
    f_name = pagenote_path[len(dir_name) + 1:]
    f_name_no_ext = f_name.rsplit(".", maxsplit=1)[0]
    ext_name = f_name.rsplit(".", maxsplit=1)[1] if len(f_name.rsplit(".", maxsplit=1)) >= 2 else None
    file_path_to_write = os.path.join(dir_name, f"modified_{f_name_no_ext}.{ext_name}").replace("\\", "/")
    with codecs.open(file_path_to_write, mode="w", encoding="utf-8") as f:
        output = json.dumps(page_note_main)
        if pagenote_ver < 24:
            f.write(quote(output))
        else:
            f.write(output)


if __name__ == "__main__":
    walk_and_fixed_pagenotes(backup_file_path)
# pageType = "file"
# key = "file:///E:/diskstation/03_Clips/02%E6%8A%80%E6%9C%AF%E7%A7%AF%E7%B4%AF/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/CV/%E4%BD%A0%E4%B8%80%E5%AE%9A%E4%BB%8E%E6%9C%AA%E7%9C%8B%E8%BF%87%E5%A6%82%E6%AD%A4%E9%80%9A%E4%BF%97%E6%98%93%E6%87%82%E7%9A%84YOLO%E7%B3%BB%E5%88%97(%E4%BB%8Ev1%E5%88%B0v5)%E6%A8%A1%E5%9E%8B%E8%A7%A3%E8%AF%BB(%E4%B8%8A)_4db82c7855bfc02158b24ad6c00ef0a9ec526f45.html"
# path = "/E:/diskstation/03_Clips/02%E6%8A%80%E6%9C%AF%E7%A7%AF%E7%B4%AF/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/CV/%E4%BD%A0%E4%B8%80%E5%AE%9A%E4%BB%8E%E6%9C%AA%E7%9C%8B%E8%BF%87%E5%A6%82%E6%AD%A4%E9%80%9A%E4%BF%97%E6%98%93%E6%87%82%E7%9A%84YOLO%E7%B3%BB%E5%88%97(%E4%BB%8Ev1%E5%88%B0v5)%E6%A8%A1%E5%9E%8B%E8%A7%A3%E8%AF%BB(%E4%B8%8A)_4db82c7855bfc02158b24ad6c00ef0a9ec526f45.html"
# url = "file:///E:/diskstation/03_Clips/02%E6%8A%80%E6%9C%AF%E7%A7%AF%E7%B4%AF/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0&%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0/CV/%E4%BD%A0%E4%B8%80%E5%AE%9A%E4%BB%8E%E6%9C%AA%E7%9C%8B%E8%BF%87%E5%A6%82%E6%AD%A4%E9%80%9A%E4%BF%97%E6%98%93%E6%87%82%E7%9A%84YOLO%E7%B3%BB%E5%88%97(%E4%BB%8Ev1%E5%88%B0v5)%E6%A8%A1%E5%9E%8B%E8%A7%A3%E8%AF%BB(%E4%B8%8A)_4db82c7855bfc02158b24ad6c00ef0a9ec526f45.html"
print("done")

