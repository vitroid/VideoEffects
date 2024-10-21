#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-
# フレームから移動平均をさしひいて、コントラストを強調する

import cv2
import numpy as np
import sys
import os


filepath = sys.argv[1]
basename_without_ext = os.path.splitext(os.path.basename(filepath))[0]
outfile = basename_without_ext + ".avi"

cap = cv2.VideoCapture(filepath)

frames = []
while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = frame[:, :, 1].astype(float)
    frames.append(frame)


fourcc = cv2.VideoWriter_fourcc(*"XVID")
vout = cv2.VideoWriter(outfile, fourcc, 30.0, frames[0].shape[::-1], isColor=False)

# newf = []
for i in range(len(frames) - 10):
    f = frames[i] - np.mean(np.array(frames[i : i + 10]), axis=0)
    f += 20
    f *= 5
    f[f > 255] = 255
    f[f < 0] = 0
    f = f.astype(np.uint8)
    vout.write(f)
    # newf.append(f)
    # print(np.min(frames[i]), np.max(frames[i]))
    cv2.imshow(basename_without_ext, f)
    key = cv2.waitKey(10)
    # 空白キー以外のキーが押されたら終了
    if key > 0:
        # cv2.imwrite("Input.jpg",frame)
        # cv2.imwrite("Motion_mask.jpg",fgmask)
        break

cap.release()
vout.release()
# vout = None
cv2.destroyAllWindows()
