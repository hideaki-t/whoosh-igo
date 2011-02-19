from whoosh.analysis import Tokenizer, Token

class IgoTokenizer(Tokenizer):
    def __init__(self, tagger):
        self.tagger = tagger

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
            pos = start_pos
            for m in self.tagger.parse(value):
                t.text = m.surface
                # TODO: use base form.
                t.boost = 1.0
                if keeporiginal:
                    t.original = t.text
                t.stopped = False
                if positions:
                    t.pos = pos
                    pos += 1
                if chars:
                    t.startchar = start_char +  m.start
                    t.endchar = start_char + len(m.surface)
                yield t
