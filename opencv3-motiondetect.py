#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
import cv2

if __name__ == '__main__':

    #cap = cv2.VideoCapture(0)
    cap = cv2.VideoCapture('/Users/matto/Stitch tmp2/IMG_0565_2.mp4')
    fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False)

    while True:
        ret, frame = cap.read()

        # 動体のマスク画像を取得
        fgmask = fgbg.apply(frame)

        #gray 画像の生成
        im_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # 各画像の表示
        cv2.imshow("Input",frame)
        cv2.imshow("Motion Mask",fgmask*im_gray)
        key = cv2.waitKey(10)
        # 空白キー以外のキーが押されたら終了
        if key > 0:
            cv2.imwrite("Input.jpg",frame)
            cv2.imwrite("Motion_mask.jpg",fgmask)
            break

    cap.release()
    cv2.destroyAllWindows()
