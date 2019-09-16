![PyPI - License](https://img.shields.io/pypi/l/drf-cache)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/drf-cache)
![GitHub last commit](https://img.shields.io/github/last-commit/rainytooo/drf-cache)
![PyPI](https://img.shields.io/pypi/v/drf-cache)
![PyPI - Status](https://img.shields.io/pypi/status/drf-cache)
[![Documentation Status](https://readthedocs.org/projects/drf-cache/badge/?version=latest)](https://drf-cache.readthedocs.io/en/latest/?badge=latest)

[![Build Status](https://dev.azure.com/ohergal/Drf-Cache/_apis/build/status/Drf-Cache/Drf-Cache%20CI?branchName=master)](https://dev.azure.com/ohergal/Drf-Cache/_build/latest?definitionId=3&branchName=master)
[![Requirements Status](https://requires.io/github/rainytooo/drf-cache/requirements.svg?branch=master)](https://requires.io/github/rainytooo/drf-cache/requirements/?branch=master)
[![codecov](https://codecov.io/gh/rainytooo/drf-cache/branch/master/graph/badge.svg)](https://codecov.io/gh/rainytooo/drf-cache)



# drf-cache

A Simple Django Rest Framework Caching Tools

## Content

* Requirements
* Quick Start
* Documentation
* Develop Log
* License


## How to use

## Requirements

* `django >= 2.0`
* `djangorestframework >= 3.9.0`
* `redis`

## Quick Start

### Installation

Install with pip

```
pip install drf-cache
```

### Add cache config to your django settings file

```
REDIS_SERVER_HOST = "127.0.0.1"
REDIS_SERVER_PORT = 6379
```

### Add cache decorator for your method

```
class HelloView(viewsets.GenericViewSet):
    renderer_classes = [PlainTextRenderer]

    @cache_rest_api_response()
    def list(self, request, *args, **kwargs):
        return Response("Hello World")
```

The default cache policy will expire after 600 seconds

### How to update cache

use the `update_seed_version` decorator

```
    @action(detail=False, methods=["get"])
    @cache_rest_api_response(resource_name="testresource", resource_type="L")
    def test_cache_with_list(self, request):
        rcode = get_random_code()
        return Response(rcode)
```

## Documentation

The [full documentation](https://drf-cache.readthedocs.io/en/latest/) is on Read the Docs

## Develop Log


* 2019-09-10
    - publish test results and coverage results to the Azure in pipeline
    - upload to pypi by azure
    - format the code
    - use tox and flake8 to build and test
* 2019-09-09
    - Use the Azure Pipeline to building and assemble
    
    
## License

Drf-Cache is released under the terms of the MIT license. Full details in LICENSE file.