#!/usr/bin/python
# -*- coding: utf-8 -*-

from rest_framework.routers import DefaultRouter

from .views import HelloView


app_name = "drf_cache"

# 新版本的restful api
testhello_router = DefaultRouter()
testhello_router.register(r"testhello", HelloView, basename="hellotest")

urlpatterns = testhello_router.urls
