import json
import re
import numpy as np

f = open('./data/hsdb.json','r')
db = json.load(f)['hsdb']['DOC']
f.close()

ptable = np.load('./data/ptable.npy')
compounds = list()

def empty_compound():
    return np.zeros(ptable.shape)

exceptions = [
    ['.','-'],
    ['BR','Br'],
    ['CO3','C-O3'],
    ['CU','Cu'],
    ['Cu-xH3','Cu2'],
    ['Cu-xH4','Cu2'],
    ['1/2C2','C'],
    ['2H','H2'],
    ['CdSO4','Cd-S-O4'],
    ['10H2-O','H20-O10'],
    ['2Na','Na2'],
    ['2NA','Na2'],
    ['HCL','H-Cl'],
    ['x-Fe','Fe'],
    ['x-H3-','-']
]

skips = ['UVCB','UNKNOWN','Mixture','D2']

def isfloat(val):
    try:
        float(val)
        return True
    except ValueError:
        return False

def parseMF(mf):
    if '(' in mf:
        return # Skip polyatomic ions for now
    if mf in skips:
        return
    raw_mf = mf
    # Some odd exceptions
    for pair in exceptions:
        if pair[0] in mf:
            mf = mf.replace(pair[0],pair[1])
    # Loop through each element
    els = mf.split('-')
    comp = empty_compound()
    for el in els:
        if '1/2' in el:
            el = el[3:] + '0.5'
        m = re.search(r"\d", el)
        # Parse coefficient of element in MF
        el_name = el
        el_num = 1
        if m != None:
            m = m.start()
            el_name = el[:m]
            if not isfloat(el[m:]):
                print('Not a valid coefficient "' + el[m:] + '" in ' + mf)
            el_num = float(el[m:])
        # Set value of compound data to coefficient
        el_name = el_name.encode('ascii')
        indices = np.where(ptable == el_name)
        if len(indices[0]) == 0:
            print('Error: unknown element ' + str(el_name))
            print('Source of error: ' + raw_mf)
        x = indices[0][0]
        y = indices[1][0]
        z = indices[2][0]
        comp[x][y][z] += el_num
    compounds.append(comp)

def parseDB():
    global compounds
    for substance in db:
        val = substance['mf']
        end = len(val)
        if '[' in val: end = min(end, val.index('['))
        if ' ' in val: end = min(end, val.index(' '))
        mf = val[:end]
        parseMF(mf)
    compounds = np.stack(compounds, axis=0)

parseDB()
print(compounds.shape)
