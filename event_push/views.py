# /usr/bin/env python
# coding=ut8

from django.http import HttpResponse

from wechat.common import check_from_wechat_signature, get_dict_from_xml


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