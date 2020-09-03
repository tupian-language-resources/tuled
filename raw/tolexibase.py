from lexibase.lexibase import LexiBase
from lingpy import *
from lingpy.compare.partial import Partial
from clldutils.misc import slug
from collections import defaultdict
from clldutils.text import strip_brackets, split_text


#wl = Wordlist('tuled-edictor.tsv')
#wl.add_entries('tokens', 'form', lambda x: x)
#for idx in wl:
#    try:
#        wl[idx, 'tokens'] = ipa2tokens(wl[idx, 'form'])
#    except:
#        wl[idx, 'tokens'] = '!ERROR!'
#wl.add_entries('alignment', 'tokens', lambda x: x)

def cogids2cogid(wordlist, ref="cogids", cognates="cogid", morphemes="morphemes"):
    C, M = {}, {}
    current = 1
    for concept in wordlist.rows:
        base = split_text(strip_brackets(concept))[0].upper().replace(" ", "_")
        idxs = wordlist.get_list(row=concept, flat=True)
        cogids = defaultdict(list)
        for idx in idxs:
            M[idx] = [c for c in wordlist[idx, ref]]
            for cogid in basictypes.ints(wordlist[idx, ref]):
                cogids[cogid] += [idx]
        for i, (cogid, idxs) in enumerate(
            sorted(cogids.items(), key=lambda x: len(x[1]), reverse=True)
        ):
            for idx in idxs:
                if idx not in C:
                    C[idx] = current
                    M[idx][M[idx].index(cogid)] = base
                else:
                    M[idx][M[idx].index(cogid)] = "_" + base.lower()
            current += 1
    wordlist.add_entries(cognates, C, lambda x: x)
    if morphemes:
        wordlist.add_entries(morphemes, M, lambda x: x)

columns=('concept_name', 'language_id', 'language_name',
        'value', 'form', 'segments', 
        'cogid_cognateset_id')
namespace=(('concept_name', 'concept'), ('language_id', 'doculect'),
        ('segments', 'tokens'), ('language_glottocode', 'glottolog'),
        ('concept_concepticon_id', 'concepticon'), ('language_latitude',
            'latitude'), ('language_longitude', 'longitude'), ('cognacy',
                'cognacy'), ('cogid_cognateset_id', 'cognacy'))


wl = Wordlist.from_cldf('../cldf/cldf-metadata.json', columns=columns,
        namespace=namespace)
D = {0: wl.columns}
for idx in wl:
    if wl[idx, 'tokens']:
        D[idx] = wl[idx]
part = Partial(D)
part.partial_cluster(method='sca', threshold=0.45, ref='cogids')
alms = Alignments(part, ref='cogids')
alms.align()
alms.add_entries('note', 'form', lambda x: '')

#part.add_entries('cog', 'cognacy', lambda x: x)
#for idx in wl:
#    if wl[idx, 'cog'].strip():
#        wl[idx, 'cog'] += '-'+wl[idx, 'concept']
#    else:
#        wl[idx, 'cog'] += str(idx)
#
#wl.renumber('cog')

cogids2cogid(alms)

lex = LexiBase(alms)
lex.db = 'tuled'
lex.dbase = 'tuled.sqlite3'
lex.create('tuled')
