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

#VideoWriter in CV2 does not work at all.
#I gave up using it.
#http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
def videowriter(filename, fps=24, size=(640,480)):
   from subprocess import Popen, PIPE
   command = [ "/usr/local/bin/ffmpeg",
               '-y', # (optional) overwrite output file if it exists
               '-f', 'rawvideo',
               '-vcodec','rawvideo',
               '-s', '{}x{}'.format(size[0],size[1]), # size of one frame
               '-pix_fmt', 'rgb24',
               '-r','{}'.format(int(fps)), # frames per second
               '-i', '-', # The imput comes from a pipe
               '-an', # Tells FFMPEG not to expect any audio
               #'-vcodec', vcodec,
               "-pix_fmt","yuv420p",
               filename ]
   print command
   pipe = Popen( command, stdin=PIPE, stderr=PIPE) # to suppress messages from ffmpeg
   return pipe

def vwrite(pipe, image):
   tmp = image[:,:,[2,1,0]].copy(order='C')
   pipe.stdin.write( tmp )



if __name__ == '__main__':
   cap = cv2.VideoCapture(0)
   ret, frame = cap.read()
   width, height = frame.shape[:2]
   image = np.zeros((width,height,3), dtype=np.uint8)
   capSize = (width,height) # this is the size of my source video
   #fourcc = cv2.VideoWriter_fourcc(*'iYUV')
   fourcc = cv2.VideoWriter_fourcc(*'mp4v')
   #fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
   fps = 15.0
   #vout = cv2.VideoWriter('output.avi',fourcc, fps, capSize)
   #vout = cv2.VideoWriter('output.avi', 0, fps, capSize)
   vout = videowriter('output.mp4', fps, (capSize[1],capSize[0]))
   if not vout:
      print "!!! Failed VideoWriter: invalid parameters"
      sys.exit(1)   
   for i in range(10): #10 frames
      ret, frame = cap.read()
      print type(frame)
      cv2.imshow("",frame)
      vwrite(vout,frame)
   cap.release()
   #vout.release()
   #vout.ReleaseVideoWriter()
