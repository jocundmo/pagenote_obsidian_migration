import codecs
import json
import os

# startDir = "D:/Clips_migration_testing"
startDir = "E:/diskstation/03_Clips"
indexPath = "vault_index.txt"

htmls_count = 0
all_count = 0
files_not_html = list()
invalid_htmls = list()
duplicated_index = list()

vault_index = dict()

for dirpath, dirnames, filenames in os.walk(startDir):
    for filename in filenames:
        relative_path = dirpath.replace(startDir, "")  # strip the leading path

        all_count += 1
        if filename.endswith(".html"):
            full_path = os.path.join(dirpath, filename).replace("\\", "/")
            htmls_count += 1
            print(filename)
            factors = filename.split("_")

            # health check
            from health_check import valid_check
            is_health, reason = valid_check(filename)
            if not is_health:
                invalid_htmls.append((filename, reason))
            # is_health = True
            # if len(factors) != 2:
            #     is_health = False
            #     if len(factors) > 1 and factors[1].strip() == "":
            #         invalid_htmls.append((filename, "索引号为空"))
            #     else:
            #         invalid_htmls.append((filename, "超过或少于两个_"))

            # make index
            if is_health:
                html_title = factors[0]
                html_index = factors[1].rstrip(".html")
                if html_index in vault_index:
                    duplicated_index.append(filename)
                else:
                    vault_index[html_index] = full_path
        else:
            files_not_html.append(filename)

print(f"{all_count} files scanned, {htmls_count} are html files. {len(files_not_html)} are not html files.")
print(f"{len(invalid_htmls)} html files are invalid, {len(duplicated_index)} html files are duplicated.")
print(f"{len(vault_index)} totally indexed.")

print(f"writing index to {indexPath}")
# with open(indexPath, mode="w", encoding='utf-8') as f:
#     json.dump(vault_index, f, ensure_ascii=False)
with codecs.open(indexPath, mode="w", encoding="utf-8") as f:
    json.dump(vault_index, f, ensure_ascii=False)
print(f"vault index done")
# print(f"{htmls_count} html files counted")
# print(f"{all_count} all files counted")
# print(f"{len(files_not_html)} files not html")
# print(files_not_html)
# print(f"{len(invalid_htmls)} htmls not valid")
# print(invalid_htmls)