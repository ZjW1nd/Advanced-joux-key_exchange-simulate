# pymcl: https://github.com/Jemtaly/pymcl
import pymcl
import hashlib
from signature import Signature

# 生成临时私钥和临时公钥
def generate_key_pair(g1,g2):
    priv_key = pymcl.Fr.random()  # 随机生成私钥
    pub_key1 = g1*priv_key  # 计算公钥
    pub_key2 = g2*priv_key 
    return priv_key, pub_key1, pub_key2

# 计算共享密钥
def compute_shared_key(priv_key,pub_11,pub_22):
    # 由于pymcl这个库不支持e(g,g)的操作，它内部的实现要求pair必须是g1和g2的对象
    # 所以我们将具体的实现稍作修改，最后的密钥采用如下方式实现，也是一样的：
    # K= e(g1,g2)^{abc}
    shared_key = pymcl.pairing(pub_11,pub_22)**priv_key
    return shared_key

# 计算hash看是不是一样
def final_key(shared_key):
    h = hashlib.sha256()
    h.update(shared_key.serialize())
    return h.digest()

if __name__ == "__main__":
    #----------初始化----------
    g1 = pymcl.g1 # generator of G1
    g2 = pymcl.g2 # generator of G2
    # 生成临时私钥和公钥
    priv_A, pub_A1, pub_A2 = generate_key_pair(g1,g2)
    priv_B, pub_B1, pub_B2 = generate_key_pair(g1,g2)
    priv_C, pub_C1, pub_C2 = generate_key_pair(g1,g2)
    signing_B=Signature()
    signing_C=Signature()
    #----------发送(Pub,R,sig)并验证----------
    # 仅举例，以B,C发送给A为例
    message_C=pub_C1.serialize()+pub_C2.serialize()
    message_B=pub_B1.serialize()+pub_B2.serialize()
    sign_C=signing_C.sign(message_C)
    sign_B=signing_B.sign(message_B)
    # A收到了(Pub_B, R_B, sig_B)和(Pub_C, R_C, sig_C)
    if(signing_C.verify(message_C, sign_C)==True):
        print("C的签名验证成功！")
    else:
        print("C的签名验证失败！")
    if(signing_B.verify(message_B, sign_B)==True):
        print("B的签名验证成功！")
    else:
        print("B的签名验证失败！")
    #----------基于双线性配对的密钥导出----------
    # 计算三方共享密钥
    K_A = compute_shared_key(priv_A, pub_B1, pub_C2) 
    K_B = compute_shared_key(priv_B, pub_C1, pub_A2) 
    K_C = compute_shared_key(priv_C, pub_A1, pub_B2) 
    # 密钥转换为可读形式顺便过一次hash
    key_A = final_key(K_A)
    key_B = final_key(K_B)
    key_C = final_key(K_C)
    # 检测
    assert key_A == key_B == key_C, "共享密钥不一致！"
    print("共享密钥 A:", key_A.hex())
    print("共享密钥 B:", key_B.hex())
    print("共享密钥 C:", key_C.hex())