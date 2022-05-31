"""Python implementation of the Kyber NTT and base multiplication."""

from copy import copy

ZETAS = [
    1,
    1729,
    2580,
    3289,
    2642,
    630,
    1897,
    848,
    1062,
    1919,
    193,
    797,
    2786,
    3260,
    569,
    1746,
    296,
    2447,
    1339,
    1476,
    3046,
    56,
    2240,
    1333,
    1426,
    2094,
    535,
    2882,
    2393,
    2879,
    1974,
    821,
    289,
    331,
    3253,
    1756,
    1197,
    2304,
    2277,
    2055,
    650,
    1977,
    2513,
    632,
    2865,
    33,
    1320,
    1915,
    2319,
    1435,
    807,
    452,
    1438,
    2868,
    1534,
    2402,
    2647,
    2617,
    1481,
    648,
    2474,
    3110,
    1227,
    910,
    17,
    2761,
    583,
    2649,
    1637,
    723,
    2288,
    1100,
    1409,
    2662,
    3281,
    233,
    756,
    2156,
    3015,
    3050,
    1703,
    1651,
    2789,
    1789,
    1847,
    952,
    1461,
    2687,
    939,
    2308,
    2437,
    2388,
    733,
    2337,
    268,
    641,
    1584,
    2298,
    2037,
    3220,
    375,
    2549,
    2090,
    1645,
    1063,
    319,
    2773,
    757,
    2099,
    561,
    2466,
    2594,
    2804,
    1092,
    403,
    1026,
    1143,
    2150,
    2775,
    886,
    1722,
    1212,
    1874,
    1029,
    2110,
    2935,
    885,
    2154,
]

Q = 3329
N = 256


def basemul(a, b, zeta):
    r = [None, None]
    r[0] = a[1] * b[1]
    r[0] *= zeta
    r[0] += a[0] * b[0]
    r[1] = a[0] * b[1]
    r[1] += a[1] * b[0]

    r[0] = r[0] % Q
    r[1] = r[1] % Q
    return r


def full_basemul(a, b):
    r = [None for _ in range(N)]
    for i in range(N // 4):
        first = basemul(
            a[(4 * i) : (4 * i + 2)], b[(4 * i) : (4 * i + 2)], ZETAS[64 + i]
        )
        r[(4 * i) : (4 * i + 2)] = first

        second = basemul(
            a[(4 * i + 2) : (4 * i + 4)], b[(4 * i + 2) : (4 * i + 4)], -ZETAS[64 + i]
        )
        r[(4 * i + 2) : (4 * i + 4)] = second

    return r


def ntt(r):
    r = copy(r)  # original code mutates r
    k = 1
    l = 128
    while l >= 2:
        start = 0
        j = 0
        while start < 256:
            j = start
            zeta = ZETAS[k]
            k += 1
            while j < start + l:
                t = (zeta * r[j + l]) % Q
                r[j + l] = (r[j] - t) % Q
                r[j] = (r[j] + t) % Q
                j += 1
            start = j + l
        l >>= 1

    return r


def invntt(r):
    r = copy(r)
    k = 127
    l = 2
    while l <= 128:
        start = 0
        j = 0
        while start < 256:
            j = start
            zeta = ZETAS[k]
            k -= 1
            while j < start + l:
                t = r[j]
                r[j] = (t + r[j + l]) % Q
                r[j + l] = r[j + l] - t
                r[j + l] = (r[j + l] * zeta) % Q
                j += 1
            start = j + l
        l <<= 1

    j = 0
    while j < 256:
        r[j] = r[j] * pow(128, -1, Q) % Q
        j += 1

    return r
