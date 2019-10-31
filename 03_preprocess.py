import json
import re
import numpy as np
import pubchempy as pcp
import chempy

print('Loading HSDB')
f = open('./data/hsdb.json','r')
db = json.load(f)['hsdb']['DOC']
f.close()
print(str(len(db)) + ' compounds loaded')

ptable = np.load('./data/ptable.npy')
compounds = list()

def empty_compound():
    return np.zeros(ptable.shape)

def isfloat(val):
    try:
        float(val)
        return True
    except ValueError:
        return False

def parseMF(mf):
    # Loop through each element
    els = chempy.Substance.from_formula(mf).composition
    comp = empty_compound()
    for el in els:
        # Set value of compound data to coefficient
        indices = np.where(ptable == el)
        if el == 0:
            indices = [[0],[0],[1]]
        elif len(indices[0]) == 0:
            print('Error: unknown element ' + str(el))
            print('Source of error: ' + mf)
        x = indices[0][0]
        y = indices[1][0]
        z = indices[2][0]
        comp[x][y][z] += els[el]
    compounds.append(comp)

def parseDB():
    global compounds
    i = 0
    for substance in db:
        if 'NameOfSubstance' not in substance: continue
        name = substance['NameOfSubstance']
        comps = pcp.get_compounds(name, 'name')
        if len(comps) > 0:
            parseMF(comps[0].molecular_formula)
        i += 1
        if i % 10 == 0:
            print(str(int(i/len(db)*100)) + '% (' + str(i) + ') compounds parsed')
    compounds = np.stack(compounds, axis=0)

parseDB()
print(compounds.shape)
