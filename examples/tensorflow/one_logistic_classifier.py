#/usr/bin/env python3

# These are all the modules we'll be using later. Make sure you can import them
# before proceeding further.
from __future__ import print_function
import imageio
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import tarfile
from IPython.display import display, Image
from sklearn.linear_model import LogisticRegression
from six.moves.urllib.request import urlretrieve
from six.moves import cPickle as pickle

url = 'https://commondatastorage.googleapis.com/books1000/'
last_percent_reported = None
data_root = '/Users/sam/srpub/examples/tensorflow/data/' # Change me to store data elsewhere

pickle_file = os.path.join(data_root, 'notMNIST.pickle')

data = pickle.load( open( pickle_file, "rb" ) )

print(data.keys())
train_dataset = data['train_dataset']
train_labels = data['train_labels']
valid_dataset = data['valid_dataset']
valid_labels = data['valid_labels']
test_dataset = data['test_dataset']
test_labels = data['test_labels']

NUM_SAMPLES = 5000
#model = LogisticRegression(penalty='l2', C=1.0)
model = LogisticRegression()

#range_low = i * CHUNK_SIZE
#print(i, ":", range_low)
#range_high = range_low + CHUNK_SIZE

train_sample = train_dataset[:NUM_SAMPLES,:,:]
train_sample_labels = train_labels[:NUM_SAMPLES]

(samples, width, height) = train_sample.shape
train_sample = np.reshape(train_sample, (samples, width * height))
print('\tTraining Reshaped:', train_sample.shape)

(samples, width, height) = test_dataset.shape
test_dataset_reshaped = np.reshape(test_dataset, (samples, width * height))

model = model.fit(train_sample, train_sample_labels)

train_score = model.score(train_sample, train_sample_labels)
test_score = model.score(test_dataset_reshaped, test_labels)
print('\tTraining score = ', train_score)
print('\tTest score = ', test_score)
