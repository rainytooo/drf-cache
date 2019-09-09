#!/usr/bin/python
# -*- coding: utf-8 -*-
from drf_cache.cache_key import KeyGenerator

__author__ = "vincent"
__email__ = "ohergal@gmail.com"
__copyright__ = "Copyright 2015, tiqiua.com"


from unittest import TestCase



class TestKeyGenerator(TestCase):
    """
    测试key的生成器
    """

    def setUp(self):
        self.key_g = KeyGenerator()

    def tearDown(self):
        pass

    def test_hash_key_data(self):
        """
        测试排序
        :return:
        """
        key_data = {
            'USER_BUILDER': '1',
            'HEADER_BUILDER': {'Accept': 'application/jsom'},
            'FORMAT_BUILDER': 'json',
        }
        result = self.key_g.hash_key_data(key_data)
        self.assertEquals('896ac46647130e43b842d694b94d9b3f0e6acf1d540ed8e4c31e3278e499cea0', result)
