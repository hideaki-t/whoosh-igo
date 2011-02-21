from whoosh.analysis import Tokenizer, Token

class TinySegmenterTokenizer(Tokenizer):
    def __init__(self, segmenter, strip=True):
        self.segmenter = segmenter
        self.strip = strip

    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0,
                 tokenize=True, mode='', **kwargs):
        assert isinstance(value, unicode), "%r is not unicode" % value
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
                def strip(s):
                    return s.strip()
            else:
                def strip(s):
                    return s

            pos = start_pos
            startchar = start_char
            for s in [strip(s) for s in self.segmenter.tokenize(value)]:
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
                    startchar += len(s)
                    t.endchar = startchar
                yield t
