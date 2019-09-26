# import time

from django.core.cache import cache
from django.test import TestCase
from django.utils.encoding import force_text
from rest_framework.test import APIClient

from drf_cache.redis_connection import RedisConn


# from django.test.client import encode_multipart, RequestFactory
# from rest_framework.authtoken.models import Token


# @override_settings(ROOT_URLCONF="libs.cache.tests.urls")
class TestCacheDecorator(TestCase):
    # urls = "libs.cache.tests.urls"

    def setUp(self):
        # settings.configure(default_settings=test_settings, DEBUG=True)
        # django.setup() # 用于unittest的debug

        self.client = APIClient()

        self.redis_conn = RedisConn()
        self.redis_conn().flushall()

        cache.clear()

    def tearDown(self):
        self.redis_conn().flushall()
        cache.clear()

    def test_hello(self):
        resp = self.client.get("/testhello/new_drf_cache/")
        self.assertEqual(force_text(resp.content), "test params")
