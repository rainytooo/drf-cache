import logging

from django.conf import settings
from django.core.cache import DEFAULT_CACHE_ALIAS, caches
from django.middleware.cache import UpdateCacheMiddleware
from django.utils.cache import (
    get_cache_key, get_max_age, has_vary_header,
    learn_cache_key, patch_response_headers
)
from django.utils.deprecation import MiddlewareMixin


log = logging.getLogger("django_drf_cache")


class DrfUpdateCacheMiddleware(UpdateCacheMiddleware):
    """

    """

    def __init__(self, get_response=None, cache_timeout=None, **kwargs):
        super().__init__(get_response)
        try:
            key_prefix = kwargs["key_prefix"]
            if key_prefix is None:
                key_prefix = ""
        except KeyError:
            key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
        self.key_prefix = key_prefix

        try:
            cache_alias = kwargs["cache_alias"]
            if cache_alias is None:
                cache_alias = DEFAULT_CACHE_ALIAS
        except KeyError:
            cache_alias = settings.CACHE_MIDDLEWARE_ALIAS
        self.cache_alias = cache_alias

        if cache_timeout is None:
            cache_timeout = settings.CACHE_MIDDLEWARE_SECONDS
        self.cache_timeout = cache_timeout
        self.cache = caches[self.cache_alias]

    def process_response(self, request, response):
        # if not self._should_update_cache(request, response):
        #     return response

        if response.streaming or response.status_code not in (200, 304):
            return response

        # Don't cache responses that set a user-specific (and maybe security
        # sensitive) cookie in response to a cookie-less request.
        if not request.COOKIES and response.cookies and has_vary_header(response, "Cookie"):
            return response

        # Don't cache a response with 'Cache-Control: private'
        if "private" in response.get("Cache-Control", ()):
            return response

        # Try to get the timeout from the "max-age" section of the "Cache-
        # Control" header before reverting to using the default cache_timeout
        # length.
        timeout = get_max_age(response)
        if timeout is None:
            timeout = self.cache_timeout
        elif timeout == 0:
            # max-age was set to 0, don't bother caching.
            return response
        patch_response_headers(response, timeout)
        if timeout and response.status_code == 200:
            cache_key = learn_cache_key(request, response, timeout, self.key_prefix, cache=self.cache)
            if hasattr(response, "render") and callable(response.render):
                response.add_post_render_callback(
                    lambda r: self.cache.set(cache_key, r, timeout)
                )
            else:
                self.cache.set(cache_key, response, timeout)
        return response


class DrfFetchFromCacheMiddleware(MiddlewareMixin):

    def __init__(self, get_response=None):
        super().__init__(get_response)
        self.key_prefix = settings.CACHE_MIDDLEWARE_KEY_PREFIX
        self.cache_alias = settings.CACHE_MIDDLEWARE_ALIAS
        self.cache = caches[self.cache_alias]

    def process_request(self, request):
        if request.method not in ("GET", "HEAD"):
            request._cache_update_cache = False
            return None  # Don't bother checking the cache.

        # try and get the cached GET response
        cache_key = get_cache_key(request, self.key_prefix, "GET", cache=self.cache)
        if cache_key is None:
            request._cache_update_cache = True
            return None  # No cache information available, need to rebuild.
        response = self.cache.get(cache_key)
        # if it wasn't found and we are looking for a HEAD, try looking just for that
        if response is None and request.method == "HEAD":
            cache_key = get_cache_key(request, self.key_prefix, "HEAD", cache=self.cache)
            response = self.cache.get(cache_key)

        if response is None:
            request._cache_update_cache = True
            return None  # No cache information available, need to rebuild.

        # hit, return cached response
        request._cache_update_cache = False
        return response
