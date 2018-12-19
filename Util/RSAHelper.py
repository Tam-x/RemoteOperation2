import rsa
from Util import LogInfo
import sys
import os

#生成资源文件目录访问路径
def resource_path(relative_path):
    if getattr(sys, 'frozen', False): #是否Bundle Resource
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

filepubkey = resource_path(os.path.join("Res","public.pem"))
fileprivkey = resource_path(os.path.join("Res","private.pem"))
# 导入密钥

#加密
def encrypted_msg(message):
    with open(filepubkey, 'r') as f:
        pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())
    crypto = rsa.encrypt(message.encode(), pubkey)
    code = str(crypto.hex())
    LogInfo.put(code)

#解密
def decrypt_msg(msg):
    with open(fileprivkey, 'r') as f:
        privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
        code = rsa.decrypt(bytes.fromhex(msg), privkey).decode()
        return code