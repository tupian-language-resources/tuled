import attr
from pathlib import Path

from pylexibank import Concept, Language, FormSpec
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar
from cldfbench import CLDFSpec
from csvw import Datatype
from pyclts import CLTS

import lingpy
from clldutils.misc import slug


@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)


@attr.s
class CustomLanguage(Language):
    Latitude = attr.ib(default=None)
    Longitude = attr.ib(default=None)
    SubGroup = attr.ib(default=None)
    Source = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = "tuled"
    concept_class = CustomConcept
    language_class = CustomLanguage
    form_spec = FormSpec(
            missing_data=("?", ),
            strip_inside_brackets=True,
            separators = ",/,"
            )

    def cmd_makecldf(self, args):

        args.writer.add_sources()
        concepts = {}
        for concept in self.concepts:
            idx = '{0}_{1}'.format(concept['NUMBER'], slug(concept['ENGLISH']))
            args.writer.add_concept(
                    ID=idx,
                    Name=concept['ENGLISH'],
                    Concepticon_ID=concept['CONCEPTICON_ID'],
                    Concepticon_Gloss=concept['CONCEPTICON_GLOSS']
                    )
            concepts[concept['PORTUGUESE']] = idx
        languages = {}
        for row in self.languages:
            args.writer.add_language(
                    ID=slug(row['Language']),
                    Name=row['Language']
                    )
            languages[row['Language']] = slug(row['Language'])
        
        data = [row for row in self.raw_dir.read_csv('concepts_cognates.tsv',
            delimiter='\t', dicts=False)]

        header = data[2]
        missc, missl = set(), set()
        for row in data[6:]:
            language = row[0]
            lid = languages.get(language)
            if lid:
                for i in range(7, len(row)-3, 3):
                    if i < len(row)+1:
                        concept=data[1][i]
                        cogid=row[i+1]
                        note=row[i+2]
                        form=row[i]
                        if concept in concepts and form.strip():
                            for lex in args.writer.add_forms_from_value(
                                    Parameter_ID=concepts[concept],
                                    Language_ID=lid,
                                    Value=form,
                                    Source=''
                                    ):
                                args.writer.add_cognate(
                                        lexeme=lex,
                                        Cognateset_ID=slug('{0}-{1}'.format(concept,
                                            cogid)),
                                        )
                        else:
                            missc.add(concept)
            else:
                missl.add(language)
        for c in missc:
            print('missing concept', c)
        print('')
        for c in missl:
            print('missing language', c)
                

