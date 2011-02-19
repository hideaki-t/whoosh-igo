# -*- coding: utf-8 -*-
import os
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser

import igo.Tagger
import IgoTokenizer

tk = IgoTokenizer.IgoTokenizer(igo.Tagger.Tagger('ipadic'))
scm = Schema(title=TEXT(stored=True, analyzer=tk), path=ID(unique=True,stored=True), content=TEXT(analyzer=tk))

def add_docs(w):
    w.add_document(title=u'その1', path=u'1', content=u'こんにちは世界')
    w.add_document(title=u'その2', path=u'2', content=u'さようなら世界')
    w.commit()

def search(s, qp, text):
    print 'search ' + text
    for r in s.search(qp.parse(text)):
        print r['path'], r['title']

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
ix = create_in('indexdir', scm)
w = ix.writer()
add_docs(w)

s = ix.searcher()
qp = QueryParser("content", schema=ix.schema)

search(s, qp, u"こんにちは世界")
search(s, qp, u"世界")
search(s, qp, u"こんにちは")
search(s, qp, u"さようなら")
