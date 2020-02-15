#!/bin/bash
#title           : Epaper Cron Job
#description     : runs RunOnce.py for epaper screen
#author          : Ryan Cummings
#date            : 2020_02_15

python3 ~/epaper_frame/RunOnce.py
echo $(date -u) "Ran Cron job" >> log.txt
