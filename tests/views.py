#!/usr/bin/python
# -*- coding: utf-8 -*-
from rest_framework.decorators import action

from drf_cache.cache_key import DefaultKeyGenerator
from drf_cache.decorators import cache_rest_api_response, update_seed_version

from drf_cache.utils import get_random_code
__author__ = "vincent"
__email__ = "ohergal@gmail.com"
__copyright__ = "Copyright 2015, tiqiua.com"

from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response




class HelloView(viewsets.GenericViewSet):

    @cache_rest_api_response()
    def list(self, request, *args, **kwargs):
        return Response('Hello World')

    @action(detail=False, methods=['get'])
    @cache_rest_api_response(key_func=DefaultKeyGenerator(
        params={
            'QUERYPARAM_BUILDER': ['params_a', 'params_b']
        }
    ))

    @action(detail=False, methods=['get'])
    def test_params(self, request):
        return Response('test params')

    @action(detail=True, methods=['get'])
    @cache_rest_api_response(resource_name='testresource', resource_type='O')
    def test_with_pk(self, request, pk=None):
        return Response('test params')

    @action(detail=True, methods=['get'])
    @cache_rest_api_response(resource_name='testresource', resource_type='O')
    def test_cache_with_pk(self, request, pk=None):
        rcode = get_random_code()
        return Response(rcode)

    @action(detail=False, methods=['get'])
    @cache_rest_api_response(resource_name='testresource', resource_type='L')
    def test_cache_with_list(self, request):
        rcode = get_random_code()
        return Response(rcode)

    @action(detail=False, methods=['get'])
    @cache_rest_api_response(follow_seed=False)
    def test_cache_no_follow(self, request):
        rcode = get_random_code()
        return Response(rcode)

    @action(detail=False, methods=['get'])
    @cache_rest_api_response(resource_name='testresource', resource_type='L', timeout=2)
    def test_cache_timeout_withseed(self, request):
        rcode = get_random_code()
        return Response(rcode)

    @action(detail=False, methods=['post'])
    @update_seed_version(resource_name='testresource', resource_type='L')
    def test_update_seed_version(self, request):
        rcode = get_random_code()
        return Response(rcode, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    @update_seed_version(resource_name='testresource', resource_type='O')
    def test_update_object_seed_version(self, request, pk=None):
        rcode = get_random_code()
        return Response(rcode, status=status.HTTP_201_CREATED)
