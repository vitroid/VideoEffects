#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 動くものにあふれるカメラ。

import numpy as np
import cv2
import sys

file = 0
if len(sys.argv) > 1:
    file = sys.argv[1]

cap = cv2.VideoCapture(file)
# cap = cv2.VideoCapture('vtest.avi')

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows=False)

ret, first = cap.read()

while 1:
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)
    fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    ksam = 255 - fgmask
    stable = cv2.bitwise_and(first, first, mask=ksam)
    mobile = cv2.bitwise_and(frame, frame, mask=fgmask)

    first = cv2.add(stable, mobile)
    cv2.imshow("frame", first)
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
