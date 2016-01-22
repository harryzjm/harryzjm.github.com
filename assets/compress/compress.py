#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import os
from PIL import Image

#https://stackoverflow.com/questions/35859140/remove-transparency-alpha-from-any-image-using-pil

def remove_transparency(path, bg_colour=(255, 255, 255)):
  im=Image.open(path)
  if im.mode in ('RGBA', 'LA') or (im.mode == 'P' and 'transparency' in im.info):
    alpha=im.convert('RGBA').split()[-1]
    bg=Image.new("RGBA", im.size, bg_colour + (255,))
    bg.paste(im, mask=alpha)
    bg.save(path)

for fpathe,dirs,fs in os.walk('./photo'):
  for f in fs:
    if f[0] != ".":
      path=os.path.join(fpathe,f)
      remove_transparency(path)
      print "compress " + f
      os.system("guetzli " + "\"" + path + "\"" + " \"" + path + "\"")
      print "end " + f