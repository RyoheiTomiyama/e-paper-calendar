#!/usr/bin/python
# -*- coding:utf-8 -*-

# import sys
# import os
# picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
# libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
# if os.path.exists(libdir):
#     sys.path.append(libdir)

# import logging
# import time
import logging
from PIL import Image
from waveshare.epd7in5b_V2 import EPD, epdconfig

logging.basicConfig(level=logging.DEBUG)

def output_epaper(image_black: Image.Image, image_red: Image.Image):
  try:

      epd = EPD()
      epd.init()
      epd.Clear()

      epd.display(epd.getbuffer(image_black),epd.getbuffer(image_red))

      epd.sleep()

      # font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
      # font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

      # # Drawing on the Horizontal image
      # logging.info("1.Drawing on the Horizontal image...")
      # Himage = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
      # Other = Image.new('1', (epd.width, epd.height), 255)  # 255: clear the frame
      # draw_Himage = ImageDraw.Draw(Himage)
      # draw_other = ImageDraw.Draw(Other)
      # draw_Himage.text((10, 0), 'hello world', font = font24, fill = 0)
      # draw_Himage.text((10, 20), '7.5inch e-Paper', font = font24, fill = 0)
      # draw_Himage.text((150, 0), u'微雪电子', font = font24, fill = 0)    
      # draw_other.line((20, 50, 70, 100), fill = 0)
      # draw_other.line((70, 50, 20, 100), fill = 0)
      # draw_other.rectangle((20, 50, 70, 100), outline = 0)
      # draw_other.line((165, 50, 165, 100), fill = 0)
      # draw_Himage.line((140, 75, 190, 75), fill = 0)
      # draw_Himage.arc((140, 50, 190, 100), 0, 360, fill = 0)
      # draw_Himage.rectangle((80, 50, 130, 100), fill = 0)
      # draw_Himage.chord((200, 50, 250, 100), 0, 360, fill = 0)
      # epd.display(epd.getbuffer(Himage),epd.getbuffer(Other))

      # # clear
      # epd.init()
      # epd.Clear()

      # epd.sleep()
      
  except IOError as e:
      print(e)
      
  except KeyboardInterrupt:    
      epdconfig.module_exit()
      exit()