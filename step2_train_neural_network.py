import numpy as np
from screen_capture import grab_screen
import cv2
import time
import os
import pandas as pd
from tqdm import tqdm
from collections import deque
from random import shuffle

from inception_v3 import googlenet

import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d,avg_pool_2d, conv_3d, max_pool_3d, avg_pool_3d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.merge_ops import merge

###Set which training_data.npy to use for training###
file_name = 'training_data-2017-09-17.npy'
WIDTH = 60
HEIGHT = 48
LR = 1e-3
MODEL_NAME = 'dod'
model = googlenet(WIDTH, HEIGHT, 3, LR, output=9, model_name=MODEL_NAME)
#####################################################

def train_model():
    training_data = np.load(file_name)
    print('There are ',len(training_data),'samples in the file')
    time.sleep(2)

    # train_set = training_data[:(-0.2*len(training_data))]
    # test_set = training_data[(-0.2*len(training_data)):]

    train_set = training_data[:-10]
    test_set = training_data[-10:]

    X = np.array([i[0] for i in train_set]).reshape(-1, WIDTH, HEIGHT, 3)
    Y = [i[1] for i in train_set]

    test_x = np.array([i[0] for i in test_set]).reshape(-1, WIDTH, HEIGHT, 3)
    test_y = [i[1] for i in test_set]

    model.fit({'input': X}, {'targets': Y}, n_epoch=1, validation_set=({'input': test_x}, {'targets': test_y}),
                snapshot_step=2500, show_metric=True, run_id=MODEL_NAME)
    print('Training Finished')
    model.save(MODEL_NAME)


train_model()