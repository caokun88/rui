# /usr/bin/env python
# coding=ut8

from django.http import HttpResponse

from wechat.common import check_from_wechat_signature, get_dict_from_xml, get_xml_from_dict, check_xml_sign
from wechat.constant import PAY_DICT
from ali.common import verity_sign


# 微信的一些推送消息
def wechat_event_push_view(request):
    signature = request.GET.get('signature', '')
    timestamp = request.GET.get('timestamp', '')
    nonce = request.GET.get('nonce', '')
    echo_str = request.GET.get("echostr", '')
    if request.method == 'GET':
        status = check_from_wechat_signature(signature, timestamp, nonce)
        if status:
            return HttpResponse(echo_str)
        return HttpResponse('not weixin service request')
    else:
        status = check_from_wechat_signature(signature, timestamp, nonce)
        if status:
            xml_str = request.body
            dict_data = get_dict_from_xml(xml_str)
            event = dict_data.get('Event')
            openid = dict_data.get('FromUserName')
            dev_wx = dict_data.get('ToUserName')
            if event in ['subscribe']:
                # 修改表状态
                # 关注后推送消息
                pass
            elif event in ['unsubscribe']:
                # 修改表状态
                pass
            elif event in ['SCAN']:
                # 用户已关注时，扫描带参数二维码事件
                pass
            elif event in ['TEMPLATESENDJOBFINISH']:
                # 模板消息推送事件
                if dict_data.get('Status') == 'success':
                    # 成功
                    pass
                elif dict_data.get('Status') == 'failed:user block':
                    # 用户设置拒绝接收公众号消息
                    pass
                else:
                    # 由于其他原因失败时
                    pass
            elif event in ['CLICK', 'VIEW']:
                event_key = dict_data.get('EventKey')
                if event == 'CLICK':
                    pass
                else:
                    pass
    return HttpResponse('')


# 微信支付回调
def notify_callback_view(request):
    xml_str = request.body
    dict_data = get_dict_from_xml(xml_str)
    trade_type = dict_data.get("trade_type", "").lower()

    if trade_type in ("native", "jsapi", "app"):
        if check_xml_sign(xml_str):
            if dict_data["appid"] == PAY_DICT["app_id"]:
                if dict_data["mch_id"] == PAY_DICT["mchid"]:
                    order_id = dict_data["out_trade_no"]
                    openid = dict_data["openid"]
                    transaction_id = dict_data["transaction_id"]
                    # 自己的业务逻辑
                    pass
                return HttpResponse(
                    get_xml_from_dict({
                        "return_code": "SUCCESS",
                        "return_msg": ""
                    })
                )
    return HttpResponse(
        get_xml_from_dict({
            "return_code": "FAIL",
            "return_msg": "error"
        })
    )


# 支付宝回调接口
def alipay_callback_view(request):
    try:
        data = request.POST.copy()
        if verity_sign(data) and data["trade_status"] == "TRADE_SUCCESS":

            order_id = data["out_trade_no"]
            # buyer_logon_id = data["buyer_logon_id"]
            gmt_payment = data["gmt_payment"]   # 交易时间
            out_trade_no = data["out_trade_no"]  # 商户订单号
            # fund_bill_list = json.loads(data["fund_bill_list"])
            # trade_status = data["trade_status"]
            trade_no = data["trade_no"]  # 支付宝订单号
            buyer_id = data["buyer_id"]  # oepnid
            # 自己的业务逻辑
    except Exception as e:
        print e
    return HttpResponse('success')
