#!/usr/bin/python
# -*- coding: utf-8 -*-
import hashlib
import json

from drf_cache.key_builder import (
    FormatKeyBuilder, QueryParamKeyBuilder,
    UniqueMethodIdKeyBuilder, UniqueResourceIdKeyBuilder
)


class KeyGenerator(object):
    """
    key生成器
    """

    def __init__(self, params=None):
        """
        params参数的形式为{"构造器名字": 参数}
        """
        if params:
            self.params = params
        else:
            self.params = {}

    def get_key(self, view_instance, view_method, request, args, kwargs):
        """
        获取key
        """
        _kwargs = {
            "view_instance": view_instance,
            "view_method": view_method,
            "request": request,
            "args": args,
            "kwargs": kwargs
        }
        key_dict = {}
        for builder in self.builders:
            data = self.get_data_from_builder(builder, **_kwargs)
            key_dict[builder.name] = data
        key_data = self.hash_key_data(key_dict)
        return key_data

    def get_data_from_builder(self, builder, **kwargs):

        builder_ins = builder()
        # 参数可以是在生成器里也可以在构造器里
        if builder_ins.name in self.params:
            build_params = self.params[builder_ins.name]
        else:
            build_params = builder_ins.params
        data = builder_ins.build_key(build_params, **kwargs)
        return data

    def __call__(self, *args, **kwargs):
        """
        方便调用 直接用类名返回结果
        """
        return self.get_key(**kwargs)

    def hash_key_data(self, key_dict):
        """
        给生成的key排序,返回排序后的json的字符串
        """
        to_hash = json.dumps(key_dict, sort_keys=True).encode("utf-8")
        return hashlib.sha256(to_hash).hexdigest()


class DefaultKeyGenerator(KeyGenerator):
    """
    默认的key生成器
    """
    builders = (QueryParamKeyBuilder,
                FormatKeyBuilder,
                UniqueMethodIdKeyBuilder,
                UniqueResourceIdKeyBuilder)
