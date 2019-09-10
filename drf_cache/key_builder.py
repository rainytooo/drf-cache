#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.utils.encoding import force_text


def prepare_header_name(name):
    """
    由于django将request里的header值做了转化,所以要有一个格式标准
        >> prepare_header_name("Accept-Language")
        http_accept_language
    """
    return "http_{0}".format(name.strip().replace("-", "_")).upper()


class BaseKeyBuilder(object):
    """
    key的具体构造器接口
    """

    def __init__(self, params=None):
        self.params = params

    def build_key(self, params, view_instance, view_method, request, args, kwargs):
        """
        根据传进来的值,生成key
        """
        raise NotImplementedError


class DictKeyBuilder(BaseKeyBuilder):
    """
    字典类型的参数做key, 比如request的query参数,META,Header等
    """

    def build_key(self, params, view_instance, view_method, request, args, kwargs):
        return_data = {}

        # 用来运算的key
        if params is not None:
            source_dict = self.get_source_dict(
                params=params,
                view_instance=view_instance,
                view_method=view_method,
                request=request,
                args=args,
                kwargs=kwargs)

            if params == "*":
                # 所有的都要运算
                params = source_dict.keys()

            for key in params:
                param_value = source_dict.get(self.transform_key_for_get(key))
                if param_value:
                    return_data[self.transform_key_for_set(key)] = force_text(param_value)

        return return_data

    def transform_key_for_get(self, key):
        """
        如果key需要转换一下,比如填写的参数可能会不标准,大小写不一致,还有header里的参数,django会转成标准的一个值,和实际传入的不一致
        比如 Accept-Language => http_accept_language
        """
        return key

    def transform_key_for_set(self, key):
        """
        写入最终build的字典里的时候怎么存这个key,比如可以直接转小写.
        """
        return key

    def get_source_dict(self, params, view_instance, view_method, request, args, kwargs):
        raise NotImplementedError


class FormatKeyBuilder(BaseKeyBuilder):
    """
    Return example for json:
        u"json"

    Return example for html:
        u"html"
    """
    name = "FORMAT_BUILDER"

    def build_key(self, params, view_instance, view_method, request, args, kwargs):
        return force_text(request.accepted_renderer.format)


class QueryParamKeyBuilder(DictKeyBuilder):
    """
    GET查询参数的builder
    """
    name = "QUERYPARAM_BUILDER"

    def get_source_dict(self, params, view_instance, view_method, request, args, kwargs):
        return request.GET


class HeadersKeyBuilder(DictKeyBuilder):
    """
    Return example:
        {"accept-language": u"ru", "x-geobase-id": "123"}

    """
    name = "HEADER_BUILDER"

    def get_source_dict(self, params, view_instance, view_method, request, args, kwargs):
        return request.META

    def prepare_key_for_value_retrieving(self, key):
        return prepare_header_name(key.lower())  # Accept-Language => http_accept_language

    def prepare_key_for_value_assignment(self, key):
        return key.lower()  # Accept-Language => accept-language


class RequestMetaKeyBuilder(DictKeyBuilder):
    """
    Return example:
        {"REMOTE_ADDR": u"127.0.0.2", "REMOTE_HOST": u"yandex.ru"}

    """
    name = "REQUEST_META_BUILDER"

    def get_source_dict(self, params, view_instance, view_method, request, args, kwargs):
        return request.META


class UniqueMethodIdKeyBuilder(BaseKeyBuilder):
    name = "UNIQUE_METHOD_BUILDER"

    def build_key(self, params, view_instance, view_method, request, args, kwargs):
        return u".".join([
            view_instance.__module__,
            view_instance.__class__.__name__,
            view_method.__name__
        ])


class UniqueResourceIdKeyBuilder(BaseKeyBuilder):
    name = "UNIQUE_RESOURCE_BUILDER"

    def build_key(self, params, view_instance, view_method, request, args, kwargs):
        if "pk" in kwargs:
            return kwargs["pk"]
        return "pk"


class UniqueViewIdKeyBuilder(BaseKeyBuilder):
    name = "UNIQUE_VIEW_BUILDER"

    def build_key(self, params, view_instance, view_method, request, args, kwargs):
        return u".".join([
            view_instance.__module__,
            view_instance.__class__.__name__
        ])


class PaginationKeyBuilder(QueryParamKeyBuilder):
    """
    Return example:
        {"page_size": 100, "page": "1"}

    """
    name = "PAGINATION_BUILDER"

    def build_key(self, **kwargs):
        kwargs["params"] = []
        if hasattr(kwargs["view_instance"], "page_kwarg"):
            kwargs["params"].append(kwargs["view_instance"].page_kwarg)
        if hasattr(kwargs["view_instance"], "paginate_by_param"):
            kwargs["params"].append(kwargs["view_instance"].paginate_by_param)
        return super(PaginationKeyBuilder, self).build_key(**kwargs)


class KwargsKeyBuilder(DictKeyBuilder):
    name = "KWARGS_BUILDER"

    def get_source_dict(self, params, view_instance, view_method, request, args, kwargs):
        return kwargs


class UserKeyBuilder(BaseKeyBuilder):
    """
    Return example for anonymous:
        u"anonymous"

    Return example for authenticated (value is user id):
        u"10"
    """
    name = "USER_BUILDER"

    def build_key(self, params, view_instance, view_method, request, args, kwargs):
        if hasattr(request, "user") and request.user and request.user.is_authenticated():
            return force_text(self._get_id_from_user(request.user))
        else:
            return u"anonymous"

    def _get_id_from_user(self, user):
        return user.id
