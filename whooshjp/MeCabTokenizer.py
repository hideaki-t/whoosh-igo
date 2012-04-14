from whoosh.analysis import Tokenizer, Token
from whoosh.compat import text_type
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
            pos = start_pos
            offset = start_char
            byte_offset = 0
            # TODO: support other encodings
            byte = value.encode('utf-8')
            m = self.tagger.parseToNode(byte)
            while m:
                if len(m.surface) == 0:
                    m = m.next
                    continue
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
                    s = byte_offset + m.rlength - m.length
                    e = s + m.length
                    t.startchar = offset + \
                        len(byte[byte_offset:s].decode('utf-8'))
                    t.endchar = t.startchar + len(byte[s:e].decode('utf-8'))
                    offset = t.endchar
                    byte_offset = e
                m = m.next
                yield t
