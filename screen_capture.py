#this function is inspired by the following website:
#https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api


def grab_screen(region=None):
    #https://msdn.microsoft.com/en-us/library/windows/desktop/ms633504(v=vs.85).aspx
    #Retrieves a handle to the desktop window. The desktop window covers the entire screen.
    # The desktop window is the area on top of which other windows are painted.
    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:

        #https://msdn.microsoft.com/en-us/library/windows/desktop/ms724385(v=vs.85).aspx
        #Retrieves the specified system metric or system configuration setting.
        #Note that all dimensions retrieved by GetSystemMetrics are in pixels.
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        print(width)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        print(height)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        print(left)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        print(top)

    #The GetWindowDC function retrieves the device context (DC) for
    # the entire window, including title bar, menus, and scroll bars.
    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)

