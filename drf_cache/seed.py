#!/usr/bin/python
# -*- coding: utf-8 -*-

from drf_cache.cache_helper import RedisCacheVersion


cache_helper = RedisCacheVersion()


def update_seed_version(resource_name,
                        resource_id=None,
                        resource_type="L"):
    """
    更新缓存的版本
    """
    if resource_id:
        cache_helper.update_seed_version(resource_name, resource_id, resource_type)
        cache_helper.update_seed_version(resource_name, None, "L")
    else:
        cache_helper.update_seed_version(resource_name, None, "L")
