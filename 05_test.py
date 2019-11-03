#!/usr/bin/env python3

import numpy as np
from keras.models import load_model
from os import listdir

toxic = np.load('./data/toxic.npy')
labels1 = np.zeros((toxic.shape[0], 2))
labels1[:,0] = 1

nontoxic = np.load('./data/nontoxic.npy')
labels2 = np.zeros((nontoxic.shape[0], 2))
labels2[:,1] = 1

weights = listdir('./models')
weights.sort()
tox_acc = list()
non_acc = list()
diffs = list()

for f in weights:
    model = load_model('./models/' + f)

    arr = model.predict(toxic)
    correct = np.where(arr[:,0] > arr[:,1])[0].shape[0]
    a1 = correct/arr.shape[0]
    tox_acc.append(a1)

    arr = model.predict(nontoxic)
    correct = np.where(arr[:,1] > arr[:,0])[0].shape[0]
    a2 = correct/arr.shape[0]
    non_acc.append(a2)

    diffs.append(abs(a1-a2))

    print(f, 'tox_acc:', a1, ', non_acc:', a2)

i = diffs.index(min(diffs))
print(weights[i])
print(tox_acc[i])
print(non_acc[i])
