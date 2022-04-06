#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import time
import sys

def inverte(imagem):
    imagem = (255-imagem)
    return imagem



def split_into_rgb_channels(image):
  '''Split the target image into its red, green and blue channels.
  image - a numpy array of shape (rows, columns, 3).
  output - three numpy arrays of shape (rows, columns) and dtype same as
           image, containing the corresponding channels.
  '''
  red = image[:,:,2]
  green = image[:,:,1]
  blue = image[:,:,0]
  return red, green, blue

if __name__ == '__main__':
    file = 0
    if len(sys.argv) > 1:
        file = sys.argv[1]

    #cap = cv2.VideoCapture(file)
    #cap = cv2.VideoCapture('/Users/matto/Stitch tmp2/IMG_0565_2.mp4')
    cap = cv2.VideoCapture('/Users/matto/Downloads/VII+Pla+Cri2.mov')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/shijokiyamachi.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/shibuya.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/littleitaly.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/akiba.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/chiyoda720p.mp4')
    #ret, frame = cap.read()
    for i in range(810):
        cap.grab()
    ret, frame = cap.retrieve()
    #frame = cv2.resize(frame,None,fx=0.25,fy=0.25)

    #make a deep picture stack
    tolerance = 20
    width, height = frame.shape[:2]
    stack = np.zeros((width,height,3,tolerance), dtype=np.float32)
    stacksum = np.zeros((width,height,3), dtype=np.float32)
    #stack = np.zeros((tolerance, width,height,3), dtype=np.float32)
    #stacksum = np.zeros((width,height,3), dtype=np.float32)
    average = np.zeros((width,height,3), dtype=np.uint8)

    #fps = 30
    #capSize = (width,height) # this is the size of my source video
    #fourcc = cv2.VideoWriter_fourcc('a','v','c','1') # note the lower case
    #vout = cv2.VideoWriter()
    #success = vout.open('motionblur.m4v',fourcc,fps,capSize,True)
    nframe = 0
    lasttime = time.clock()
    while True:
        #for i in range(10):
        #ret, frame = cap.read()
        cap.grab()
        ret, frame = cap.retrieve()
        if not ret:
            break
        #frame = cv2.resize(frame,None,fx=0.25,fy=0.25)
        stacksum[:,:,:] += frame[:,:,:] - stack[:,:,:,tolerance-1]
        stack[:,:,:,1:tolerance] = stack[:,:,:,0:tolerance-1]
        stack[:,:,:,0] = frame[:,:,:]

        average = (stacksum / tolerance).astype(np.uint8)

        # 各画像の表示
        #cv2.imshow("Input",frame)
        #cv2.imshow("Motion Mask",masked)
        now = time.clock()
        duration,lasttime = now - lasttime, now
        print("{} sec.".format(duration))
        cv2.imshow("Majority",average)
        cv2.imwrite("motionblur-t%d/%05d.jpg" % (tolerance,nframe),average)
        #vout.write(average)
        nframe += 1
        key = cv2.waitKey(10)
        if key > 0:
            break

    cap.release()
    #vout.release()
    #vout = None
    cv2.destroyAllWindows()
