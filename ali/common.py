# /usr/bin/env python
# coding=utf8

import base64

import rsa

from constant import ALI_DICT


def get_ali_pay_sign(params_dict):
    """
    支付宝支付签名生成
    :param params_dict: 需要参与签名的字典
    :return: sign
    :rtype: str
    """
    keys = params_dict.keys()
    keys.sort()
    sign_items = []

    for key in keys:
        if params_dict[key]:
            sign_items.append("{}={}".format(key, params_dict[key]))
    params_str = "&".join(sign_items)

    pri_key = rsa.PrivateKey.load_pkcs1(ALI_DICT["private_key"])
    sign = base64.b64encode(rsa.sign(params_str, pri_key, "SHA-256"))

    return sign


def verity_sign(params={}):
    """
    验证支付宝sign
    :param params: 需要验证的字典
    :return:
    """
    try:
        sign = base64.b64decode(params["sign"])

        del params["sign"]
        del params["sign_type"]

        keys = params.keys()
        keys.sort()
        sign_items = []

        for key in keys:
            sign_items.append(key + u"=" + params[key])
        params_str = u"&".join(sign_items)

        pub_key = rsa.PublicKey.load_pkcs1_openssl_pem(ALI_DICT["pay_public_key"])
        if rsa.verify(params_str.encode("utf-8"), sign, pub_key):
            return True
        else:
            return False
    except Exception as e:
        print e
        return False
