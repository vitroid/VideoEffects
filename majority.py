#!/usr/bin/python2.7
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

    #cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture('/Users/matto/Stitch tmp2/IMG_0565_2.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/shijokiyamachi.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/shibuya.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/littleitaly.mp4')
    #cap = cv2.VideoCapture('/Users/matto/Downloads/akiba.mp4')
    # cap = cv2.VideoCapture('/Users/matto/Downloads/chiyoda720p.mp4')
    cap = cv2.VideoCapture(sys.argv[1])
    ret, frame = cap.read()
    #fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False)
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()

    #make a deep picture stack
    accum = 10
    width, height = frame.shape[:2]
    stack = np.zeros((width,height,3), dtype=np.float32)
    weight = np.zeros((width,height), dtype=np.float32)
    majority = np.zeros((width,height,3), dtype=np.uint8)
    imagequeue = []
    weightqueue = []

    #fps = 15
    #capSize = (width,height) # this is the size of my source video
    #fourcc = cv2.VideoWriter_fourcc('m','p','4','v') # note the lower case
    #vout = cv2.VideoWriter()
    #success = vout.open('majority.mov',fourcc,fps,capSize,True)
    nframe = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        # if nframe in (1,2):
        #     cv2.imwrite("im{0}.jpg".format(nframe), frame)
        # 動体のマスク画像を取得
        fgmask = fgbg.apply(frame)
        # ノイズを減らす。
        fgmask = cv2.medianBlur(fgmask,7)
        #gray 画像の生成
        #im_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #動かない部分のマスク。
        fgksam = inverte(fgmask)
        #積算。
        #抜けを生じさせないためには、ピクセル単位での積算が欲しいが、そんなことできるか?できるはず。
        #stack  += fgksam*im_gray
        masked = cv2.bitwise_and(frame,frame,mask = fgksam)
        bitweight = fgksam / 255
        stack  += masked
        weight += bitweight
        #本当はピクセル単位で、最新の10点程度の平均をとれば良いのだが、それは処理が重くなる。
        #一番サンプルが少ないところにあわせ、画像を貯めつづける。
        minweight = np.amin(weight)
        #保存
        imagequeue.append(masked)
        weightqueue.append(bitweight)
        #if len(imagequeue) > accum:
        if minweight > accum:
            print("{} Queue Length".format(len(imagequeue)))
            lastimage = imagequeue.pop(0)
            lastweight = weightqueue.pop(0)
            stack  -= lastimage
            weight -= lastweight
        #majority == background
        #normalize three channels
        majority[:,:,0] = stack[:,:,0] / weight
        majority[:,:,1] = stack[:,:,1] / weight
        majority[:,:,2] = stack[:,:,2] / weight

        # 各画像の表示
        #cv2.imshow("Input",frame)
        #cv2.imshow("Motion Mask",masked)
        cv2.imshow("Majority",majority)
        # cv2.imwrite("majority/%05d.jpg" % nframe,majority)
        #vout.write(majority)
        nframe += 1
        key = cv2.waitKey(10)
        # 空白キー以外のキーが押されたら終了
        if key > 0:
            # cv2.imwrite("Input.jpg",frame)
            # cv2.imwrite("Motion_mask.jpg",fgmask)
            break

    cap.release()
    #vout.release()
    #vout = None
    cv2.destroyAllWindows()
