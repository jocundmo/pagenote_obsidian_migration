import codecs
import json
import os
from src import util
from urllib.parse import unquote, quote

vault_index_path = "../vault_index.txt"
startDir = "E:/ObsidianVault/Personal"
# startDir = "E:/ObsidianVault/Personal_testing"

ignored_folders = [".git", ".obsidian", ".trash"]
turn_on_backup = False
do_write_disk = True
markdown_note_title = "本地知识库"


def walk_and_fixed_markdown_note(vault_path, index_path):
    replaced_count = 0
    with codecs.open(index_path, mode='r', encoding='utf-8') as f:
        vault_index = json.load(f)
    for dirpath, dirnames, filenames in os.walk(startDir):
        dirnames[:] = list(set(dirnames) - set(ignored_folders))
        for filename in filenames:
            relative_path = dirpath.replace(startDir, "")  # strip the leading path
            if filename.endswith(".md"):
                note_path = os.path.join(dirpath, filename).replace("\\", "/")
                # note_path = "小米手机MIX2解锁刷机.md"
                with codecs.open(note_path, mode='r', encoding='utf-8') as f:
                    content = f.read()
                    vault_links = util.fregex(rf"\[{markdown_note_title}\]\((file:///)?(.*\.html)\)", content, [0, 2])

                    write_to_disk = False
                    for link in vault_links:
                        index = link[1].rsplit("_", maxsplit=1)[-1].rstrip(".html")
                        source_link = link[0].replace("\\", "/")
                        if index not in vault_index:
                            print(f"note link not existed in knowledge base index... {note_path}, {source_link}")
                            continue
                        target_path = vault_index[index]
                        dir = "/".join(target_path.split("/")[0:-1])
                        filename = target_path.split("/")[-1]
                        encoded_filename = util.encode_min(filename)  # 这里已优化成只encode敏感字符，不处理中文
                        encoded_target_path = os.path.join(dir, encoded_filename).replace("\\", "/")
                        target_link = f"[本地知识库](file:///{encoded_target_path})"
                        if source_link.strip() == target_link.strip():
                            print(f"note link is idential... {note_path}, {source_link}")
                            continue

                        if do_write_disk:
                            content = content.replace(source_link, target_link)
                            print(f"replacing note {note_path}... {source_link} -> {target_link}")
                        else:
                            print(f"replacing note {note_path}... {source_link} -> {target_link}")
                        write_to_disk = True

                    if write_to_disk:
                        replaced_count += 1
                        dir_name = os.path.dirname(note_path)
                        f_name = note_path[len(dir_name)+1:]
                        f_name_no_ext = f_name.rsplit(".", maxsplit=1)[0]
                        ext_name = f_name.rsplit(".", maxsplit=1)[1] if len(f_name.rsplit(".", maxsplit=1)) >= 2 else None
                        if turn_on_backup:
                            f_name_no_ext += "_modified"
                        file_path_to_write = os.path.join(dir_name, f"{f_name_no_ext}.{ext_name}").replace("\\", "/")
                        if do_write_disk:
                            with codecs.open(file_path_to_write, mode="w", encoding="utf-8") as f:
                                # output = json.dumps(content, ensure_ascii=False)
                                f.write(content)
    print(f"{replaced_count} notes are replaced.")


if __name__ == "__main__":
    walk_and_fixed_markdown_note(startDir, vault_index_path)