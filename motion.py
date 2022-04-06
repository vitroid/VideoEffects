#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
#動くものを撮影することを拒否するカメラ。

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
    file = 0
    if len(sys.argv) > 1:
        file = sys.argv[1]

    # cap = cv2.VideoCapture(file)

    #cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture('/Users/matto/Stitch tmp2/IMG_0565_2.mp4')
    # cap = cv2.VideoCapture('/Users/matto/Downloads/shijokiyamachi.mp4')
    # cap = cv2.VideoCapture('/Users/matto/Downloads/shibuya.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/littleitaly.mp4')
    cap = cv2.VideoCapture('/Users/matto/Downloads/akiba.mp4')
    # cap = cv2.VideoCapture('/Users/matto/Downloads/akiba2.mov')
    #cap = cv2.VideoCapture('/Users/matto/Movies/iMovie Events.localized/SlitCam 2013-11-12/clip-2013-11-12 14;07;39.mov')
    # cap = cv2.VideoCapture('/Users/matto/Downloads/shibuya2.mp4')
    #https://www.youtube.com/watch?v=kw3MEiTKbpk
    ret, frame = cap.read()
    # fgbg = cv2.createBackgroundSubtractorMOG2()
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False, varThreshold=64)
    # fgbg = cv2.createBackgroundSubtractorMOG(detectShadows=False)

    #make a deep picture stack
    accum = 50
    width, height = frame.shape[:2]
    motion = np.zeros((width,height,3), dtype=np.uint8)
    static = np.zeros((width,height,3), dtype=np.uint8)

    #fps = 15
    #capSize = (width,height) # this is the size of my source video
    #fourcc = cv2.VideoWriter_fourcc('m','p','4','v') # note the lower case
    #fourcc = cv2.VideoWriter_fourcc('m','j','p','g') # note the lower case
    #vout = cv2.VideoWriter()
    #success = vout.open('motion720p.mov',fourcc,fps,capSize,True)
    nframe = 0
    while True:
        for i in range(5):
            ret, frame = cap.read()
        #print ret
        if not ret:
            break
        # 動体のマスク画像を取得
        cv2.imshow("Input",frame)
        # key = cv2.waitKey(0)
        fgmask = fgbg.apply(frame)
        # ゴマ塩ノイズ除去
        fgmask = cv2.medianBlur(fgmask,7)
        #反転mask
        fgksam = inverte(fgmask)

        #ksamed = cv2.bitwise_and(frame,frame,mask = fgksam)
        masked = cv2.bitwise_and(frame,frame,mask = fgmask)

        #static = cv2.bitwise_and(static,static,mask = fgmask)
        #static = cv2.add(static,ksamed)
        #motion[0:width-3,:,:] = motion[3:width,:,:]
        motion = cv2.bitwise_and(motion,motion,mask = fgksam)
        motion = cv2.add(motion,masked)
        # 各画像の表示
        #cv2.imshow("Input",frame)
        #cv2.imshow("Motion Mask",masked)
        #cv2.imshow("Mask",fgmask)
        #cv2.imshow("Majority",majority)
        #cv2.imshow("Static",static)
        cv2.imshow("Motion",motion)
        #vout.write(motion)
        #cv2.imwrite("motion/%05d.jpg" % nframe,motion)
        nframe += 1
        key = cv2.waitKey(10)
        # 空白キー以外のキーが押されたら終了
        if key > 0:
            #cv2.imwrite("Input.jpg",frame)
            #cv2.imwrite("Motion_mask.jpg",fgmask)
            break

    cap.release()
    #vout.release()
    #vout = None
    cv2.destroyAllWindows()
