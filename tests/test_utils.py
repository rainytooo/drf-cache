#!/usr/bin/python
# -*- coding: utf-8 -*-
from drf_cache.redis_connection import RedisConn
from drf_cache.seed import update_seed_version

__author__ = "vincent"
__email__ = "ohergal@gmail.com"
__copyright__ = "Copyright 2015, tiqiua.com"


import time

from django.test import TestCase, override_settings

from django.utils.encoding import force_text
from django.core.cache import cache


from rest_framework.test import APIClient



# @override_settings(ROOT_URLCONF='libs.cache.tests.urls')
class TestCacheDecorator(TestCase):
    # urls = 'libs.cache.tests.urls'



    def setUp(self):
        # settings.configure(default_settings=test_settings, DEBUG=True)
        # django.setup() # 用于unittest的debug
        self.client = APIClient()

        self.redis_conn = RedisConn()
        self.redis_conn().flushall()
        cache.clear()

    def tearDown(self):
        self.redis_conn().flushall()
        cache.clear()

    def test_update_list_seed(self):
        resource_name = 'testresource'
        # 原始要更新的缓存
        resp = self.client.get('/testhello/2/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_1 = force_text(resp.content)
        resp = self.client.get('/testhello/2/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_2 = force_text(resp.content)
        self.assertEquals(con_1, con_2)

        resp = self.client.get('/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conc_1 = force_text(resp.content)
        resp = self.client.get('/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conc_2 = force_text(resp.content)
        self.assertEquals(conc_1, conc_2)

        # 更新list缓存版本
        update_seed_version(resource_name, None, 'L')

        # list被更新了
        resp = self.client.get('/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conc_3 = force_text(resp.content)
        self.assertNotEqual(conc_3, conc_1)

        # 单个对象不变
        resp = self.client.get('/testhello/2/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_3 = force_text(resp.content)
        self.assertEquals(con_3, con_1)

        # 更新了单个对象
        update_seed_version(resource_name, '2', 'O')
        # list被更新了
        resp = self.client.get('/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conc_4 = force_text(resp.content)
        self.assertNotEqual(conc_4, conc_3)

        # 单个对象缓存也被更新了
        resp = self.client.get('/testhello/2/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_4 = force_text(resp.content)
        self.assertNotEqual(con_4, con_3)

        # 更新另一个id的对象
        update_seed_version(resource_name, '33', 'O')

        # 原有对象不变
        resp = self.client.get('/testhello/2/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_5 = force_text(resp.content)
        self.assertEquals(con_5, con_4)

        # list被更新了
        resp = self.client.get('/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conc_5 = force_text(resp.content)
        self.assertNotEqual(conc_5, conc_4)






