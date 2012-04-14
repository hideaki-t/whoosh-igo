# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import whooshjp
import whooshjp.Filters


def add_docs(w):
    w.add_document(title='その1', path='1', content='こんにちは世界')
    w.add_document(title='その2', path='2', content='さようなら世界')
    w.add_document(title='その3', path='3', content='今日はいい天気')
    w.add_document(title='その4', path='4', content='これは日本語をテストする文章です。')
    w.commit()

def search(s, qp, text):
    print('search ' + text)
    for r in s.search(qp.parse(text)):
        print(r['path'], r['title'])

def test_(tk):
    scm = Schema(title=TEXT(stored=True, analyzer=tk), path=ID(unique=True,stored=True), content=TEXT(stored=True, analyzer=tk))
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
    ix = create_in('indexdir', scm)
    w = ix.writer()
    add_docs(w)

    s = ix.searcher()
    qp = QueryParser("content", schema=ix.schema)

    search(s, qp, "こんにちは世界")
    search(s, qp, "世界")
    search(s, qp, "こんにちは")
    search(s, qp, "さようなら")
    search(s, qp, "今日はいい天気")
    search(s, qp, "天気")
    search(s, qp, "は")
    ix.close()

def test_tokenize(tk):
    for i in tk('今日はいい天気'):
        print(i.text, i.stopped)
    for i in tk('これは日本語をテストする文章です。', positions=True, chars=True):
        print(i.text, i.pos, i.startchar, i.endchar)

try:
    print('Igo')
    from whooshjp.IgoTokenizer import IgoTokenizer
    import igo.Tagger
    tk = IgoTokenizer(dataDir='ipadic', gae=False)
    tk = IgoTokenizer(igo.Tagger.Tagger('ipadic'))
    test_tokenize(tk)
    tk = tk | whooshjp.Filters.FeatureFilter(['^助詞,係助詞.*$'])
    test_(tk)
    test_tokenize(tk)
except:
    print('skip')

try:
    print('MeCab')
    import MeCab
    from whooshjp.MeCabTokenizer import MeCabTokenizer
    tk = MeCabTokenizer()
    test_tokenize(tk)
    tk = tk | whooshjp.Filters.FeatureFilter(['^助詞,係助詞.*$'])
    test_(tk)
    test_tokenize(tk)
except:
    print('skip')

try:
    print('TinySegmenter')
    import tinysegmenter
    from whooshjp.TinySegmenterTokenizer import TinySegmenterTokenizer
    tk = TinySegmenterTokenizer(tinysegmenter.TinySegmenter())
    test_(tk)
    test_tokenize(tk)
except:
    print('skip')

