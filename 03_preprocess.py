import numpy as np
import pubchempy as pcp
from time import time
from datetime import timedelta

ptable = np.load('./data/ptable.npy')

def empty_compound():
    return np.zeros(ptable.shape)

def parse_compound(mol):
    els = dict()
    for el in mol.elements:
        if el in els: els[el] += 1
        else: els[el] = 1
    comp = empty_compound()
    comp[0][0][1] = mol.charge # Formal charge behind H
    for el in els:
        # Set value of compound data to coefficient
        indices = np.where(ptable == el.encode('ascii'))
        if len(indices[0]) == 0:
            print('Error: unknown element ' + str(el))
            print('Source of error: ' + mf)
            return None
        x = indices[0][0]
        y = indices[1][0]
        z = indices[2][0]
        comp[x][y][z] += els[el]
    return comp

def parseDB(db, check):
    i = 0
    compounds = list()
    formulae = set()
    start_time = time()
    for substance in db:
        substance = substance.lower()
        while True:
            try:
                comps = pcp.get_compounds(substance, 'name')
                if len(comps) > 0:
                    mf = comps[0].molecular_formula
                    if (not check) or (mf not in formulae):
                        result = parse_compound(comps[0])
                        if result is not None: compounds.append(result)
                        formulae.add(mf)
                #else:
                #    print('Could not find compound: ' + substance)
                break
            except:
                print('Could not load from PubChem. Trying again')
        i += 1
        # Print helpful info
        if i % int(0.01*len(db)) == 0:
            curr = time()
            perc = i / len(db)
            remaining = (curr - start_time) / perc
            remaining = str(timedelta(seconds=int(remaining)))
            msg = str(int(perc*100)) + '%'
            msg += ' (' + str(i) + '/' + str(len(db)) + ')'
            msg += ' compounds parsed. '
            msg += remaining + ' remaining'
            print('  ' + msg)
    return np.stack(compounds, axis=0)

def parse_hsdb():
    print('Loading HSDB')
    f = open('./data/hsdb_names.txt','r')
    hsdb = f.read().splitlines()
    f.close()
    print(str(len(hsdb)) + ' compounds loaded from HSDB')

    print('Parsing ' + str(len(hsdb)) + ' toxic compounds')
    toxic = parseDB(hsdb, False)
    print('Done. Found ' + str(toxic.shape[0]) + ' toxic compounds')
    np.save('./data/toxic.npy', toxic)
    print('Saved.')

def parse_chemid():
    print('Loading ChemIDplus')
    f = open('./data/chemid_names.txt','r')
    chemdb = f.read().splitlines()
    f.close()
    print(str(len(chemdb)) + ' compounds loaded from ChemIDplus')

    print('Parsing ' + str(len(chemdb)) + ' total compounds')
    nontoxic = parseDB(chemdb, True)
    print('Done. Found ' + str(nontoxic.shape[0]) + ' nontoxic compounds')
    np.save('./data/nontoxic.npy', nontoxic)
    print('Saved.')

def main():
    parse_hsdb()
    parse_chemid()

if __name__ == '__main__':
    main()
