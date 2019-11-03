#!/usr/bin/env python3

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten
from keras.utils import to_categorical
from keras.callbacks import ModelCheckpoint

toxic = np.load('./data/toxic.npy')
labels1 = np.full((toxic.shape[0]), 0)
print('Toxic Compounds:')
print(toxic.shape)
print(labels1.shape)

nontoxic = np.load('./data/nontoxic.npy')
labels2 = np.full((nontoxic.shape[0]), 1)

print('Nontoxic Compounds:')
print(nontoxic.shape)
print(labels2.shape)

X = np.concatenate([toxic, nontoxic])
y = np.concatenate([labels1, labels2])

# Normalize data
print('Min:', X.min()) # -176
print('Max:', X.max()) # 486
X = (X + 176) / (486+176)

# Calculate class weight
cw = class_weight.compute_class_weight('balanced', np.unique(y), y)
cw = dict(enumerate(cw))
print(cw)

y = to_categorical(y)
#X_train, X_test, y_train, y_test = train_test_split(X, y)

# Create model
model = Sequential()

# Add model layers
model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(7, 18, 15)))
model.add(Conv2D(32, kernel_size=3, activation='relu'))
model.add(Flatten())
model.add(Dense(2, activation='softmax'))

# Compile model
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train model
filepath = "./models/model-{epoch:02d}-{accuracy:.2f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='accuracy', verbose=1, save_best_only=False, mode='max')
num_epochs = 100
model.fit(X, y, epochs=num_epochs, class_weight = cw, callbacks = [checkpoint])

# Save model
model.save('./models/model.h5')
