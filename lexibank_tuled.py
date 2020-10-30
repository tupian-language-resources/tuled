import attr
from pathlib import Path

from pylexibank import Concept, Language, Cognate, Lexeme
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar
from csvw import Datatype
from pyclts import CLTS

import lingpy
from clldutils.misc import slug


@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)
    Portuguese_Gloss = attr.ib(default=None)
    EOL_ID = attr.ib(default=None)
    Semantic_Field = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Source = attr.ib(default=None)


@attr.s
class CustomCognate(Cognate):
    Segment_Slice = attr.ib(default=None)


@attr.s
class Form(Lexeme):
    Morphemes = attr.ib(default=None)
    SimpleCognate = attr.ib(default=None)
    PartialCognates = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "tuled"
    concept_class = CustomConcept
    language_class = CustomLanguage
    cognate_class = CustomCognate
    lexeme_class = Form

    def cmd_download(self, args):
        print('download')
        self.raw_dir.download(
            "https://lingulist.de/edictor/triples/get_data.py?file=tuled&remote_dbase=tuled.sqlite3",
            "tuled.tsv"
            )

    def cmd_makecldf(self, args):
        from pybtex import errors
        errors.strict = False
        args.writer.add_sources()
        args.writer["FormTable", "Segments"].separator = " + "
        args.writer["FormTable", "Segments"].datatype = Datatype.fromvalue(
            {"base": "string", "format": "([\\S]+)( [\\S]+)*"}
            )
        args.writer["FormTable", "Morphemes"].separator = "+"
        args.writer["FormTable", "PartialCognates"].separator = " "

        concepts = {}
        errors, blacklist = set(), set()
        for concept in self.concepts:
            idx = '{0}_{1}'.format(concept['NUMBER'], slug(concept['ENGLISH']))
            try:
                args.writer.add_concept(
                        ID=idx,
                        Name=concept['ENGLISH'],
                        Portuguese_Gloss=concept['PORTUGUESE'],
                        Concepticon_ID=concept['CONCEPTICON_ID'],
                        #Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                    EOL_ID=concept['EOL'],
                    Semantic_Field=concept['SEMANTIC_FIELD'],
                        )
                concepts[concept['ENGLISH']] = idx
            except ValueError:
                args.log.warn('Invalid concepticon ID {0}'.format(
                    concept['CONCEPTICON_ID']))
                errors.add('CONCEPTICON_ID {0} {1}'.format(
                    concept['ENGLISH'],
                    concept['CONCEPTICON_ID']))
        languages = {}
        sources = {}
        for row in self.languages:
            if not -90 < float(row['Latitude']) < 90:
                errors.add('LATITUDE {0}'.format(row['Name']))
            elif not -180 < float(row['Longitude']) < 180:
                errors.add('LONGITUDE {0}'.format(row['Name']))
            else:
                try:
                    args.writer.add_language(
                        ID=row['ID'],
                        Name=row['Name'],
                        SubGroup=row['SubGroup'],
                        Latitude=row['Latitude'],
                        Longitude=row['Longitude'],
                        Glottocode=row['Glottocode'] if row['Glottocode'] != '???' else None,
                    )
                    languages[row['Name']] = row['ID']
                    sources[row['ID']] = row['Sources'].split(',')
                except ValueError:
                    errors.add('LANGUAGE ID {0}'.format(
                        row['ID'],
                        ))
                    args.log.warn('Invalid Language ID {0}'.format(row['ID']))

        wl = lingpy.Wordlist(self.raw_dir.joinpath('tuled.tsv').as_posix())
        bipa = CLTS(args.clts.dir).bipa
        for idx, tokens, glosses, cogids, alignment in wl.iter_rows(
                'tokens', 'morphemes', 'cogids', 'alignment'):
            tl, gl, cl, al = (
                    len(lingpy.basictypes.lists(tokens).n),
                    len(glosses),
                    len(cogids),
                    len(lingpy.basictypes.lists(alignment).n)
                    )
            if tl != gl or tl != cl or gl != cl or al != gl or al != cl:
                errors.add('LENGTH: {0} {1} {2}'.format(
                    idx,
                    wl[idx, 'language'],
                    wl[idx, 'concept']))
                blacklist.add(idx)
            for token in tokens:
                if bipa[token].type == 'unknownsound':
                    errors.add('SOUND: {0}'.format(token))
                    blacklist.add(idx)

        visited = set()
        for idx in wl:
            if wl[idx, 'concept'] not in concepts:
                if wl[idx, 'concept'] not in visited:
                    args.log.warn('Missing concept {0}'.format(wl[idx,
                    'concept']))
                    visited.add(wl[idx, 'concept'])
                    errors.add('CONCEPT {0}'.format(wl[idx, 'concept']))
            elif wl[idx, 'doculect'] not in languages:
                if wl[idx, 'doculect'] not in visited:
                    args.log.warn("Missing language {0}".format(wl[idx, 'doculect']
                        ))
                    visited.add(wl[idx, 'doculect'])
                    errors.add('LANGUAGE {0}'.format(wl[idx, 'doculect']))
            else:
                if ''.join(wl[idx, 'tokens']).strip() and idx not in blacklist:
                    lex = args.writer.add_form_with_segments(
                        Language_ID=wl[idx, 'doculect'],
                        Parameter_ID=concepts[wl[idx, 'concept']],
                        Value=wl[idx, 'value'] or ''.join(wl[idx, 'tokens']),
                        Form=wl[idx, 'form'] or ''.join(wl[idx, 'tokens']),
                        Segments=wl[idx, 'tokens'],
                        Morphemes=wl[idx, 'morphemes'],
                        SimpleCognate=wl[idx, 'cogid'],
                        PartialCognates=wl[idx, 'cogids'],
                        Source=sources[wl[idx, 'doculect']],
                    )
                    for gloss_index, cogid in enumerate(wl[idx, 'cogids']):
                        alignment = lingpy.basictypes.lists(
                                wl[idx, "alignment"]).n[gloss_index]
                        args.writer.add_cognate(
                                lexeme=lex,
                                Cognateset_ID=cogid,
                                Segment_Slice=gloss_index + 1,
                                Alignment=alignment
                                )
                else:
                    args.log.warn('Entry ID={0}, concept={1}, language={2} is empty'.format(
                        idx, wl[idx, 'concept'], wl[idx, 'doculect']))
        

        with open(self.dir.joinpath('errors.md'), 'w') as f:
            f.write('# Error Analysis for TULED\n')
            for error in sorted(errors):
                f.write('* '+error+'\n')
