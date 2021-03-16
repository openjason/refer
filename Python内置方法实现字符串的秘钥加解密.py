Python内置方法实现字符串的秘钥加解密,介绍了利用Python内置方法实现字符串的秘钥加解密
在实际编程开发中，我们会使用到各类的加密算法来对数据和信息进行加密。比如密码中比较常见的MD5加密，以及AES加密等等。
对于密码认证来说，MD5加密是比较适合的，因为其不需要接触到明文的数据，只需要比对MD5加密后的哈希值就能判断数据是否一致；而对于一些在加密后进行解密的数据而言，AES则更加的常用。
在Python中实现AES算法需要借助的第三方库Crypto，其在各个操作系统上的安装方法有些许复杂，所以对于简单的使用有点杀鸡用牛刀的意思。
在Mrdoc的开发过程中，我们就遇到了这样的问题。一方面不想为了一个小小的功能增加一个安装容易出错的第三方库，一方面又有对用户输入的
第三方密码进行加密和解密的需求。最终，我们采用的Python内置的方法实现了。

一、设置一个秘钥
在这个秘钥加解密方案中，我们需要设置一个秘钥，用来对数据进行加密和解密。在Mrdoc中，我们借助Django项目中的SECRET_KEY变量来作为秘钥。原则就是，尽量复杂且长：

key = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
接下来对数据的加密和解密，我们都需要使用到这个秘钥。

二、对数据进行加密

我们的加密逻辑其实很简单，核心是一个Python内置方法ord()，这个方法用于返回一个单字节的ASCII码字符的Unicode码位。加密逻辑步骤如下：

1、创建一个空字符串变量，作为加密字符的初始值；
2、使用zip()方法同时遍历数据字符串和秘钥；
3、使用ord()方法分别获取遍历的数据字符和秘钥字符的Unicode码位，并将其相加，得到此数据字符的加密字符；
4、将得到的加密字符追加到空字符串变量中；
5、返回最终的空字符串变量；
其代码如下所示：
# 加密
def enctry(s):
 k = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
 encry_str = ""
 for i,j in zip(s,k):
  # i为字符，j为秘钥字符
  temp = str(ord(i)+ord(j))+'_' # 加密字符 = 字符的Unicode码 + 秘钥的Unicode码
  encry_str = encry_str + temp
 return encry_str

如果我们将字符串”zmister”使用这个加密方法进行加密，最终会得到如下所示的加密字符串：
'222_215_218_152_169_200_231_'
三、对数据进行解密
与加密的逻辑相反，我们需要把Unicode码位还原为单字节的ASCII码字符，这需要利用到Python的内置方法chr()。所以数据解密的步骤如下所示：
1、定义一个空的字符串变量，作为解密数据的初始值；
2、使用zip()方法同时遍历加密后的数据和秘钥；
3、将加密数据字符减去秘钥字符的Unicode码位，得到原始数据的Unicode码位，然后使用chr()方法将其还原为ASCII单字节字符；
4、将得到的解密字符追加到空字符串变量中；
5、返回解密字符
其代码如下所示：
# 解密
def dectry(p):
 k = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
 dec_str = ""
 for i,j in zip(p.split("_")[:-1],k):
  # i 为加密字符，j为秘钥字符
  temp = chr(int(i) - ord(j)) # 解密字符 = (加密Unicode码字符 - 秘钥字符的Unicode码)的单字节字符
  dec_str = dec_str+temp
 return dec_str
这样，我们就能把加密的数据解密出来。我们用一个完整的代码来测试一下：
# coding:utf-8
# @文件: utils.py
# @创建者：州的先生
# #日期：2019/12/8
# 博客地址：zmister.com
 
# 加密
def enctry(s):
 k = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
 encry_str = ""
 for i,j in zip(s,k):
  # i为字符，j为秘钥字符
  temp = str(ord(i)+ord(j))+'_' # 加密字符 = 字符的Unicode码 + 秘钥的Unicode码
  encry_str = encry_str + temp
 return encry_str
 
# 解密
def dectry(p):
 k = 'djq%5cu#-jeq15abg$z9_i#_w=$o88m!*alpbedlbat8cr74sd'
 dec_str = ""
 for i,j in zip(p.split("_")[:-1],k):
  # i 为加密字符，j为秘钥字符
  temp = chr(int(i) - ord(j)) # 解密字符 = (加密Unicode码字符 - 秘钥字符的Unicode码)的单字节字符
  dec_str = dec_str+temp
 return dec_str
 
data = "zmister.com"
print("原始数据为：",data)
enc_str = enctry(data)
print("加密数据为：",enc_str)
dec_str = dectry(enc_str)
print("解密数据为：",dec_str)
运行上述代码，我们会得到如下图所示的结果：
四、最后
可以发现，这个方法对于一般性的数据加解密而言，还是比较简单和便捷的，唯一需要考量的是秘钥的复杂性和安全性，如果有更好地实现方法，欢迎留言讨论：）
ps：Python利用字符串自带函数实现加密和解密
字符串自带的简单加密 
encode = str.maketrans('eilouvy','1234567')#加密方式 
words = 'iloveyou'
encode_words = words.translate(encode)#按encode加密方式加密 
print(encode_words) #输出23461745 
dedoed = str.maketrans('1234567','eilouvy')#解密方式 
dedoed_words = encode_words.translate(dedoed)#按decode解密方式解密 
print(dedoed_words)#输出iloveyou
