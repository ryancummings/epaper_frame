#!/usr/bin/python
# -*- coding:utf-8 -*-

from PIL import Image,ImageDraw,ImageFont
import time
import datetime
import traceback
import requests
import os

def get_data():
    
    date_str = datetime.datetime.now().strftime("%m/%d/%Y")
    time_str = datetime.datetime.now().strftime("%H:%M")

    lat = 40.664501
    lon = -73.977212
    url = ('https://api.darksky.net/forecast/459a764488e7dfb2bcb73fb429ac833b/{},{}'.format(lat,lon))
    response = requests.get(url)
    weather_data = {'temp': response.json()['currently']['temperature'],
            'wind': response.json()['currently']['windSpeed'],
            'hour_summary': response.json()['hourly']['summary'],
            'day_summary': response.json()['daily']['summary']}

    weather_data['currently'] = "{}F | {}MPH".format(weather_data['temp'], int(round(weather_data['wind'])))
    print('Weather info downloaded')
    return {'date': date_str,
            'time': time_str,
            'weather': weather_data,
            }

            
def draw_image():

    data = get_data()
    
    cwd = os.getcwd()
    font_file = cwd + '/SourceSerifPro-Bold.otf'

    EPD_WIDTH       = 640
    EPD_HEIGHT      = 384
    
    x_offset = 12
    y_margin = 10
    font_medium = ImageFont.truetype(font_file, 56)
    font_large = ImageFont.truetype(font_file, 74)

    
    Himage = Image.new('1', (EPD_WIDTH, EPD_HEIGHT), 255)  # 255: clear the frame
    draw = ImageDraw.Draw(Himage)

    # Draw the DATE and move y_text to next line
    draw.text((10, 10), data['date'], font = font_large, fill = 0)

    date_width, date_height = font_large.getsize(data['date'])
    y_text = y_margin + date_height + 5

    # Draw the TEMP and move y_text to next line
    draw.text((x_offset, y_text), data['weather']['currently'], font = font_medium, fill = 0)

    temp_width, temp_height = font_medium.getsize(data['weather']['currently'])
    y_text += temp_height + 5

    font_small_size = 60

    fits = False
    print('Scaling font ...')
    while not fits:
        text_output = []
        par_text = data['weather']['hour_summary'].split(' ') + data['weather']['day_summary'].split(' ') + ['Updated','at'] + data['time'].split(' ')
        font_small = ImageFont.truetype(font_file, font_small_size)

        while len(par_text) > 0:
            line = []
            while len(par_text) > 0 and font_small.getsize(' '.join(line + [par_text[0]]))[0] < (EPD_WIDTH - x_offset)
                line.append(par_text.pop(0))
            text_output.append(' '.join(line))
            
        y_space = EPD_HEIGHT - y_text
        for line in text_output:
            width, height = font_small.getsize(line)
            y_space -= height
        print("y space = {}".format(y_space))
        if y_space >= 0:
            fits = True
        else:
            font_small_size -= 2
                      
    for line in text_output:
        width, height = font_small.getsize(line)
        draw.text((x_offset, y_text), line, font = font_small, fill=0)
        y_text += height

    ## PRINT BICYCLE
    Bottom = date_height + temp_height + y_margin + 10
    Left = max(date_width, temp_width) + x_offset
    bike_margin = 40
    bike_width = EPD_WIDTH - Left - bike_margin
    bike_height = EPD_HEIGHT - Bottom - bike_margin

    
    
    size = [bike_width, bike_height]
    bike = Image.open('bicycle.png').convert("RGBA").resize(size,Image.ANTIALIAS).transpose(Image.FLIP_LEFT_RIGHT)
    bike_background = Image.new("RGBA", bike.size, "WHITE")
    bike_background.paste(bike, (0, 0), bike)
    Himage.paste(bike_background, (Left + int((bike_margin / 2)), int(bike_margin / 2)))

    return Himage

