# coding:utf-8
from whoosh.analysis import Tokenizer, Token
from whoosh.compat import text_type
import igo.Tagger


class IgoTokenizer(Tokenizer):
    def __init__(self, tagger=None, **tagger_initparam):
        if tagger:
            self.tagger = tagger
            self.tagger_initparam = None
        else:
            self.tagger = igo.Tagger.Tagger(**tagger_initparam)
            self.tagger_initparam = tagger_initparam

    def __getstate__(self):
        if self.tagger_initparam is not None:
            return self.__dict__
        return {k: v for k, v in self.__dict__.items() if k != "tagger"}

    def __setstate__(self, state):
        self.__dict__.update(state)
        if not hasattr(self, 'tagger'):
            self.tagger = igo.Tagger.Tagger(**self.tagger_initparam)

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
            for m in self.tagger.parse(value):
                t.text = m.surface
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
                    t.startchar = start_char + m.start
                    t.endchar = t.startchar + len(m.surface)
                yield t
