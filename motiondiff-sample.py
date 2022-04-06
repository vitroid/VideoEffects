#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

#taken from
#http://python-gazo.blog.jp/opencv/フレーム間差分法
#http://python-gazo.blog.jp/opencv/動体領域抽出

import cv2
import numpy as np

def flame_sub(im1,im2,im3,th,blur):

    d1 = cv2.absdiff(im3, im2)
    d2 = cv2.absdiff(im2, im1)
    diff = cv2.bitwise_and(d1, d2)
    # 差分が閾値より小さければTrue
    mask = diff < th
    # 背景画像と同じサイズの配列生成
    im_mask = np.empty((im1.shape[0],im1.shape[1]),np.uint8)
    im_mask[:][:]=255
    # Trueの部分（背景）は黒塗り
    im_mask[mask]=0
    # ゴマ塩ノイズ除去
    im_mask = cv2.medianBlur(im_mask,blur)

    return  im_mask



# 動体を検出
def motion_detect(im_bg,im_in,th,blur):

    # 差分計算
    diff = cv2.absdiff(im_in,im_bg)
    # 差分が閾値より小さければTrue
    mask = diff < th
    # 背景画像と同じサイズの配列生成
    im_mask = np.zeros((im_bg.shape[0],im_bg.shape[1]),np.uint8)
    # Trueの部分（背景）は白塗り
    im_mask[mask]=255
    # ゴマ塩ノイズ除去
    #im_mask = cv2.medianBlur(im_mask,blur)
    # エッジ検出
    im_edge = cv2.Canny(im_mask,100,200)
    # 動体抽出
    im_mask = cv2.bitwise_not(im_mask,im_in,mask = im_mask)

    return im_mask,im_edge



if __name__ == '__main__':

    #cam = cv2.VideoCapture(0)
    cam = cv2.VideoCapture('/Users/matto/Stitch tmp2/IMG_0589_2.mp4')
    im1 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    im2 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
    im3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

    while True:
        # フレーム間差分計算
        #im_fs = flame_sub(im1,im2,im3,5,7)
        # 動体差分
        im_mo,im_edge = motion_detect(im1,im2,15,7)
        #cv2.imshow("Input",im2)
        #cv2.imshow("Motion Mask",im_fs)
        cv2.imshow("Motion Detect",im_mo)
        #im1 = im2
        im2 = im3
        im3 = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
        key = cv2.waitKey(10)
        # Escキーが押されたら
        if key == 27:
            cv2.imwrite("input.jpg",im3)
            #cv2.imwrite("frame_sub.jpg",im_fs)
            cv2.imwrite("motion_detect.jpg",im_mo)
            cv2.destroyAllWindows()
            break
