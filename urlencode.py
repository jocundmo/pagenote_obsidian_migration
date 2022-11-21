url = "file:///E:/diskstation/03_Clips/39综合收藏/小米手 机解锁及线刷教程_167d24a570d126e5b5182c7f805dda7d54e814e1.html"


def encode_min(url):
    return url.replace(" ", "%20").replace(":", "%3A").replace("/", "%2F").replace("?", "%3F")\
        .replace("#", "%23").replace("[", "%5B").replace("]", "%5D").replace("@", "%40")\
        .replace("!", "%21").replace("$", "%24").replace("&", "%26").replace("'", "%27").replace("(", "%28").replace("(", "%29")\
        .replace("*", "%2A").replace("+", "%2B").replace(",", "%2C").replace(";", "%3B").replace("?", "%3F")

# def decode_min()
result = encode_min(url)
print(result)