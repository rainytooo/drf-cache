#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

log = logging.getLogger("django_drf_cache")


class CacheView(object):
    """decorator for view method
    """

    def __init__(self, expires=None, seed=None, detail=False,
                 cache=None, key_prefix=None):
        self.expires = expires
        self.seed = seed
        self.detail = detail
        self.cache = cache
        self.key_prefix = key_prefix

    def __call__(self, *args, **kwargs):
        pass


cache_view = CacheView
