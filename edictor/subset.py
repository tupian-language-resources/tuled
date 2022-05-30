"""
Create a link to a subset of the data.
"""
from csvw.dsv import UnicodeDictReader
from pyedictor import fetch
from lingpy import *
from collections import defaultdict

template = "http://lingulist.de/edictor/index.html?file=tuled&remote_dbase=tuled&columns=DOCULECT|CONCEPT|VALUE|FORM|TOKENS|ALIGNMENT|COGID|COGIDS|CROSSIDS|MORPHEMES|COGNACY|BORROWING|NOTE&basics=DOCULECT|CONCEPT|VALUE|FORM|TOKENS|COGID|COGIDS|MORPHEMES|BORROWING|NOTE&preview=100&languages={LANGUAGES}&async=true"

badge = "http://lingulist.de/edictor/img/edictor-small.png"

languages = defaultdict(list)
with UnicodeDictReader("../etc/languages.tsv", delimiter="\t") as reader:
    for row in reader:
        languages[row["SubGroup"]] += [row["ID"]]


with open("README.md", "w") as f:
    f.write("# Links to Subsets of the Data\n\n")
    f.write("Subgroup | Link \n--- | --- \n")
    for group, langs in languages.items():
        f.write(group+" | [URL]("+template.format(LANGUAGES="|".join(langs))+")\n\n")

