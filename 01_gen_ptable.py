import numpy as np

arr = np.chararray((7,18,15),itemsize=2) # Periodic table
arr[:] = ''
# Period 1
arr[0,0,0] = 'H'
arr[0,17,0] = 'He'
# Period 2
arr[1,0:2,0] = ['Li','Be']
arr[1,12:,0] = ['B','C','N','O','F','Ne']
# Period 3
arr[2,0:2,0] = ['Na','Mg']
arr[2,12:,0] = ['Al','Si','P','S','Cl','Ar']
# Period 4
arr[3,:,0] = ['K','Ca','Sc','Ti','V','Cr','Mn','Fe','Co','Ni','Cu','Zn','Ga','Ge','As','Se','Br','Kr']
# Period 5
arr[4,:,0] = ['Rb','Sr','Y','Zr','Nb','Mo','Tc','Ru','Rh','Pd','Ag','Cd','In','Sn','Sb','Te','I','Xe']
# Period 6
arr[5,:,0] = ['Cs','Ba','La','Hf','Ta','W','Re','Os','Ir','Pt','Au','Hg','Tl','Pb','Bi','Po','At','Rn']
# Period 7
arr[6,:,0] = ['Fr','Ra','Ac','Rf','Db','Sg','Bh','Hs','Mt','Ds','Rg','Cn','Nh','Fl','Mc','Lv','Ts','Og']
# Lanthinide series
arr[5,2,:] = ['La','Ce','Pr','Nd','Pm','Sm','Eu','Gd','Tb','Dy','Ho','Er','Tm','Yb','Lu']
# Actinide series
arr[6,2,:] = ['Ac','Th','Pa','U','Np','Pu','Am','Cm','Bk','Cf','Es','Fm','Md','No','Lr']

np.save('./data/ptable.npy', arr)
