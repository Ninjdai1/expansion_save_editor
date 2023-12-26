def byteArrayFromFile(path: str):
    with open(path, "rb") as file:
        data = bytearray(file.read())
    return data

def readstring(text):
    chars = "0123456789!?.-         ,  ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    ret = ""
    for i in text:
        c = int(i) - 161
        if c<0 or c>len(chars):
            ret = ret + " "
        else:
            ret = ret + chars[c]
    return ret.strip()
