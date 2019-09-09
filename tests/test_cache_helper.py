#!/usr/bin/python
# -*- coding: utf-8 -*-
from drf_cache.cache_helper import RedisCacheVersion
from drf_cache.redis_connection import RedisConn

__author__ = "vincent"
__email__ = "ohergal@gmail.com"
__copyright__ = "Copyright 2015, tiqiua.com"

import calendar
from datetime import timedelta
from unittest import TestCase

from django.utils import timezone



class TestCacheVersion(TestCase):

    def setUp(self):
        self.cache_version = RedisCacheVersion()
        self.redis_conn = RedisConn()
        self.redis_conn().flushall()

    def tearDown(self):
        self.redis_conn().flushall()

    def test_seed_version_key(self):
        seed_version_key = self.cache_version.calculate_seed_version_key('resource', None, 'L')
        self.assertEquals('seedversion_resource_L', seed_version_key)

        seed_version_key = self.cache_version.calculate_seed_version_key('resource', 1, 'O')
        self.assertEquals('seedversion_resource_O_1', seed_version_key)

    def test_cache_version_key(self):
        seed_version_key = self.cache_version.calculate_cache_version_key('kahdasdk', 'resource', None, 'L')
        self.assertEquals('cacheversion_resource_L_kahdasdk', seed_version_key)

        seed_version_key = self.cache_version.calculate_cache_version_key('kahdasdk', 'resource', 1, 'O')
        self.assertEquals('cacheversion_resource_O_1_kahdasdk', seed_version_key)

    def test_cache_is_new(self):
        self.redis_conn().flushall()
        seedversion = 'seedversion_resource_L'
        cache_key = 'kajhsjdahskd'
        cacheversion = 'cacheversion_resource_L_kajhsjdahskd'
        ts_version = calendar.timegm(timezone.now().timetuple())
        tz_2 = timezone.now() + timedelta(minutes=-2)
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, 'resource', None, 'L')
        self.assertFalse(is_new)

        ts_version2 = calendar.timegm(tz_2.timetuple())
        self.redis_conn().set(cacheversion, ts_version2)
        self.redis_conn().expire(seedversion, 600)
        is_new = self.cache_version.cache_is_new(cache_key, 'resource', None, 'L')
        self.assertFalse(is_new)

        self.redis_conn().flushall()
        is_new = self.cache_version.cache_is_new(cache_key, 'resource', None, 'L')
        self.assertFalse(is_new)

        seedversion = 'seedversion_resource_L'
        cache_key = 'kajhsjdahskd'
        cacheversion = 'cacheversion_resource_L_kajhsjdahskd'
        ts_version = calendar.timegm(timezone.now().timetuple())
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)
        self.redis_conn().set(cacheversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, 'resource', None, 'L')
        self.assertTrue(is_new)

        self.redis_conn().flushall()

    def test_cache_is_new_object(self):
        """
        测试单个对象的
        """
        self.redis_conn().flushall()
        seedversion = 'seedversion_resource_O_233'
        cache_key = 'kajhsjdahskd'
        cacheversion = 'cacheversion_resource_O_233_kajhsjdahskd'
        ts_version = calendar.timegm(timezone.now().timetuple())
        tz_2 = timezone.now() + timedelta(minutes=-2)
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, 'resource', 233, 'O')
        self.assertFalse(is_new)

        ts_version2 = calendar.timegm(tz_2.timetuple())
        self.redis_conn().set(cacheversion, ts_version2)
        self.redis_conn().expire(seedversion, 600)
        is_new = self.cache_version.cache_is_new(cache_key, 'resource', 233, 'O')
        self.assertFalse(is_new)

        self.redis_conn().flushall()
        is_new = self.cache_version.cache_is_new(cache_key, 'resource', 233, 'O')
        self.assertFalse(is_new)

        ts_version = calendar.timegm(timezone.now().timetuple())
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)
        self.redis_conn().set(cacheversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, 'resource', 233, 'O')
        self.assertTrue(is_new)

        self.redis_conn().flushall()

    def test_update_cache_version(self):
        self.redis_conn().flushall()

        seedversion = 'seedversion_resource_L'
        cache_key = 'kajhsjdahskd'
        is_new = self.cache_version.cache_is_new(cache_key, 'resource', None, 'L')
        self.assertFalse(is_new)

        cacheversion = 'cacheversion_resource_L_kajhsjdahskd'
        ts_version = calendar.timegm(timezone.now().timetuple())
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, 'resource', None, 'L')
        self.assertFalse(is_new)

        self.cache_version.update_cache_version(cache_key, 'resource', None, 'L')

        is_new = self.cache_version.cache_is_new(cache_key, 'resource', None, 'L')
        self.assertTrue(is_new)

        self.redis_conn().flushall()
