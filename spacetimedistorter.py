#!/usr/local/bin/python2.7
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import sys



class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)

import sys
sys.stdout = Unbuffered(sys.stdout)


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
   maxwidth = 720 #because the process is very slow
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
   ratio = 1.0
   if width > maxwidth:
      ratio = float(maxwidth) / width
      width = maxwidth
      height = int(height*ratio)
   image = np.zeros((width,height,3), dtype=np.uint8)
   capSize = (width,height) # this is the size of my source video
   fourcc = cv2.VideoWriter_fourcc('A','V','C','1')
   #fourcc = cv2.VideoWriter_fourcc('m','p','4','v') # note the lower case
   #fourcc = cv2.VideoWriter_fourcc('m','j','p','g') # note the lower case
   vout = cv2.VideoWriter()
   fps=30
   success = vout.open('motion720p.mov',fourcc,fps,capSize,True)
   print (success)
   nframe = 0
   wend = (height,width,height,width,height)
   cache = [np.zeros((width,height,3), dtype=np.uint8) for i in range(wend[dir]//w)]
   while True:
      ret, frame = cap.read()
      frame = cv2.resize(frame,None,fx=ratio,fy=ratio)
      cache.append(frame)
      #print nframe
      if not ret:
         print ("No frame.")
         break
      if dir == 0:
         #from left to right
         for i in range(0,wend[dir],w):
            image[:,i:i+w,:] = cache[i//w][:,i:i+w,:]
      elif dir == 1:
         #from top to bottom
         for i in range(0,wend[dir],w):
            image[i:i+w,:,:] = cache[i//w][i:i+w,:,:]
      elif dir == 2:
         #from left to right
         for i in range(0,wend[dir],w):
            image[:,i:i+w,:] = cache[(wend[dir]-i)//w][:,i:i+w,:]
      elif dir == 3:
         #from left to right
         for i in range(0,wend[dir],w):
            image[i:i+w,:,:] = cache[(wend[dir]-i)//w][i:i+w,:,:]
      elif dir == 4: #v-shape
         for i in range(0,wend[dir]//2,w):
            image[:,i:i+w,:] = cache[i/w][:,i:i+w,:]
         for i in range(wend[dir]//2,wend[dir],w):
            image[:,i:i+w,:] = cache[(wend[dir]-i)//w][:,i:i+w,:]
      cv2.imshow("Image",image)
      vout.write(image)
      #cv2.imwrite("distorter_/%05d.jpg" % nframe,image)
      nframe += 1
      cache.pop(0)
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
   #vout.ReleaseVideoWriter()
   cv2.destroyAllWindows()
