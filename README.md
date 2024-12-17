# 改进后的Joux三方密钥交换协议应用程序
HUST 网络空间安全学院 密码学协议结课作业之一
简单地实现了基于Joux三方密钥交换协议的改进版本，包含生成临时私钥和公钥、签名、以及计算共享密钥的完整流程。

改进版本的协议具有如下安全性：
* 抗中间人攻击
* 具有前向安全性
* 抗临时密钥泄露攻击
* 抗密钥泄露伪装攻击

# 使用方法
## 安装pycryptodome库
```bash
pip3 install pycryptodome
```
## 安装pymcl库
项目地址：https://github.com/Jemtaly/pymcl

> 强烈推荐linux环境(Debian系)，作者在Windows上安装该库遇到了许多错误且并未解决

```bash
git clone https://github.com/Jemtaly/pymcl
cd pymcl
./install.sh
```

## 运行
```bash
python key_exchange.py
```
