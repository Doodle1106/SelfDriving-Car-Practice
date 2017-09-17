import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import cv2 as cv

# Global parameters############################################################

# Gaussian smoothing
kernel_size = 3

# Canny Edge Detector
low_threshold = 50
high_threshold = 150

# Region-of-interest vertices
# We want a trapezoid shape, with bottom edge at the bottom of the image
trap_bottom_width = 0.85  # width of bottom edge of trapezoid, expressed as percentage of image width
trap_top_width = 0.07  # ditto for top edge of trapezoid
trap_height = 0.4  # height of the trapezoid expressed as percentage of image height

# Hough Transform
rho = 2 # distance resolution in pixels of the Hough grid
theta = 1 * np.pi/180 # angular resolution in radians of the Hough grid
threshold = 15     # minimum number of votes (intersections in Hough grid cell)
min_line_length = 10 #minimum number of pixels making up a line
max_line_gap = 20    # maximum gap in pixels between connectable line segments
##################################################################

def load_image(image_name):
    image = cv.imread(image_name)
    #print('this image is of type :',type(image),'with dimension :',image.shape)
    img = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    img = cv.GaussianBlur(img,(3,3),0)
    img = cv.Canny(img,low_threshold,high_threshold)
    lines = cv.HoughLinesP(img, 1, np.pi/180, 180, 20, 15)
    draw_lanes_method3(image,lines,color=[0,0,255],thickness=10)

    while True:
        cv.imshow('raw image',image)
        if cv.waitKey(25) & 0xFF == ord('q'):
            break


def draw_lanes_method3(img, lines, color, thickness):
    draw_right = True
    draw_left = True
    slope_threshold = 0.5
    slopes = []
    new_lines = []

    for line in lines:
        x1, y1, x2, y2 = line[0]
        # Calculate slope
        if x2 - x1 == 0.:  # corner case, avoiding division by 0
            slope = 999.  # practically infinite slope
        else:
            slope = (y2 - y1) / (x2 - x1)
        if abs(slope) > slope_threshold:
            slopes.append(slope)
            new_lines.append(line)

    lines = new_lines

    #find right and left lines
    right_lines = []
    left_lines = []
    for i, line in enumerate(lines):
        x1, y1, x2, y2 = line[0]
        img_x_center = img.shape[1] / 2
        if slopes[i] > 0 and x1 > img_x_center and x2 > img_x_center:
            right_lines.append(line)
        elif slopes[i] < 0 and x1 < img_x_center and x2 < img_x_center:
            left_lines.append(line)

    right_lines_x = []
    right_lines_y = []

    for line in right_lines:
        x1, y1, x2, y2 = line[0]

        right_lines_x.append(x1)
        right_lines_x.append(x2)

        right_lines_y.append(y1)
        right_lines_y.append(y2)

        if len(right_lines_x) > 0:
            right_m, right_b = np.polyfit(right_lines_x, right_lines_y, 1)  # y = m*x + b
        else:
            right_m, right_b = 1, 1
            draw_right = False

    left_lines_x = []
    left_lines_y = []

    for line in left_lines:
        x1, y1, x2, y2 = line[0]

        left_lines_x.append(x1)
        left_lines_x.append(x2)

        left_lines_y.append(y1)
        left_lines_y.append(y2)

    if len(left_lines_x) > 0:
        left_m, left_b = np.polyfit(left_lines_x, left_lines_y, 1)  # y = m*x + b
    else:
        left_m, left_b = 1, 1
        draw_left = False

    y1 = img.shape[0]
    y2 = img.shape[0] * (1 - trap_height)

    right_x1 = (y1 - right_b) / right_m
    right_x2 = (y2 - right_b) / right_m

    left_x1 = (y1 - left_b) / left_m
    left_x2 = (y2 - left_b) / left_m

    y1 = int(y1)
    y2 = int(y2)
    right_x1 = int(right_x1)
    right_x2 = int(right_x2)
    left_x1 = int(left_x1)
    left_x2 = int(left_x2)

    if draw_right:
        print('right lanes found, drawing right lanes')
        cv.line(img, (right_x1, y1), (right_x2, y2), color, thickness)
    if draw_left:
        print('left lanes found, drawing left lanes')
        cv.line(img, (left_x1, y1), (left_x2, y2), color, thickness)

def region_of_interest(img, vertices):
    mask = np.zeros_like(img)
    cv.fillPoly(mask, vertices)
    masked_image = cv.bitwise_and(img, mask)
    return masked_image

#load_image('0.jpg')
