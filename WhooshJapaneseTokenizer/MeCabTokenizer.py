from whoosh.analysis import Tokenizer, Token
import MeCab

class MeCabTokenizer(Tokenizer):
    def __init__(self, conf=''):
        self.conf = conf
        self.tagger = MeCab.Tagger(conf)

    def __getstate__(self):
        return dict([(k, self.__dict__[k]) for k in self.__dict__
                     if k != "tagger"])

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.tagger = MeCab.Tagger(conf)

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
            offset = start_char
            # TODO: support other encodings
            m = self.tagger.parseToNode(value.encode('utf-8')).next
            while m:
                t.text = m.surface.decode('utf-8')
                t.feature = m.feature
                # TODO: use base form.
                t.boost = 1.0
                if keeporiginal:
                    t.original = t.text
                t.stopped = False
                if positions:
                    t.pos = pos
                    pos += 1
                if chars:
                    t.startchar = offset + m.rlength - m.length
                    t.endchar = t.startchar + m.length
                    offset = t.endchar
                m = m.next
                yield t
