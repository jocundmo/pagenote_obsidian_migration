import os

startDir = "E:/diskstation/03_Clips"

htmls_count = 0
all_count = 0
files_not_html = list()
htmls_not_valid = list()

for dirpath, dirnames, filenames in os.walk(startDir):
    for filename in filenames:
        relative_path = dirpath.replace(startDir, "")  # strip the leading path
        all_count += 1
        if filename.endswith(".html"):
            htmls_count += 1
            print(filename)
            factors = filename.split("_")
            if len(factors) != 2:
                if len(factors) > 1 and factors[1].strip() == "":
                    htmls_not_valid.append((filename, "索引号为空"))
                else:
                    htmls_not_valid.append((filename, "超过或少于两个_"))
        else:
            files_not_html.append(filename)

print(f"{htmls_count} html files counted")
print(f"{all_count} all files counted")
print(f"{len(files_not_html)} files not html")
print(files_not_html)
print(f"{len(htmls_not_valid)} htmls not valid")
print(htmls_not_valid)