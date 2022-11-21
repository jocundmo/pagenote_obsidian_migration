
def valid_check(filename):
    factors = filename.split("_")

    if len(factors) != 2:
        if len(factors) > 1 and factors[1].strip() == "":
            return False, "索引号为空"
        else:
            return False, "_符号不是exactly两个"
    else:
        return True, None
