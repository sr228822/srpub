# These are all the modules we'll be using later. Make sure you can import them
# before proceeding further.
from __future__ import print_function

import os
import sys
import tarfile

import imageio
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import display, Image
from six.moves import cPickle as pickle
from six.moves.urllib.request import urlretrieve
from sklearn.linear_model import LogisticRegression
