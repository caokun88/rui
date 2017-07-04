# /usr/bin/env python
# coding=utf8

import datetime
import json
import urllib

import requests

from constant import ALI_DICT
from common import get_ali_pay_sign


def api_ali_pay(return_url, subject, out_trade_no, product_code, fee, product_intro):
    params = {
        "app_id": ALI_DICT['app_id'],
        "method": ALI_DICT['pay_order_method'],
        "format": ALI_DICT['format'],
        "charset": ALI_DICT['charset'],
        "sign_type": ALI_DICT['sign_type'],
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": ALI_DICT['version'],
        "notify_url": ALI_DICT['notify_url'],
        "return_url": return_url,
        "biz_content": json.dumps({
            "body": product_intro,
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": str(float(fee) / 100),  # 单位为元
            "product_code": product_code
        })
    }
    sign = get_ali_pay_sign(params)
    params["sign"] = sign
    res = requests.get(
        url='{}?{}'.format(ALI_DICT['host'], urllib.urlencode(params))
    )
    try:
        url=res.url
    except Exception as e:
        url = ''
    return url


def api_ali_refund_fee(order_id, refund_fee, remark, refund_type):
    """
    阿里支付退款
    :param order_id: 商户订单id
    :param refund_fee: 退款金额（单位，分）
    :param remark: 退款备注
    :param refund_type: 退款类型
    :return:
    """
    order_obj = Order.objects.filter(id=order_id).first()
    refund_dict = {
        'app_id': ALI_DICT["app_id"], 'method': ALI_DICT['refund_method'], 'format': ALI_DICT['format'],
        'charset': ALI_DICT['charset'],
        'sign_type': 'RSA2', 'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "version": ALI_DICT['version'],
        'biz_content': json.dumps({
            'out_trade_no': order_id, 'refund_amount': float(refund_fee / 100.0)
        })
    }
    sign = get_ali_pay_sign(refund_dict)
    refund_dict["sign"] = sign
    res = requests.get(
        url='{}?{}'.format(ALI_DICT['host'], urllib.urlencode(refund_dict))
    )
    resp_data = res.json()
    if resp_data['alipay_trade_refund_response']['code'] in [10000, '10000']:
        try:
            order_obj.refund_fee = order_obj.refund_fee + refund_fee
            order_obj.refund_remark = remark
            order_obj.refund_type = refund_type
            order_obj.refund_time = resp_data['alipay_trade_refund_response'].get('gmt_refund_pay', datetime.datetime.now())
            order_obj.status = 3
            order_obj.save()
            # 自己的业务逻辑
        except Exception as e:
            print e
        return 'success'
    elif resp_data['alipay_trade_refund_response']['code'] in [20000, '20000']:
        # 服务不可用
        pass
    elif resp_data['alipay_trade_refund_response']['code'] in [40004, '40004']:
        # 有可能私钥或者公钥有误（我就是因为这个原因，查了好久）
        return 'has been refunded'
    return None
