#!/usr/bin/env python
# coding=utf8

from __future__ import absolute_import

from celery import Celery

app = Celery('ck_celery_tasks')

app.config_from_object('tasks.config')
