#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging

from django.utils.decorators import decorator_from_middleware_with_args

from django_drf_cache.middleware import DrfUpdateCacheMiddleware


log = logging.getLogger("django_drf_cache")


def drf_cache(expires, *, cache=None, key_prefix=None):
    return decorator_from_middleware_with_args(DrfUpdateCacheMiddleware)(
        cache_timeout=expires, cache_alias=cache, key_prefix=key_prefix
    )

#
# class CacheView(object):
#     """decorator for view method
#     """
#
#     def __init__(self, expires=None, seed=None, detail=False,
#                  cache=None, key_prefix=None):
#         self.expires = expires
#         self.seed = seed
#         self.detail = detail
#         self.cache = cache
#         self.key_prefix = key_prefix
#
#     def __call__(self, func):
#         this = self
#
#         @wraps(func)
#         def inner(i_self, request, *args, **kwargs):
#             pass
#         return inner
#
#
# cache_view = CacheView
