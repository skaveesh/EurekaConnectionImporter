import collections


def make_hash():
    return collections.defaultdict(make_hash)