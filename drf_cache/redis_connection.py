#!/usr/bin/python
# -*- coding: utf-8 -*-

import redis
from django.conf import settings

from drf_cache.utils import singleton


redis_host = getattr(settings, "REDIS_SERVER_HOST", "127.0.0.1")
redis_port = getattr(settings, "REDIS_SERVER_PORT", 6379)


@singleton
class RedisConn(object):

    def __init__(self):
        self.redis_pool = redis.ConnectionPool(
            host=redis_host,
            port=redis_port)
        self._conn = redis.Redis(
            connection_pool=self.redis_pool,
            db=0,
            charset="utf-8")

    def __call__(self, *args, **kwargs):
        return self._conn

    def get_conn(self):
        return self._conn
