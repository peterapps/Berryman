import json
import re

f = open('hsdb.json','r')
db = json.load(f)['hsdb']['DOC']
f.close()

elements = set()
compounds = list()

def parseMF(mf):
    mf = mf.replace('.','-')
    els = mf.split('-')
    el_data = dict()
    for el in els:
        m = re.search(r"\d", el)
        el_name = el
        el_num = 1
        if m != None:
            m = m.start()
            el_name = el[:m]
            el_num = int(el[m:])
        elements.add(el_name)
        el_data[el_name] = el_num
    compounds.append(el_data)

def padCompounds():
    for i in range(len(compounds)):
        for el in elements:
            if el not in compounds[i]:
                compounds[i][el] = 0

for substance in db:
    val = substance['mf']
    end = len(val)
    if '[' in val: end = min(end, val.index('['))
    if ' ' in val: end = min(end, val.index(' '))
    mf = val[:end]
    parseMF(mf)

padCompounds()

print(elements)
