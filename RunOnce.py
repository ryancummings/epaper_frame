#!/usr/bin/pythonuu
# -*- coding:utf-8 -*-

debug = False

import time
from PIL import Image,ImageDraw,ImageFont
import datetime

# import requests

from my_functions import draw_image

if not debug:
    import epd7in5

def main():

    try:
        Himage = draw_image()
        Himage.save('debug.bmp')
        print('image produced')


        if not debug:
            epd = epd7in5.EPD()
            epd.init()

            epd.display(epd.getbuffer(Himage))
            time.sleep(2)

            epd.sleep()
    except:
        return
# ---------------------- END LIVE CODE -----------------

# def get_headline():

#     url = ('https://newsapi.org/v2/top-headlines?'
#            'sources=google-news&'
#            'apiKey=649f16b64f4f421784dc77cda071b64d')
#     response = requests.get(url)
#     rand_index = randint(0,len(response.json()['articles'])-1)
#     return response.json()['articles'][rand_index]['title']

if __name__ == '__main__':
    main()
