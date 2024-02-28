# -*- coding: utf-8 -*-

"""
兼容Python 2.X 与 3.X 版本
"""

import sys
import appserver


is_py2 = (sys.version_info[0] == 2)
is_py3 = (sys.version_info[0] == 3)


if is_py2:
    import md5
    import urllib2
    from M2Crypto import RSA
    from M2Crypto import BIO
    from BaseHTTPServer import  HTTPServer, BaseHTTPRequestHandler

    def verrify(auth_str, authorization_base64, pub_key):
        """
        校验签名是否正确（MD5 + RAS）
        :param auth_str: 文本信息
        :param authorization_base64: 签名信息
        :param pub_key: 公钥
        :return: 若签名验证正确返回 True 否则返回 False
        """
        auth_md5 = md5.new(auth_str).digest()
        bio = BIO.MemoryBuffer(pub_key)
        rsa_pub = RSA.load_pub_key_bio(bio)
        authorization = authorization_base64.decode('base64')
        result = False
        try:
            result = rsa_pub.verify(auth_md5, authorization, 'md5')
        except:
            result = False
        return result

    def get_http_request_unquote(url):
        return urllib2.unquote(url)


    def get_pub_key(pub_key_url_base64):
        pub_key_url = pub_key_url_base64.decode('base64')
        url_reader = urllib2.urlopen(pub_key_url)
        pub_key = url_reader.read()
        return pub_key


    class MyHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            """处理 POST 请求"""
            return appserver.do_POST(self)

        def do_GET(self):
            """处理 GET 请求"""
            appserver.do_GET(self)


    class MyHTTPServer(HTTPServer):
        def __init__(self, host, port):
            print("run app server by python2!")
            HTTPServer.__init__(self,  (host, port), MyHTTPRequestHandler)

elif is_py3:
    import base64
    import urllib.request
    from http.server import HTTPServer, BaseHTTPRequestHandler
    from Crypto.Signature import PKCS1_v1_5
    from Crypto.Hash import MD5
    from Crypto.PublicKey import RSA


    def verrify(auth_str, authorization_base64, pub_key):
        """
        校验签名是否正确（MD5 + RAS）
        :param auth_str: 文本信息
        :param authorization_base64: 签名信息
        :param pub_key: 公钥
        :return: 若签名验证正确返回 True 否则返回 False
        """
        pub_key_load = RSA.importKey(pub_key)
        auth_md5 = MD5.new(auth_str.encode())
        result = False
        try:
            result = PKCS1_v1_5.new(pub_key_load).verify(auth_md5, base64.b64decode(authorization_base64.encode()))
        except Exception as e:
            print(e)
            result = False
        return result

    def get_http_request_unquote(url):
        return urllib.request.unquote(url)

    def get_pub_key(pub_key_url_base64):
        """ 抽取出 public key 公钥 """
        pub_key_url = base64.b64decode(pub_key_url_base64.encode())
        url_reader = urllib.request.urlopen(pub_key_url.decode())
        pub_key = url_reader.read()
        return pub_key

    class MyHTTPRequestHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            """处理 POST 请求"""
            return appserver.do_POST(self)

        def do_GET(self):
            """处理 GET 请求"""
            appserver.do_GET(self)

    class MyHTTPServer(HTTPServer):
        def __init__(self, host, port):
            print("run app server by python3!")
            HTTPServer.__init__(self,  (host, port), MyHTTPRequestHandler)
