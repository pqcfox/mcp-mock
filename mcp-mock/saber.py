"""Python implementation of the Saber SBM."""

N = 256


def sbm(a, b, mod=2**13):
    c = [0 for _ in range(N)]
    for i in range(N):
        for j in range(N):
            negative = i + j >= N
            c[(i + j) % N] += a[i] * b[j] * (-1 if negative else 1)

    c = [x % mod for x in c]
    return c
