#!/usr/local/bin/python2.7
# coding: UTF-8

#example taken from
#http://qiita.com/daxanya1/items/4709ad8454760e17148c

import numpy as np
import cv2

# 実装の参考　http://www.beechtreetech.com/opencv-exercises-in-python
# cv2を使うように変更

updatelock = False # トラックバー処理中のロックフラグ
windowname = 'frame' # Windowの名前
trackbarname = 'Position' # トラックバーの名前

# AVIファイルを読む
# aviは適当な長さのサンプルをインターネットから拾ってくる
# 参考:http://www.engr.colostate.edu/me/facil/dynamics/avis.htm
cap = cv2.VideoCapture('/Users/matto/Stitch tmp2/IMG_0589_2.mp4')

# トラックバーを動かしたときに呼び出されるコールバック関数の定義
def onTrackbarSlide(pos):
    updatelock = True
    cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos)
    updatelock = False

# 名前付きWindowを定義する
cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)

# AVIファイルのフレーム数を取得する
frames = int(cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT))

# フレーム数が1以上ならトラックバーにセットする
if (frames > 0):
    cv2.createTrackbar(trackbarname, windowname, 0, frames, onTrackbarSlide)

# AVIファイルを開いている間は繰り返し（最後のフレームまで読んだら終わる）
while(cap.isOpened()):

    # トラックバー更新中は描画しない
    if (updatelock):
        continue

    # １フレーム読む
    ret, frame = cap.read()

    # 読めなかったら抜ける
    if ret == False:
        break

    # 画面に表示
    cv2.imshow(windowname,frame)

    # 現在のフレーム番号を取得
    curpos = int(cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES))

    # トラックバーにセットする（コールバック関数が呼ばれる）
    cv2.setTrackbarPos(trackbarname, windowname, curpos)

    # qを押したら抜ける
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# AVIファイルを解放
cap.release()

# Windowを閉じる
cv2.destroyAllWindows()
