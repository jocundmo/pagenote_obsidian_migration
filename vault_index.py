import os

startDir = "E:/diskstation/03_Clips"

htmls_count = 0
all_count = 0
files_not_html = list()
htmls_not_valid = list()
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
            is_health = True
            if len(factors) != 2:
                is_health = False
                if len(factors) > 1 and factors[1].strip() == "":
                    htmls_not_valid.append((filename, "索引号为空"))
                else:
                    htmls_not_valid.append((filename, "超过或少于两个_"))

            # make index
            if is_health:
                html_title = factors[0]
                html_index = factors[1]
                if html_index in vault_index:
                    duplicated_index.append(filename)
                else:
                    vault_index[html_index] = full_path
        else:
            files_not_html.append(filename)

print(f"{htmls_count} html files counted")
print(f"{all_count} all files counted")
print(f"{len(files_not_html)} files not html")
print(files_not_html)
print(f"{len(htmls_not_valid)} htmls not valid")
print(htmls_not_valid)