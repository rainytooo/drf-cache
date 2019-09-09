#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "vincent"
__email__ = "ohergal@gmail.com"
__copyright__ = "Copyright 2015, tiqiua.com"

from rest_framework.routers import DefaultRouter

from .views import HelloView

app_name = "drf_cache"

# 新版本的restful api
testhello_router = DefaultRouter()
testhello_router.register(r'testhello', HelloView, base_name='hellotest')

urlpatterns = testhello_router.urls


