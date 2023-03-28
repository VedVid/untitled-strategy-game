# -*- coding: utf-8 -*-


import random
import string


def make_seed(n, sections):
    seed = ""
    while sections > 0:
        seed = seed + ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
        seed = seed + "-"
        sections -= 1
    return seed[:-1]
