#!/usr/bin/pythonuu
# -*- coding:utf-8 -*-

debug = False

import time
from PIL import Image,ImageDraw,ImageFont
import datetime

import requests

from my_functions import draw_image

if not debug:
    import epd7in5
    import schedule

# Define times when not to update the screen
r1_start = datetime.time(23, 30, 0)
r1_end = datetime.time(4, 30, 0)

r2_start = datetime.time(10, 30, 0)
r2_end = datetime.time(11, 0, 0)


def main():

    Himage = draw_image()
    Himage.save('debug.bmp')
    print('image produced')
    
# ---------------------- LIVE CODE ------------------
    if not debug:
        now = datetime.datetime.now().time()
        if now >= r1_start or now <= r1_end or (now >=r2_start and now <= r2_end):
            print("sleeping until Ryan is around")
            return

        epd = epd7in5.EPD()
        epd.init()
        # print("Clear")
        # epd.Clear(0xFF)

        epd.display(epd.getbuffer(Himage))
        time.sleep(2)

        # bmp = Image.open('100x100.bmp')
        # Himage2.paste(bmp, (50,10))
        # epd.display(epd.getbuffer(Himage2))
        # time.sleep(2)

        epd.sleep()
# ---------------------- END LIVE CODE -----------------

# def get_headline():

#     url = ('https://newsapi.org/v2/top-headlines?'
#            'sources=google-news&'
#            'apiKey=649f16b64f4f421784dc77cda071b64d')
#     response = requests.get(url)
#     rand_index = randint(0,len(response.json()['articles'])-1)
#     return response.json()['articles'][rand_index]['title']


if not debug:
    schedule.every(2).minutes.do(main)

if __name__ == '__main__':
    if not debug:
        main()
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        main()
