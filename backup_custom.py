#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd7in5
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import datetime
import schedule

from bs4 import BeautifulSoup
import requests
import textwrap

from random import randint

debug = False
headline = ""

# Define times when not to update the screen
r1_start = datetime.time(23, 30, 0)
r1_end = datetime.time(4, 30, 0)

r2_start = datetime.time(10, 30, 0)
r2_end = datetime.time(11, 0, 0)
    

def main():
    
    now = datetime.datetime.now().time()
    if now >= r1_start or now <= r1_end or (now >=r2_start and now <= r2_end):
        print("sleeping until Ryan is around")
        return

    global headline
    x_offset = 20

    # Generate image
    print("Getting data")
    # text = get_headline()
    data = get_weather()
    temp_num = data['temp']
    windspeed_num = data['wind']
    sum_hour = data['hour_summary']
    sum_day = data['day_summary']
    temp = "{}F|{}MPH".format(temp_num, int(round(windspeed_num)))
    # headline = text
    print("Drawing")
    date_str = datetime.datetime.now().strftime("%m/%d/%Y")
    time_str = datetime.datetime.now().strftime("%H:%M:%S")
    # Drawing on the Horizontal image
    Himage = Image.new('1', (epd7in5.EPD_WIDTH, epd7in5.EPD_HEIGHT), 255)  # 255: clear the frame

    draw = ImageDraw.Draw(Himage)
    font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold', 32)
    font_medium = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold', 60)
    font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold', 88)
    draw.text((10, 10), date_str, font = font_large, fill = 0)

    date_width, date_height = font_large.getsize(date_str)
    y_text = 10 + date_height + 5

    draw.text((x_offset, y_text), temp, font = font_medium, fill = 0)

    temp_width, temp_height = font_medium.getsize(temp)
    y_text += temp_height + 5
    
    # lines = textwrap.wrap(headline, width=33)
    lines = textwrap.wrap(sum_hour, width=32)
    for line in lines:
        width, height = font_small.getsize(line)
        draw.text((x_offset, y_text), line, font = font_small, fill=0)
        y_text += height

    y_text += 5
    
    lines = textwrap.wrap(sum_day, width=32)
    for line in lines:
        width, height = font_small.getsize(line)
        draw.text((x_offset, y_text), line, font = font_small, fill=0)
        y_text += height
                          
    width, height = font_medium.getsize(time_str)
    width_panel, height_panel = Himage.size
    if height <= height_panel - y_text - 10:
        draw.text((x_offset, y_text+10),
                  "Updated {}".format(time_str),
                  font = font_small,
                  fill = 0)
  
    # draw.line((20, 50, 70, 100), fill = 0)
    # draw.line((70, 50, 20, 100), fill = 0)
    # draw.rectangle((20, 50, 70, 100), outline = 0)
    # draw.line((165, 50, 165, 100), fill = 0)
    # draw.line((140, 75, 190, 75), fill = 0)
    # draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
    # draw.rectangle((80, 50, 130, 100), fill = 0)
    # draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
    Himage.save('debug.bmp')

    if not debug:
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


def get_headline():

    url = ('https://newsapi.org/v2/top-headlines?'
           'sources=google-news&'
           'apiKey=649f16b64f4f421784dc77cda071b64d')
    response = requests.get(url)
    rand_index = randint(0,len(response.json()['articles'])-1)
    return response.json()['articles'][rand_index]['title']


def get_weather():
    lat = 40.664501
    lon = -73.977212

    url = ('https://api.darksky.net/forecast/459a764488e7dfb2bcb73fb429ac833b/{},{}'.format(lat,lon))
    
    response = requests.get(url)
    return {'temp': response.json()['currently']['temperature'],
            'wind': response.json()['currently']['windSpeed'],
            'hour_summary': response.json()['hourly']['summary'],
            'day_summary': response.json()['daily']['summary']}

schedule.every(60).minutes.do(main)

if __name__ == '__main__':
    if not debug:
        main()
        while True:
            schedule.run_pending()
            time.sleep(1)
    else:
        main()
