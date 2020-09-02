from lexibase.lexibase import LexiBase
from lingpy import *

wl = Wordlist('tuled-edictor.tsv')
wl.add_entries('tokens', 'form', lambda x: x)
for idx in wl:
    try:
        wl[idx, 'tokens'] = ipa2tokens(wl[idx, 'form'])
    except:
        wl[idx, 'tokens'] = '!ERROR!'
wl.add_entries('alignment', 'tokens', lambda x: x)

wl.add_entries('cog', 'cognacy', lambda x: x)
for idx in wl:
    if wl[idx, 'cog'].strip():
        wl[idx, 'cog'] += '-'+wl[idx, 'concept']
    else:
        wl[idx, 'cog'] += str(idx)

wl.renumber('cog')


lex = LexiBase(wl)
lex.db = 'tuled'
lex.dbase = 'tuled.sqlite3'
lex.create('tuled')
