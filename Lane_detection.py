import numpy as np
import cv2 as cv
from screen_capture import grab_screen
from image_process import process_image
#EDIT settings here
real_time_flag = True
do_roi = False
print ("press q to quit")
######################

#process one single image and conduct BGR2GRAY, CANNY, GAUSSIAN BLUR
def test_mode():
    raw_img=cv.imread('2.jpeg')
    process_image(raw_img, do_roi)

def real_time_mode():
    while True:
        screen = grab_screen(region=(0, 40, 800, 600))
        screen = cv.cvtColor(screen,cv.COLOR_BGR2RGB)
        cv.imshow("Real time screendddddd",screen)
        process_image(screen,do_roi)
        if cv.waitKey(25) & 0xFF == ord('q'):
            cv.destroyAllWindows()
            break

def main():

    if (real_time_flag):
        real_time_mode()
    else:
        test_mode()



main()