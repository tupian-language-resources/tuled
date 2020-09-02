with open('spreadsheet.tsv', 'r') as f:
    data = [[cell.strip() for cell in row.split('\t')] for row in f]

header = data[2]
table = []
idx = 1
concepts = []
for row in data[5:]:
    language = row[0]
    for i in range(7, len(row)-3, 3):
        concept = data[1][i]
        cogid = row[i+1]
        note = row[i+2]
        value = row[i]
        concepts += [[concept, data[2][i], data[3][i]]]
        if value.strip():
            cogids = [c.strip() for c in cogid.split('/')]
            notes = [c.strip() for c in note.split('/')]
            for j, form in enumerate(value.split('/')):
                try:
                    cogid = cogids[j]
                except:
                    cogid = ''
                try:
                    note = notes[j]
                except:
                    note = ''
                table += [[str(idx), language, concept, value, form, cogid,
                    note]]
                idx += 1
with open('tuled.tsv', 'w') as f:
    for row in table:
        f.write('\t'.join(row)+'\n')
        
with open('tuled-concepts.tsv', 'w') as f:
    for row in concepts:
        f.write('\t'.join(row)+'\n')


