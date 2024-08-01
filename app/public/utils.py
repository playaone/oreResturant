def trans_id():
    import random
    code = str(int.from_bytes(random.randbytes(8), 'big'))
    return code[0:4] + "-" + code[4:8] + "-" + code[8:12] + "-" + code[12:16]