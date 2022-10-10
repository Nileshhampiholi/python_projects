import numpy as np

def rec(num, k, p =[]):

    s = sum(p)

    if s ==k:
        return p

    for i in range(len(num)):

        n = num[i]

