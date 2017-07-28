# /usr/bin/env python
# coding=utf8


import json
import xmltodict


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


if __name__ == '__main__':
    demo_dict = xml_to_dict(XML_STR)
    print demo_dict
    xml_str = dict_to_xml(demo_dict)
    print xml_str
    print zip(range(10), range(11), range(12), range(-16, 23))
