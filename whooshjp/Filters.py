import re
from whoosh.analysis import Filter


class FeatureFilter(Filter):
    def __init__(self, ignores):
        self.ignores = [re.compile(x, re.U) for x in ignores]

    @staticmethod
    def find_match(f, ignores):
        for pat in ignores:
            if pat.match(f):
                return True
        return False

    def __call__(self, tokens):
        ignores = self.ignores
        find_match = FeatureFilter.find_match
        pos = None
        for t in tokens:
            if find_match(t.feature, ignores):
                if not t.removestops:
                    t.stopped = True
                    yield t
            else:
                if t.positions:
                    if pos is None:
                        pos = t.pos
                    else:
                        pos += 1
                        t.pos = pos
                t.stopped = False
                yield t
