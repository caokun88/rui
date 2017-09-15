#!/usr/bin/env python
# coding=utf8

from tasks import app

from util import send_mail


@app.task(queue='ck:celery:mail')
def celery_send_mail(mail_to, subject='', content='', html_content='', file_paths=None, http_links=None):
    msg = send_mail(mail_to, subject, content, html_content, file_paths, http_links)
    return msg
