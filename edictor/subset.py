"""
Create a link to a subset of the data.
"""
from csvw.dsv import UnicodeDictReader
from pyedictor import fetch
from lingpy import *
from collections import defaultdict

template = "http://lingulist.de/edictor/index.html?file=tuled&remote_dbase=tuled&columns=DOCULECT|CONCEPT|VALUE|FORM|TOKENS|ALIGNMENT|COGID|COGIDS|CROSSIDS|MORPHEMES|COGNACY|BORROWING|NOTE&basics=DOCULECT|CONCEPT|VALUE|FORM|TOKENS|COGID|COGIDS|CROSSIDS|MORPHEMES|BORROWING|NOTE&preview=100&root_formatter=CROSSIDS&doculects={LANGUAGES}&async=true"

badge = "http://lingulist.de/edictor/img/edictor-small.png"

languages = defaultdict(list)
with UnicodeDictReader("../etc/languages.tsv", delimiter="\t") as reader:
    for row in reader:
        languages[row["SubGroup"]] += [row["ID"]]


with open("README.html", "w") as f:
    f.write("<h1>Links to Subsets of the Data</h1>\n\n")
    f.write("<table>")
    f.write("<tr><th>Subgroup</th><th>Link</th><th>Size</th></tr>\n")
    for group, langs in languages.items():
        f.write("<tr><td>"+group+"</td><td><a href="+'"'+template.format(LANGUAGES="|".join(langs))+'">URL</a></td>')
        f.write("<td>"+str(len(langs))+'</td></tr>')
    f.write("</table>")

