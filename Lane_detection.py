import numpy as np
import cv2 as cv
from screen_capture import grab_screen
from image_process import process_image
import time

print ("press q to quit")

#EDIT settings here
real_time_flag = True
do_roi = False
image_name = '2.jpeg'
######################

#process one single image and conduct BGR2GRAY, CANNY, GAUSSIAN BLUR
def test_mode():
    while True:
        last_time = time.time()
        raw_img=cv.imread(image_name)
        process_image(raw_img, do_roi)
        print('loop took {} seconds'.format(time.time() - last_time))
        if cv.waitKey(25) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break

def real_time_mode():
    while True:
        last_time = time.time()
        screen = grab_screen(region=(0, 40, 800, 600))
        screen = cv.cvtColor(screen,cv.COLOR_BGR2RGB)
        cv.imshow("Real time screendddddd",screen)
        process_image(screen,do_roi)
        print('loop took {} seconds'.format(time.time() - last_time))
        if cv.waitKey(25) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break

def main():

    if (real_time_flag):
        real_time_mode()
    else:
        test_mode()



main()