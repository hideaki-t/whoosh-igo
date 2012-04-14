from whoosh.analysis import Tokenizer, Token
from whoosh.compat import text_type


class TinySegmenterTokenizer(Tokenizer):
    def __init__(self, segmenter, strip=True):
        self.segmenter = segmenter
        self.strip = strip

    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0,
                 tokenize=True, mode='', **kwargs):
        assert isinstance(value, text_type), "%r is not unicode" % value
        t = Token(positions, chars, removestops=removestops, mode=mode)
        if not tokenize:
            t.original = t.text = value
            t.boost = 1.0
            if positions:
                t.pos = start_pos
            if chars:
                t.startchar = start_char
                t.endchar = start_char + len(value)
            yield t
        else:
            if self.strip:
                strip = lambda s: s.strip()
            else:
                strip = lambda s: s
            pos = start_pos
            startchar = start_char
            for s, l in \
                    [(strip(s), len(s)) for s in
                     self.segmenter.tokenize(value)]:
                t.text = s
                t.boost = 1.0
                if keeporiginal:
                    t.original = t.text
                t.stopped = False
                if positions:
                    t.pos = pos
                    pos += 1
                if chars:
                    t.startchar = startchar
                    startchar += l
                    t.endchar = startchar
                yield t
