#/usr/bin/python

# These are all the modules we'll be using later. Make sure you can import them
# before proceeding further.
from __future__ import print_function
import imageio
import matplotlib.pyplot as plt
import os
import sys
import tarfile
from IPython.display import display, Image

import numpy as np
os.environ['TF_CPP_MIN_LOG_LEVEL']='2'
import tensorflow as tf

from six.moves import cPickle as pickle
from six.moves import range

data_root = '/Users/sam/learning/data/' # Change me to store data elsewhere
last_percent_reported = None

pickle_file = os.path.join(data_root, 'notMNIST.pickle')

with open(pickle_file, 'rb') as f:
  save = pickle.load(f)
  train_dataset = save['train_dataset']
  train_labels = save['train_labels']
  valid_dataset = save['valid_dataset']
  valid_labels = save['valid_labels']
  test_dataset = save['test_dataset']
  test_labels = save['test_labels']
  del save  # hint to help gc free up memory
  print('Training set', train_dataset.shape, train_labels.shape)
  print('Validation set', valid_dataset.shape, valid_labels.shape)
  print('Test set', test_dataset.shape, test_labels.shape)

image_size = 28
num_labels = 10

def reformat(dataset, labels):
  dataset = dataset.reshape((-1, image_size * image_size)).astype(np.float32)
  # Map 0 to [1.0, 0.0, 0.0 ...], 1 to [0.0, 1.0, 0.0 ...]
  labels = (np.arange(num_labels) == labels[:,None]).astype(np.float32)
  return dataset, labels
train_dataset, train_labels = reformat(train_dataset, train_labels)
valid_dataset, valid_labels = reformat(valid_dataset, valid_labels)
test_dataset, test_labels = reformat(test_dataset, test_labels)
print('Training set', train_dataset.shape, train_labels.shape)
print('Validation set', valid_dataset.shape, valid_labels.shape)
print('Test set', test_dataset.shape, test_labels.shape)

INITIAL_LEARNING_RATE = 0.3

BETA = 0.03

# With gradient descent training, even this much data is prohibitive.
# Subset the training data for faster turnaround.
NUM_HIDDEN_ONE = 1024
NUM_HIDDEN_TWO = 300
#NUM_HIDDEN = 2048

num_steps = 3001
#num_steps = 5500

batch_size = 128
#batch_size = 256

graph = tf.Graph()
with graph.as_default():

  # Input data. For the training data, we use a placeholder that will be fed
  # at run time with a training minibatch.
  tf_train_dataset = tf.placeholder(tf.float32,
                                    shape=(batch_size, image_size * image_size))
  tf_train_labels = tf.placeholder(tf.float32, shape=(batch_size, num_labels))
  tf_valid_dataset = tf.constant(valid_dataset)
  tf_test_dataset = tf.constant(test_dataset)
  
  # Variables.
  weights1 = tf.Variable(
    tf.truncated_normal([image_size * image_size, NUM_HIDDEN_ONE]))
  biases1 = tf.Variable(tf.zeros([NUM_HIDDEN_ONE]))

  weights2 = tf.Variable(
    tf.truncated_normal([NUM_HIDDEN_ONE, NUM_HIDDEN_TWO]))
  biases2 = tf.Variable(tf.zeros([NUM_HIDDEN_TWO]))

  weights3 = tf.Variable(
    tf.truncated_normal([NUM_HIDDEN_TWO, num_labels]))
  biases3 = tf.Variable(tf.zeros([num_labels]))

  # Placeholder to control dropout probability.
  keep_prob = tf.placeholder(tf.float32)

  # Training computation.
  def forward_prop(input):
    h1 = tf.nn.relu(tf.matmul(input, weights1) + biases1)
    h1_drop = tf.nn.dropout(h1, keep_prob)

    h2 = tf.nn.relu(tf.matmul(h1_drop, weights2) + biases2)
    h2_drop = tf.nn.dropout(h2, keep_prob)

    return tf.matmul(h2_drop, weights3) + biases3

  # Training computation.
  logits = forward_prop(tf_train_dataset)
  loss = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=tf_train_labels, logits=logits))
  loss += BETA * (tf.nn.l2_loss(weights1) + tf.nn.l2_loss(weights2) + tf.nn.l2_loss(weights3))

  # Optimizer w/ learning rate decay.
  global_step = tf.Variable(0)
  learning_rate = tf.train.exponential_decay(INITIAL_LEARNING_RATE, global_step, 1000, 0.9)
  #learning_rate = INITIAL_LEARNING_RATE
  
  # Optimizer.
  optimizer = tf.train.GradientDescentOptimizer(learning_rate).minimize(loss, global_step=global_step)
  
  # Predictions for the training, validation, and test data.
  train_prediction = tf.nn.softmax(logits)
  valid_prediction = tf.nn.softmax(forward_prop(tf_valid_dataset))
  test_prediction = tf.nn.softmax(forward_prop(tf_test_dataset))

def accuracy(predictions, labels):
  return (100.0 * np.sum(np.argmax(predictions, 1) == np.argmax(labels, 1))
          / predictions.shape[0])

with tf.Session(graph=graph) as session:
  tf.global_variables_initializer().run()
  print("Initialized")
  for step in range(num_steps):
    # Pick an offset within the training data, which has been randomized.
    # Note: we could use better randomization across epochs.
    offset = (step * batch_size) % (train_labels.shape[0] - batch_size)
    # Generate a minibatch.
    batch_data = train_dataset[offset:(offset + batch_size), :]
    batch_labels = train_labels[offset:(offset + batch_size), :]
    # Prepare a dictionary telling the session where to feed the minibatch.
    # The key of the dictionary is the placeholder node of the graph to be fed,
    # and the value is the numpy array to feed to it.
    feed_dict_drop = {tf_train_dataset : batch_data, tf_train_labels : batch_labels, keep_prob:0.5}
    feed_dict = {tf_train_dataset : batch_data, tf_train_labels : batch_labels, keep_prob:1.0}
    _, l, predictions = session.run(
      [optimizer, loss, train_prediction], feed_dict=feed_dict_drop)
    if (step % 500 == 0):
      print("Minibatch loss at step %d: %f" % (step, l))
      print("Minibatch accuracy: %.1f%%" % accuracy(predictions, batch_labels))
      print("Validation accuracy: %.1f%%" % accuracy(
        valid_prediction.eval(feed_dict=feed_dict), valid_labels))
    #if (step % 100 == 0):
    #    print("Test accuracy: %.1f%%" % accuracy(test_prediction.eval(), test_labels))
  print("Test accuracy: %.1f%%" % accuracy(test_prediction.eval(feed_dict=feed_dict), test_labels))
