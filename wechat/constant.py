# /usr/bin/env python
# coding=utf8

ACCESS_TOKEN_KEY = 'common_access_token'
TIMEOUT_ACCESS_token = 7000

WECHAT_TOKEN = ''

PAY_DICT = {
    'app_id': '',
    'secret': '',
    'mchid': '',
    'key': '',
    'ip': '',
    'pay_template_id': ''
}


DICT = {
    'app_id': '',
    'secret': '',
    'token': ''
}


API_URL_DICT = {
    'unified_order_url': 'https://api.mch.weixin.qq.com/pay/unifiedorder',
    'pay_callback_url': 'http://xxxx/pay/notify/',
    'refund_url': 'https://api.mch.weixin.qq.com/secapi/pay/refund',
    'sapi_ticket_url': 'https://api.weixin.qq.com/cgi-bin/ticket/getticket',
    'access_token_url': 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}',
    'create_menu_url': 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}',
    'web_access_token_url': 'https://api.weixin.qq.com/sns/oauth2/access_token?'
                            'appid={}&secret={}&code={}&grant_type=authorization_code',
    'web_user_info_url': 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN ',
    'user_info_url': 'https://api.weixin.qq.com/cgi-bin/user/info?access_token={}&openid={}&lang=zh_CN',
    'upload_multi_media_url': 'http://file.api.weixin.qq.com/cgi-bin/media/upload?access_token={}&type={}',
}
