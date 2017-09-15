# /usr/bin/env python
# coding=utf8


import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import xmltodict
import requests


EMAIL_HOST = ''
EMAIL_USER = ""
EMAIL_PASS = ""

XML_STR = """
<student> 
    <stid>10213</stid> 
    <info> 
        <name>name</name> 
        <mail>xxx@xxx.com</mail> 
        <sex>male</sex> 
    </info> 
    <course> 
        <name>math</name> 
        <score>90</score> 
    </course> 
    <course> 
        <name>english</name> 
        <score>88</score> 
    </course> 
</student>
"""


def xml_to_dict(xml_str):
    """
    xml字符串转dict
    :param xml_str:
    :return: demo_dict
    :rtype: dict
    """
    try:
        order_tuple = xmltodict.parse(xml_str)
        demo_dict_str = json.dumps(order_tuple)
        demo_dict = json.loads(demo_dict_str)
    except Exception as e:
        print e
        demo_dict = dict()
    return demo_dict


def dict_to_xml(info_dict):
    """
    dict 转 xml
    :param info_dict:
    :return: xml_str
    :rtype: str
    """
    try:
        xml_str = xmltodict.unparse(info_dict)
    except Exception as e:
        print e
        xml_str = ''
    return xml_str


def send_mail(mail_to, subject='', content='', html_content='', file_paths=None, http_links=None):
    try:
        me = ("%s<" + EMAIL_USER + ">") % Header(u"测试", "utf-8")
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = ','.join(mail_to)

        if content:
            msg.attach(MIMEText(content, 'plain', 'utf8'))
        if html_content:
            msg.attach((MIMEText(html_content, 'html', 'utf8')))

        if file_paths:
            for f in file_paths:
                f_name = f.split(r'/')[-1] if f.split(r'/') else f
                attach = MIMEText(open(f, 'rb').read(), 'base64', 'utf8')
                attach['Content-Type'] = 'application/octet-stream'
                attach.add_header('Content-Disposition', 'attachment', filename='{}'.format(f_name.encode('utf8')))
                msg.attach(attach)

        if http_links:
            for l in http_links:
                f_name = l.split('filename=')[-1] if l.split('filename') else ''
                attach = MIMEText(requests.get(l).content, 'base64', 'utf8')
                attach['Content-Type'] = 'application/octet-stream'
                attach.add_header('Content-Disposition', 'attachment', filename='{}'.format(f_name.encode('utf8')))

        server = smtplib.SMTP()
        server.connect(EMAIL_HOST)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.sendmail(me, mail_to, msg=msg.as_string())
        server.quit()
    except Exception as e:
        print e
        return False
    return True


if __name__ == '__main__':
    demo_dict = xml_to_dict(XML_STR)
    print demo_dict
    xml_str = dict_to_xml(demo_dict)
    print xml_str
    print zip(range(10), range(11), range(12), range(-16, 23))
