#!/usr/bin/python
# -*- coding: utf-8 -*-
import time

from django.core.cache import cache
from django.test import TestCase, override_settings
from django.utils.encoding import force_text
from rest_framework.test import APIClient  # force_authenticate, APIRequestFactory,

from drf_cache.redis_connection import RedisConn


# from django.test.client import encode_multipart, RequestFactory
# from rest_framework.authtoken.models import Token


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

    def test_hello(self):
        resp = self.client.get('/testhello/?aaa=222&page=2&hakjshdkjas=uasiuad')
        self.assertEquals(force_text(resp.content), '"Hello World"')

    def test_cache_params(self):
        resp = self.client.get(
            '/testhello/test_params/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        self.assertEquals(force_text(resp.content), '"test params"')

    def test_decorator_with_pk(self):
        resp = self.client.get(
            '/testhello/23/test_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        self.assertEquals(force_text(resp.content), '"test params"')

    def test_cache_with_pk(self):
        resp = self.client.get(
            '/testhello/23/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_1 = force_text(resp.content)
        resp = self.client.get(
            '/testhello/23/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_2 = force_text(resp.content)
        self.assertEquals(con_1, con_2)

    def test_cache_with_list(self):
        resp = self.client.get(
            '/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_1 = force_text(resp.content)
        resp = self.client.get(
            '/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_2 = force_text(resp.content)
        self.assertEquals(con_1, con_2)

        resp = self.client.get(
            '/testhello/23/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_3 = force_text(resp.content)
        self.assertNotEqual(con_1, con_3)

    def test_cache_without_followseed(self):
        resp = self.client.get(
            '/testhello/test_cache_no_follow/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_1 = force_text(resp.content)
        resp = self.client.get(
            '/testhello/test_cache_no_follow/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_2 = force_text(resp.content)
        self.assertEquals(con_1, con_2)

    def test_cache_timeout_withseed(self):
        resp = self.client.get('/testhello/test_cache_timeout_withseed/?dkjha=asjdaks')
        con_1 = force_text(resp.content)
        resp = self.client.get('/testhello/test_cache_timeout_withseed/?dkjha=asjdaks')
        con_2 = force_text(resp.content)
        self.assertEquals(con_1, con_2)

        time.sleep(4)
        resp = self.client.get('/testhello/test_cache_timeout_withseed/?dkjha=asjdaks')
        con_3 = force_text(resp.content)
        self.assertNotEqual(con_3, con_1)

    def test_update_seed_version(self):
        resp = self.client.get('/testhello/test_cache_with_list/?dkjha=asjdaks')
        con_1 = force_text(resp.content)
        resp = self.client.get('/testhello/test_cache_with_list/?dkjha=asjdaks')
        con_2 = force_text(resp.content)
        self.assertEquals(con_1, con_2)

        self.client.post('/testhello/test_update_seed_version/', data={})

        resp = self.client.get('/testhello/test_cache_with_list/?dkjha=asjdaks')
        con_3 = force_text(resp.content)
        self.assertNotEqual(con_3, con_1)

    def test_update_seed_version_object(self):
        # 原始要更新的缓存
        resp = self.client.get(
            '/testhello/23/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_1 = force_text(resp.content)
        resp = self.client.get(
            '/testhello/23/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_2 = force_text(resp.content)
        self.assertEquals(con_1, con_2)
        # 其它对象是缓存的
        resp = self.client.get(
            '/testhello/24/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conb_1 = force_text(resp.content)
        resp = self.client.get(
            '/testhello/24/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conb_2 = force_text(resp.content)
        self.assertEquals(conb_1, conb_2)

        # list是缓存的
        resp = self.client.get(
            '/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conc_1 = force_text(resp.content)
        resp = self.client.get(
            '/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conc_2 = force_text(resp.content)
        self.assertEquals(conc_1, conc_2)

        # 更新缓存
        self.client.post('/testhello/23/test_update_object_seed_version/', data={})

        # 缓存失效了取出来的是新值
        resp = self.client.get(
            '/testhello/23/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        con_3 = force_text(resp.content)
        self.assertNotEqual(con_3, con_1)

        # list缓存也得更新
        resp = self.client.get(
            '/testhello/test_cache_with_list/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conc_3 = force_text(resp.content)
        self.assertNotEqual(conc_3, conc_1)

        # 单个其它对象缓存不更新
        resp = self.client.get(
            '/testhello/24/test_cache_with_pk/?dkjha=asjdaks&params_b=alsdl&ksjdkasjd=askdjakshd&asdhghashd=asjdkajs')
        conb_3 = force_text(resp.content)
        self.assertEquals(conb_3, conb_1)
