#!/usr/bin/python
# -*- coding: utf-8 -*-

import logging
# from django.utils.decorators import available_attrs
from functools import WRAPPER_ASSIGNMENTS, wraps

from django.core.cache import cache as dj_cache

from drf_cache.cache_helper import RedisCacheVersion
from drf_cache.cache_key import DefaultKeyGenerator


log = logging.getLogger("drf_cache")


class CacheRestApiResponse(object):
    def __init__(self,
                 resource_name=None,
                 resource_type="L",
                 key_func=None,
                 cache=None,
                 timeout=None,
                 cache_errors=False,
                 follow_seed=True):
        if timeout is None:
            self.timeout = 600
        else:
            self.timeout = timeout
        self.key_func = key_func or DefaultKeyGenerator()
        if cache:
            self.cache = cache
        else:
            self.cache = dj_cache
        self.cache_errors = cache_errors
        self.cache_helper = RedisCacheVersion()
        self.resource_name = resource_name
        self.resource_type = resource_type
        self.follow_seed = follow_seed

    def __call__(self, func):
        this = self

        @wraps(func, assigned=WRAPPER_ASSIGNMENTS)
        def inner(self, request, *args, **kwargs):
            return this.process_cache_response(
                view_instance=self,
                view_method=func,
                request=request,
                args=args,
                kwargs=kwargs,
            )

        return inner

    def process_cache_response(self,
                               view_instance,
                               view_method,
                               request,
                               args,
                               kwargs):
        try:
            # 获取key
            key = self.calculate_key(
                view_instance=view_instance,
                view_method=view_method,
                request=request,
                args=args,
                kwargs=kwargs)
            if self.follow_seed:
                # 版本判断
                # 获取resource id
                if "pk" in kwargs:
                    resource_id = kwargs["pk"]
                else:
                    resource_id = None
                cache_is_new = self.cache_helper.cache_is_new(key,
                                                              self.resource_name,
                                                              resource_id,
                                                              self.resource_type)
                if cache_is_new:
                    # 缓存的是最新的，可以取缓存
                    log.debug("cache hit by key: %s" % key)
                    response = self.cache.get(key)
                    if not response:
                        response = self.render_response(request, view_instance, view_method, args, kwargs)
                        if not response.status_code >= 400 or self.cache_errors:
                            self.cache.set(key, response, self.timeout)
                else:
                    log.debug("cache not hit: %s" % key)
                    response = self.render_response(request, view_instance, view_method, args, kwargs)
                    if not response.status_code >= 400 or self.cache_errors:
                        self.cache.set(key, response, self.timeout)
                    self.cache_helper.update_cache_version(key, self.resource_name, resource_id,
                                                           self.resource_type)
            else:
                # 直接缓存,不经过版本管理
                response = self.cache.get(key)
                if not response:
                    response = self.render_response(request, view_instance, view_method, args, kwargs)
                    if not response.status_code >= 400 or self.cache_errors:
                        self.cache.set(key, response, self.timeout)
        except Exception as e:
            log.exception(e)
            response = self.render_response(request, view_instance, view_method, args, kwargs)
        if not hasattr(response, "_closable_objects"):
            response._closable_objects = []
        return response

    def render_response(self, request,
                        view_instance, view_method,
                        args, kwargs):
        response = view_method(view_instance, request, *args, **kwargs)
        response = view_instance.finalize_response(request, response, *args, **kwargs)
        response.render()
        return response

    def calculate_key(self,
                      view_instance,
                      view_method,
                      request,
                      args,
                      kwargs):
        """
        获取缓存的key
        """
        cache_key = self.key_func(
            view_instance=view_instance,
            view_method=view_method,
            request=request,
            args=args,
            kwargs=kwargs
        )
        return cache_key


class UpdateCacheSeedVersion(object):

    def __init__(self,
                 resource_name=None,
                 resource_type="L", ):
        self.cache_helper = RedisCacheVersion()
        self.resource_name = resource_name
        self.resource_type = resource_type

    def __call__(self, func):
        this = self

        @wraps(func, assigned=WRAPPER_ASSIGNMENTS)
        def inner(self, request, *args, **kwargs):
            return this.update_cahce_version(
                view_instance=self,
                view_method=func,
                request=request,
                args=args,
                kwargs=kwargs,
            )

        return inner

    def update_cahce_version(self,
                             view_instance,
                             view_method,
                             request,
                             args,
                             kwargs):
        """
        更新缓存的版本
        """

        response = view_method(view_instance, request, *args, **kwargs)
        if response:
            if response.status_code == 201:
                if "pk" in kwargs:
                    resource_id = kwargs["pk"]
                else:
                    resource_id = None
                self.cache_helper.update_seed_version(self.resource_name, resource_id, self.resource_type)
                # 如果是单个对象,那么就要更新整个list
                if resource_id:
                    self.cache_helper.update_seed_version(self.resource_name, None, "L")
        # 如果是201 或者
        return response


cache_rest_api_response = CacheRestApiResponse

update_seed_version = UpdateCacheSeedVersion
