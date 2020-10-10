"""
Lexibank script for generating a CLDF dataset for the TuLeD data.
"""

# Import Python standard libraries
from pathlib import Path
import attr

# Import Lexibank/CLDF/CLLD utils
from pylexibank import Concept, Language, FormSpec
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.util import progressbar
from clldutils.misc import slug


@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)
    Portuguese_Gloss = attr.ib(default=None)


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
    #    form_spec = FormSpec(
    #        missing_data=("?",),
    #        strip_inside_brackets=True,
    #        separators=",/",
    #        brackets={"{": "}", "(": ")", "[": "]"},
    #    )

    def cmd_makecldf(self, args):

        # Write sources
        args.writer.add_sources()

        # Collect concepts
        concepts = {}
        for concept in self.concepts:
            concepticon_id = concept["Concepticon"].split("/")[0]
            concepticon_id = concepticon_id.replace("_", "").strip()

            parameter_id = f"{concepticon_id}_{slug(concept['Name'])}"
            args.writer.add_concept(
                ID=parameter_id,
                Name=concept["Name"],
                Portuguese_Gloss=concept["Portuguese"],
                Concepticon_ID=concepticon_id,
            )
            concepts[concept["Name"]] = parameter_id

        # Collect languages
        languages = {}
        for row in self.languages:
            args.writer.add_language(
                ID=slug(row["Name"]),
                Name=row["Name"],
                SubGroup=row["SubGroup"],
                Glottocode=row["Glottocode"],
            )
            languages[row["ID"]] = slug(row["Name"])

        # Read raw data
        data = list(self.raw_dir.read_csv("tuled.tsv", delimiter="\t", dicts=True))

        # Add rows
        for row in progressbar(data, desc="Building CLDF"):
            eng_concept = row["CONCEPT"].strip().replace("_", " ").upper()

            # We can only add data if all fields are given
            if all([row["VALUE"], row["FORM"], row["TOKENS"]]):
                args.writer.add_form_with_segments(
                    Language_ID=languages[row["DOCULECT"]],
                    Parameter_ID=concepts[eng_concept],
                    Value=row["VALUE"],
                    Form=row["FORM"],
                    Segments=row["TOKENS"].split(),
                )
