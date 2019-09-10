#!/usr/bin/python
# -*- coding: utf-8 -*-


import logging
import time

from drf_cache.redis_connection import RedisConn
from drf_cache.utils import get_random_code


# Get an instance of a logger
logger = logging.getLogger(__name__)


class CacheVersion(object):
    """
    缓存版本工具
    """
    redis_conn = RedisConn()

    def get_version_by_key(self, key):
        raise NotImplementedError

    def cache_is_new(self, cache_key, resource_name, resource_id, resource_type):
        """
        比较是否最新
        :param follow:          拿来比较的seed key
        :param cache_key:
        :return:
        """
        seed_version_key = self.calculate_seed_version_key(resource_name,
                                                           resource_id,
                                                           resource_type)
        seed_version = self.get_version_by_key(seed_version_key)
        logger.debug("seed version key: %s, seed version value: %s" %
                     (seed_version_key, seed_version))

        cache_version_key = self.calculate_cache_version_key(cache_key,
                                                             resource_name,
                                                             resource_id,
                                                             resource_type)
        cache_version = self.get_version_by_key(cache_version_key)
        logger.debug("cache version key: %s, cache version value: %s" %
                     (cache_version_key, cache_version))

        is_new = False
        if seed_version and cache_version:
            if seed_version == cache_version:
                # 缓存是新的
                is_new = True
        return is_new

    def calculate_seed_version_key(self,
                                   resource_name,
                                   resource_id=None,
                                   resource_type="L"):
        if resource_type == "L":
            seed_version_key = "seedversion_%s_%s" % (resource_name, resource_type)
        else:
            seed_version_key = "seedversion_%s_%s_%s" % (resource_name, resource_type, str(resource_id))
        return seed_version_key

    def calculate_cache_version_key(self,
                                    cache_key,
                                    resource_name,
                                    resource_id=None,
                                    resource_type="L"):
        if resource_type == "L":
            seed_version_key = "cacheversion_%s_%s_%s" % \
                               (resource_name,
                                resource_type,
                                cache_key)
        else:
            seed_version_key = "cacheversion_%s_%s_%s_%s" % \
                               (resource_name,
                                resource_type,
                                str(resource_id),
                                cache_key)
        return seed_version_key

    def update_cache_version(self,
                             cache_key,
                             resource_name,
                             resource_id=None,
                             resource_type="L"):
        seed_version_key = self.calculate_seed_version_key(resource_name, resource_id, resource_type)
        seed_version = self.get_version_by_key(seed_version_key)

        cache_version_key = self.calculate_cache_version_key(cache_key,
                                                             resource_name, resource_id, resource_type)
        cache_version = self.get_version_by_key(cache_version_key)

        if seed_version:
            if cache_version:
                # 比较
                if seed_version != cache_version:
                    # 缓存是旧的
                    self.redis_conn().set(cache_version_key, seed_version)
                    self.redis_conn().expire(cache_version_key, 600)
            else:
                # 缓存的版本不存在
                self.redis_conn().set(cache_version_key, seed_version)
                self.redis_conn().expire(cache_version_key, 600)
        else:
            # 当前的版本不存在，没有缓存过, 更新seed的缓存版本和缓存的版本
            logger.debug("never cache ,update cache seed key and cache key")
            ts_version = self.get_new_version_value()
            self.redis_conn().set(seed_version_key, ts_version)
            self.redis_conn().expire(seed_version_key, 3000)
            self.redis_conn().set(cache_version_key, ts_version)
            self.redis_conn().expire(cache_version_key, 600)

    def update_seed_version(self,
                            resource_name,
                            resource_id=None,
                            resource_type="L"):
        # 更新缓存seed的值为最新,不做任何判断直接更新
        seed_version_key = self.calculate_seed_version_key(resource_name, resource_id, resource_type)
        ts_version = self.get_new_version_value()
        logger.debug("update cache seed version , key: %s, value : %s" % (seed_version_key, ts_version))
        self.redis_conn().set(seed_version_key, ts_version)
        self.redis_conn().expire(seed_version_key, 3000)

    def get_new_version_value(self):
        ts = int(round(time.time() * 1000))
        return "%d_%s" % (ts, get_random_code(5))


class RedisCacheVersion(CacheVersion):

    def get_version_by_key(self, key):
        return self.redis_conn().get(key)
