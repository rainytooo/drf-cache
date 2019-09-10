#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import string


def get_random_code(str_count=10):
    """
    获取随机码
    """
    r_str = "".join(random.SystemRandom()
                    .choice(string.ascii_uppercase + string.digits)
                    for _ in range(str_count))
    return r_str
