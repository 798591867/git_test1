from hashlib import sha1


# TODO 定义一个用来对密码进行加密的方法
def get_hash(str):
    sh = sha1()
    sh.update(str.encode('utf8'))
    return sh.hexdigest()

