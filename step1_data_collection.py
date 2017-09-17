#this is the first step before training the Neural Network, it collects screen image data
#as well as corresponding commands you type into
#eg: it takes down left, right and moving forward command

import numpy as np
from screen_capture import grab_screen
import cv2 as cv
import time
from getkeys import key_check
import os

#############Global Variable###########
show_resized_image = False
file_name = 'training_data-{}.npy'.format(time.strftime('%Y-%m-%d',time.localtime(time.time())))
desired_size_of_training_data = 50
w = [1,0,0,0,0]
s = [0,1,0,0,0]
a = [0,0,1,0,0]
d = [0,0,0,1,0]
afk = [0,0,0,0,1]
#######################################

def keys_to_output(keys):
    if 'W' in keys:
        output = w
    elif 'S' in keys:
        output = s
    elif 'A' in keys:
        output = a
    elif 'D' in keys:
        output = d
    else:
        output = afk
    return output

def collect_data():

    training_data = []
    for i in [3,2,1]:
        print('system initializing :',i)
        time.sleep(1)
    print('start!')
    time.sleep(1.5)


    while True:
        start_time = time.time()
        screen_image = grab_screen(region =(0,40,600,480))
        loop_time = time.time() - start_time
        print('This iteration caused :',loop_time)
        screen_image = cv.resize(screen_image,(60,48))
        screen_image = cv.cvtColor(screen_image,cv.COLOR_BGR2RGB)

        keys = key_check()
        output = keys_to_output(keys)
        training_data.append([screen_image,output])
        print('Number of samples in training data : ',len(training_data))

        if desired_size_of_training_data == len(training_data):
            np.save(file_name, training_data)
            print('Number of preset data sample reached ',desired_size_of_training_data,', Data Saved to',file_name)
            break


collect_data()