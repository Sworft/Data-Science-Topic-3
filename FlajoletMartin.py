import hashlib


def hash_SHA(s):
    return int(hashlib.sha1(s).hexdigest(), 16) & 0xffffff


def least1(x, L):
    if x == 0:
        return 2 ** L
    return x & -x


def cardinality(stream):
    bitmap = 0
    for w in stream:
        h = hash_SHA(w)
        bitmap |= least1(h, 24)
    return least1(~bitmap, 24) / 0.77351
