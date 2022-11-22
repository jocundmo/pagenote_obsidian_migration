import codecs
import json
import os

from src import util

# startDir = "D:/Clips_migration_testing"
startDir = "E:/diskstation/03_Clips"
indexPath = "../vault_index.txt"
invalidHtmlsPath = "../invalid_html_list.txt"
duplicatedIndexPath = "../duplicated_index_list.txt"


def walk_through_vault(vault_base_path):
    vault_index = dict()
    files_not_html = list()
    invalid_htmls = list()
    duplicated_index = list()

    htmls_count = 0
    all_count = 0
    for dirpath, dirnames, filenames in os.walk(vault_base_path):
        for filename in filenames:
            relative_path = dirpath.replace(vault_base_path, "")  # strip the leading path

            all_count += 1
            if filename.endswith(".html"):
                full_path = os.path.join(dirpath, filename).replace("\\", "/")
                htmls_count += 1
                print(filename)

                # health check
                is_health, reason = util.valid_check(filename)
                if not is_health:
                    invalid_htmls.append((filename, reason))

                # make index
                factors = filename.rsplit("_", maxsplit=1)  # 确保最后的是signature作为index
                if is_health:
                    html_title = factors[0]
                    html_index = factors[1].rstrip(".html")
                    if html_index in vault_index:
                        duplicated_index.append(filename)
                    else:
                        vault_index[html_index] = full_path
            else:
                files_not_html.append(filename)

    print(f"{all_count} files scanned, {htmls_count} are html files. {len(files_not_html)} are not.")

    print(f"{len(invalid_htmls)} html files are invalid, {len(duplicated_index)} html files are duplicated.")
    print(f"writing invalid html list to file {invalidHtmlsPath}")
    with codecs.open(invalidHtmlsPath, mode="w", encoding="utf-8") as f:
        json.dump(invalid_htmls, f, ensure_ascii=False, indent=2)

    print(f"{len(vault_index)} totally indexed.")
    print(f"writing duplicated index list to file {duplicatedIndexPath}")
    with codecs.open(duplicatedIndexPath, mode="w", encoding="utf-8") as f:
        json.dump(duplicated_index, f, ensure_ascii=False, indent=2)

    return vault_index


if __name__ == "__main__":
    index = walk_through_vault(startDir)
    print(f"writing index to {indexPath}")
    with codecs.open(indexPath, mode="w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False)
    print(f"vault index done")