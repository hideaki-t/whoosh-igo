from whoosh.analysis import Tokenizer, Token
from whoosh.compat import text_type, PY3
import MeCab


if PY3:
    def toMeCab(s, encoding=None):
        return s

    def fromMeCab(s, encoding=None):
        return s
else:
    def toMeCab(s, encoding='utf-8'):
        return s.encode(encoding)

    def fromMeCab(s, encoding='utf-8'):
        return s.decode(encoding)


class MeCabTokenizer(Tokenizer):
    def __init__(self, conf='', encoding='utf-8'):
        self.conf = conf
        self.encoding = encoding
        self.tagger = MeCab.Tagger(conf)
        self.tagger.parseToNode(toMeCab(''))

    def __getstate__(self):
        return {k: v for k, v in self.__dict__.items() if k != "tagger"}

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.tagger = MeCab.Tagger(self.conf)
        self.tagger.parseToNode(toMeCab(''))

    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0,
                 tokenize=True, mode='', **kwargs):
        assert isinstance(value, text_type), "%r is not unicode" % value
        enc = self.encoding
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
            byte_offset = 0
            byte = value.encode('utf-8')
            m = self.tagger.parseToNode(toMeCab(value))
            while m:
                if len(m.surface) == 0:
                    m = m.next
                    continue
                t.text = fromMeCab(m.surface, enc)
                t.feature = fromMeCab(m.feature, enc)
                # TODO: use base form.
                t.boost = 1.0
                if keeporiginal:
                    t.original = t.text
                t.stopped = False
                if positions:
                    t.pos = pos
                    pos += 1
                if chars:
                    s = byte_offset + m.rlength - m.length
                    e = s + m.length
                    # convert num of byte to num of unicode chars
                    t.startchar = offset + len(byte[byte_offset:s].decode(enc))
                    t.endchar = t.startchar + len(byte[s:e].decode(enc))
                    offset = t.endchar
                    byte_offset = e
                m = m.next
                yield t
