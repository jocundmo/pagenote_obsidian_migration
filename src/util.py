import re


def valid_check(filename):
    factors = filename.rsplit("_", maxsplit=1)

    if len(factors) != 2:
        if len(factors) > 1 and factors[1].strip() == "":
            return False, "索引号为空"
        else:
            return False, "_符号不是exactly两个"
    else:
        return True, None


def encode_min(url):
    return url.replace(" ", "%20").replace(":", "%3A").replace("/", "%2F").replace("?", "%3F")\
        .replace("#", "%23").replace("[", "%5B").replace("]", "%5D").replace("@", "%40")\
        .replace("!", "%21").replace("$", "%24").replace("&", "%26").replace("'", "%27").replace("(", "%28").replace(")", "%29")\
        .replace("*", "%2A").replace("+", "%2B").replace(",", "%2C").replace(";", "%3B").replace("?", "%3F")


def fregex(pattern, text, index):
    pattern = re.compile(pattern, flags=re.IGNORECASE)
    res = pattern.search(text)
    lst = []
    while res:
        start, end = res.span()
        if isinstance(index, list):
            lst.append([res.group(i) for i in index])
        else:
            lst.append(res.group(index))
        res = pattern.search(text, start + 1)

    return lst