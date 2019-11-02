import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from joblib import dump

toxic = np.load('./data/toxic.npy')
toxic = toxic.reshape(toxic.shape[0], -1)
labels1 = np.zeros((toxic.shape[0], 2))
labels1[:,0] = 1

print(toxic.shape)
print(labels1.shape)

nontoxic = np.load('./data/nontoxic.npy')
nontoxic = nontoxic.reshape(nontoxic.shape[0], -1)
labels2 = np.zeros((nontoxic.shape[0], 2))
labels2[:,1] = 1

print(nontoxic.shape)
print(labels2.shape)

X = np.concatenate([toxic, nontoxic])
y = np.concatenate([labels1, labels2])

X_train, X_test, y_train, y_test = train_test_split(X, y)

mlp = MLPClassifier(alpha=1, max_iter=1000, verbose=1)
mlp.fit(X_train, y_train)
print("Training set score: %f" % mlp.score(X_train, y_train))
print("Test set score: %f" % mlp.score(X_test, y_test))
dump(mlp, './models/mlp.joblib')
