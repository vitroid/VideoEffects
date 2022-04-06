#!/usr/bin/env python
# -*- coding: utf-8 -*-
#動くものを撮影することを拒否するカメラ。

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

    cap = cv2.VideoCapture(file)
    #cap = cv2.VideoCapture('/Users/matto/Stitch tmp2/IMG_0565_2.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/shijokiyamachi.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/shibuya.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/littleitaly.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/akiba.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/chiyoda720p.mp4')
    ret, frame = cap.read()
    frame = cv2.resize(frame,None,fx=0.25,fy=0.25)
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False)

    #make a deep picture stack
    tolerance = 20
    width, height = frame.shape[:2]
    stack = np.zeros((width,height,3,tolerance), dtype=np.float32)
    stacksum = np.zeros((width,height,3), dtype=np.float32)
    #stack = np.zeros((tolerance, width,height,3), dtype=np.float32)
    #stacksum = np.zeros((width,height,3), dtype=np.float32)
    majority = np.zeros((width,height,3), dtype=np.uint8)

    #fps = 15
    #capSize = (width,height) # this is the size of my source video
    #fourcc = cv2.VideoWriter_fourcc('m','p','4','v') # note the lower case
    #vout = cv2.VideoWriter()
    #success = vout.open('majority.mov',fourcc,fps,capSize,True)
    nframe = 0
    lasttime = time.time()
    while True:
        for i in range(10):
            ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame,None,fx=0.25,fy=0.25)
        # 動体のマスク画像を取得
        fgmask = fgbg.apply(frame)
        # ノイズを減らす。
        fgmask = cv2.medianBlur(fgmask,7)
        #fgmask[x,y]==0なピクセルにのみ処理を行う。
        stacksum[fgmask==0,:] += frame[fgmask==0,:] - stack[fgmask==0,:,tolerance-1]
        stack[fgmask==0,:,1:tolerance] = stack[fgmask==0,:,0:tolerance-1]
        stack[fgmask==0,:,0] = frame[fgmask==0,:]
        #stacksum[fgmask==0,:] += frame[fgmask==0,:] - stack[tolerance-1,fgmask==0,:]
        #stack[1:tolerance,fgmask==0,:] = stack[0:tolerance-1,fgmask==0,:]
        #stack[0,fgmask==0,:] = frame[fgmask==0,:]
        majority = (stacksum / tolerance).astype(np.uint8)

        # 各画像の表示
        #cv2.imshow("Input",frame)
        #cv2.imshow("Motion Mask",masked)
        now = time.time()
        duration,lasttime = now - lasttime, now
        print("{} sec.".format(duration))
        cv2.imshow("Majority",majority)
        cv2.imshow("Frame",frame)
        #cv2.imwrite("majority2-t%d/%05d.jpg" % (tolerance,nframe),majority)
        #vout.write(majority)
        nframe += 1
        key = cv2.waitKey(10)
        if key > 0:
            cv2.imwrite("Input.jpg",frame)
            cv2.imwrite("Motion_mask.jpg",fgmask)
            break

    cap.release()
    #vout.release()
    #vout = None
    cv2.destroyAllWindows()
