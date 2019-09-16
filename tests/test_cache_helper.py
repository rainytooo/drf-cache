#!/usr/bin/python
# -*- coding: utf-8 -*-
import calendar
from datetime import timedelta
from unittest import TestCase

from django.utils import timezone

from drf_cache.cache_helper import RedisCacheVersion, CacheVersion
from drf_cache.redis_connection import RedisConn


class TestCacheVersion(TestCase):

    def setUp(self):
        self.cache_version = RedisCacheVersion()
        self.redis_conn = RedisConn()
        self.redis_conn().flushall()

    def tearDown(self):
        self.redis_conn().flushall()

    def test_not_implements_cache_version(self):
        not_implements = CacheVersion()
        with self.assertRaises(NotImplementedError) as sec:
            seed_version_key = not_implements.cache_is_new("board", "resource", None, "L")

    def test_seed_version_key(self):
        seed_version_key = self.cache_version.calculate_seed_version_key("resource", None, "L")
        self.assertEqual("seedversion_resource_L", seed_version_key)

        seed_version_key = self.cache_version.calculate_seed_version_key("resource", 1, "O")
        self.assertEqual("seedversion_resource_O_1", seed_version_key)

    def test_cache_version_key(self):
        seed_version_key = self.cache_version.calculate_cache_version_key("kahdasdk", "resource", None, "L")
        self.assertEqual("cacheversion_resource_L_kahdasdk", seed_version_key)

        seed_version_key = self.cache_version.calculate_cache_version_key("kahdasdk", "resource", 1, "O")
        self.assertEqual("cacheversion_resource_O_1_kahdasdk", seed_version_key)

    def test_cache_is_new(self):
        self.redis_conn().flushall()
        seedversion = "seedversion_resource_L"
        cache_key = "kajhsjdahskd"
        cacheversion = "cacheversion_resource_L_kajhsjdahskd"
        ts_version = calendar.timegm(timezone.now().timetuple())
        tz_2 = timezone.now() + timedelta(minutes=-2)
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, "resource", None, "L")
        self.assertFalse(is_new)

        ts_version2 = calendar.timegm(tz_2.timetuple())
        self.redis_conn().set(cacheversion, ts_version2)
        self.redis_conn().expire(seedversion, 600)
        is_new = self.cache_version.cache_is_new(cache_key, "resource", None, "L")
        self.assertFalse(is_new)

        self.redis_conn().flushall()
        is_new = self.cache_version.cache_is_new(cache_key, "resource", None, "L")
        self.assertFalse(is_new)

        seedversion = "seedversion_resource_L"
        cache_key = "kajhsjdahskd"
        cacheversion = "cacheversion_resource_L_kajhsjdahskd"
        ts_version = calendar.timegm(timezone.now().timetuple())
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)
        self.redis_conn().set(cacheversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, "resource", None, "L")
        self.assertTrue(is_new)

        self.redis_conn().flushall()

    def test_cache_is_new_object(self):
        """
        测试单个对象的
        """
        self.redis_conn().flushall()
        seedversion = "seedversion_resource_O_233"
        cache_key = "kajhsjdahskd"
        cacheversion = "cacheversion_resource_O_233_kajhsjdahskd"
        ts_version = calendar.timegm(timezone.now().timetuple())
        tz_2 = timezone.now() + timedelta(minutes=-2)
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, "resource", 233, "O")
        self.assertFalse(is_new)

        ts_version2 = calendar.timegm(tz_2.timetuple())
        self.redis_conn().set(cacheversion, ts_version2)
        self.redis_conn().expire(seedversion, 600)
        is_new = self.cache_version.cache_is_new(cache_key, "resource", 233, "O")
        self.assertFalse(is_new)

        self.redis_conn().flushall()
        is_new = self.cache_version.cache_is_new(cache_key, "resource", 233, "O")
        self.assertFalse(is_new)

        ts_version = calendar.timegm(timezone.now().timetuple())
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)
        self.redis_conn().set(cacheversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        is_new = self.cache_version.cache_is_new(cache_key, "resource", 233, "O")
        self.assertTrue(is_new)

        self.redis_conn().flushall()

    def test_update_cache_version(self):
        self.redis_conn().flushall()

        seedversion = "seedversion_resource_L"
        cache_key = "kajhsjdahskd"
        is_new = self.cache_version.cache_is_new(cache_key, "resource", None, "L")
        self.assertFalse(is_new)

        # cacheversion = "cacheversion_resource_L_kajhsjdahskd"
        # now resource updated, the seed version is update
        ts_version = calendar.timegm(timezone.now().timetuple())
        self.redis_conn().set(seedversion, ts_version)
        self.redis_conn().expire(seedversion, 600)

        # after resource updated,  everything about this resource must update,
        # so the cache version is old
        is_new = self.cache_version.cache_is_new(cache_key, "resource", None, "L")
        self.assertFalse(is_new)
        # now update the cache version
        self.cache_version.update_cache_version(cache_key, "resource", None, "L")
        # right now the cache version is synchronous update with the resource seed version
        is_new = self.cache_version.cache_is_new(cache_key, "resource", None, "L")
        self.assertTrue(is_new)

        self.redis_conn().flushall()

    def test_update_seed_version(self):
        self.redis_conn().flushall()

        resource_name = "pillar"
        resource_id = 499
        resource_type = "O"
        # get a seed key
        seed_version_key = self.cache_version.calculate_seed_version_key(
            resource_name, resource_id, resource_type)
        self.assertIsNone(self.redis_conn().get(seed_version_key))
        # save the seed version to redis
        self.cache_version.update_seed_version(
            resource_name, resource_id, resource_type)

        seed_version = self.redis_conn().get(seed_version_key)
        self.assertIsNotNone(seed_version)

        # update the seed version
        seed_version_after_update = self.cache_version.update_seed_version(
            resource_name, resource_id, resource_type)
        self.assertNotEqual(seed_version, seed_version_after_update)
