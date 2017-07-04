# /usr/bin/env python
# coding=utf8

import json
import os

import redis
import requests

from constant import PAY_DICT, DICT, API_URL_DICT, TIMEOUT_ACCESS_token, ACCESS_TOKEN_KEY
from common import get_xml_from_dict, generate_nonce_str


pool = redis.ConnectionPool(
    host='127.0.0.1',
    port=6379,
    db=0,
    password=None
)

redis_conn = redis.StrictRedis(connection_pool=pool)

# 统一下单请求数据
data = {
    "appid": PAY_DICT["app_id"],
    "mch_id": PAY_DICT["mchid"],
    "nonce_str": generate_nonce_str(),
    "body": 'product_name',
    "out_trade_no": 'order_id',
    "total_fee": 'total_fee',
    "spbill_create_ip": PAY_DICT["ip"],
    "notify_url": API_URL_DICT["pay_callback_url"],
    "trade_type": 'trade_type',
    "product_id": 'product_id',
    'openid': 'openid'  # 如果有就用，没有就不用
}


def api_wechat_unified_order(param_dict):
    """
    微信统一下单
    :param param_dict: 下单数据字典
    :return: resp_dict
    :rtype: dict
    trade_type == native: code_url(这个是扫码支付的链接，需要自己转成二维码)
    trade_type == jsapi: 详细看文档
    trade_type = app: 详细看文档
    """
    url = API_URL_DICT['unified_order_url']
    req_xml = get_xml_from_dict(param_dict)
    resp_str = requests.post(url=url, data=req_xml)
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
        print e
    return resp_dict


refund_dict = {
    'appid': PAY_DICT["app_id"],
    'mch_id': PAY_DICT["mchid"],
    'out_trade_no': 'order_id',
    'nonce_str': generate_nonce_str(),
    'total_fee': 'int(total_fee)',
    'refund_fee': 'int(refund_fee)',
    'out_refund_no': "str(int(time.time())) + '_' + nonce_str"
}


def api_wechat_refund(param_dict):
    """
    微信退款api
    :param param_dict: 退款参数
    :return: resp_data
    :rtype: dict
    return_code == 'SUCCESS' and result_code == 'SUCCESS', 才是退款api成功，具体退款时间，看情况。
    """
    url = API_URL_DICT['refund_url']
    req_xml = get_xml_from_dict(param_dict)
    dir_name = os.path.dirname((os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    cert_path = os.path.join(dir_name, r'wx_cert/apiclient_cert.pem')  # 证书cert
    cert_key_path = os.path.join(dir_name, r'wx_cert/apiclient_key.pem')  # 证书key
    resp_str = requests.post(url=url, data=req_xml, cert=(cert_path, cert_key_path))
    try:
        resp_data = resp_str.json()
    except Exception as e:
        resp_data = dict()
    return resp_data


def __api_get_access_token():
    """
    获取通用access_token
    :return: access_token
    :rtype: str
    """
    redis_access_token = redis_conn.get(ACCESS_TOKEN_KEY)
    if redis_access_token:
        return redis_access_token
    app_id, secret = DICT['app_id'], DICT['secret']
    url = API_URL_DICT['access_token_url']
    resp_str = requests.get(
        url=url.format(app_id, secret)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    if resp_dict:
        access_token = resp_dict['access_token']
        redis_conn.setex(ACCESS_TOKEN_KEY, TIMEOUT_ACCESS_token, access_token)
    else:
        return None


def api_create_menu(param_dict):
    """
    创建菜单api
    :param param_dict: 菜单内容
    :return: resp_dict
    :rtype: dict
    """
    url = API_URL_DICT['create_menu_url']
    access_token = __api_get_access_token()
    resp_str = requests.post(
        url=url.format(access_token),
        data=json.dumps(param_dict, ensure_ascii=False).encode('utf8')
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_send_template(product_name, openid, click_url):
    """
    发送模板消息api
    :param product_name: 产品名称
    :param openid: 接收模板消息的openid
    :param click_url: 点击跳转的url
    :return: resp_dict
    :rtype: dict
    """
    url = API_URL_DICT['']
    access_token = __api_get_access_token()
    data = {
        'first': {'value': '恭喜你购买成功！', 'color': '#173177'},
        'name': {"value": product_name},
        'remark': {'value': 'REMARK_TEXT'}
    }
    param_data = {
        'touser': openid,
        'template_id': PAY_DICT['pay_template_id'],
        'url': click_url,
        'data': data
    }
    resp_str = requests.post(
        url=url.format(access_token),
        data=json.dumps(param_data, ensure_ascii=False).encode('utf8')
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_get_web_access_token(code):
    """
    获取网页access_token和openid
    :param code: code
    :return: access_token, openid
    :rtype: str, str
    """
    url = API_URL_DICT['web_access_token_url']
    app_id, secret = DICT['app_id'], DICT['secret']
    resp_str = requests.get(
        url=url.format(app_id, secret, code)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    if resp_dict:
        return resp_dict['access_token'], resp_dict['openid']
    return None, None


def api_get_web_user_info(access_token, openid):
    """
    网页授权，获取用户基本信息api
    :param access_token: 网页授权access_token
    :param openid: 用户的openid
    :return: resp_dict
    :rtype: dict
    """
    url = API_URL_DICT['web_user_info_url']
    resp_str = requests.get(
        url=url.format(access_token, openid)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict


def api_get_user_info(openid):
    """
    获取用户的基本信息，包括是否关注过该公众号（订阅号或者服务号）
    :param openid: 用户的openid
    :return: resp_dict
    :rtype: dict
    """
    url = API_URL_DICT['user_info_url']
    access_token = __api_get_access_token()
    resp_str = requests.get(
        url=url.format(access_token, openid)
    )
    try:
        resp_dict = resp_str.json()
    except Exception as e:
        resp_dict = dict()
    return resp_dict
