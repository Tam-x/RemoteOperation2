# #!/usr/bin/python

import rsa
# 生成密钥
# (pubkey, privkey) = rsa.newkeys(1024)

# 保存密钥
# with open('public.pem', 'w+') as f:
#     f.write(pubkey.save_pkcs1().decode())
#
# with open('private.pem', 'w+') as f:
#     f.write(privkey.save_pkcs1().decode())

#
# # 明文
# message = 'hello'
#
# # 公钥加密
# # crypto = rsa.encrypt(message.encode(), pubkey)
# # print(crypto.hex())
# # 私钥解密
# message = rsa.decrypt(bytes.fromhex('75af677da85be550669b101f510b1ca7e5cfe1e6bd90058d7e36b43ccf1df99d4ccaf4bbd25d043157eaa0fd269f71ebb130f70138560a7f2f2fcce8d699f706e6a26a416811cc3036758193d1edb032182ea602151d1472cc84d6548d488c9559106b34d0f7b87bebbf3b09b778773ad2b366628b9aa33f0023c22f96b76893'), privkey).decode()
# print(message)

# # 私钥签名
# signature = rsa.sign(message.encode(), privkey, 'SHA-1')
#
# # 公钥验证
# rsa.verify(message.encode(), signature, pubkey)