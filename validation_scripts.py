def validate_name(inp:str) -> bool:
    for chr in inp.lower():
        if chr not in "qwertyuiopasdfghjklzxcvbnm -_":
            return False
    return True

def validate_class(inp:str) -> bool:
    for chr in inp.lower():
        if chr not in "qwertyuiopasdfghjklzxcvbnm":
            return False
    return True

def validate_int(inp:str) -> bool:
    try:
        int(inp)
    except:
        return False
    return True