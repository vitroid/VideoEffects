#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import cv2
import numpy as np
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

    w = 1
    rewind = 0
    dir = 0 #left to right
    file = 0
    while len(sys.argv)>1:
        arg = sys.argv.pop(1)
        if arg == '-r':
            rewind = int(sys.argv.pop(1))
        elif arg == '-w':
            w      = int(sys.argv.pop(1))
        elif arg == '-d':
            dir    = int(sys.argv.pop(1))
        elif arg[0] != '-':
            file = arg
    cap = cv2.VideoCapture(file)
    for i in range(1+rewind):
        ret, frame = cap.read()
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

    #make a deep picture stack
    accum = 50
    width, height = frame.shape[:2]
    image = np.zeros((width,height,3), dtype=np.uint8)

    #fps = 15
    #capSize = (width,height) # this is the size of my source video
    #fourcc = cv2.VideoWriter_fourcc('m','p','4','v') # note the lower case
    #fourcc = cv2.VideoWriter_fourcc('m','j','p','g') # note the lower case
    #vout = cv2.VideoWriter()
    #success = vout.open('motion720p.mov',fourcc,fps,capSize,True)
    nframe = 0
    wend = (height,width,height,width)
    while True:
        for i in (0,):
            ret, frame = cap.read()
        #print nframe
        if not ret:
            print ("No frame.")
            break
        if nframe>=wend[dir]:
            print ("Width completed.")
            break
        #from top to bottom
        #image[nframe,:,:] = frame[nframe,:,:]
        if dir == 0:
            #from left to right
            image[:,nframe:nframe+w,:] = frame[:,nframe:nframe+w,:]
        if dir == 2:
            #from left to right
            image[:,height-w-nframe:height-nframe,:] = frame[:,height-w-nframe:height-nframe,:]
        half = cv2.resize(image,None,fx=0.5,fy=0.5)
        cv2.imshow("image",half)
        #vout.write(motion)
        #cv2.imwrite("motion/%05d.jpg" % nframe,motion)
        nframe += w
        key = cv2.waitKey(10)
        # 空白キー以外のキーが押されたら終了
        if key > 0:
            #cv2.imwrite("Input.jpg",frame)
            #cv2.imwrite("Motion_mask.jpg",fgmask)
            break
    if file == 0:
        file = "Image"
    cv2.imwrite("{}-{}x{}+{}.jpg".format(file,dir,w,rewind),image)
    cap.release()
    #vout.release()
    #vout = None
    cv2.destroyAllWindows()
