# -*- coding: utf-8 -*-
"""
@Time        : 2020/7/19 12:17
@Author      : NingWang
@Email       : yogehaoren@gmail.com
@File        : upload.py
@Description : 
@Version     : 0.1-dev
@Edited      : Xiaohan
"""
import sys
import getopt
import argparse
import os
import random
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

from utils import Utils

class YiQingTong:
    def __init__(self,args):
        self.username = args.username
        self.password = args.password
        self.cookie_file = args.cookie
        self.message_file = args.message_file
        self.location = args.location

    ##############################
    # Internal Methods #
    ##############################
    def _upload_use_cookie(self):
        cookie = Utils.load_cookie_from_file(self.cookie_file)
        upload_message = Utils.load_upload_message_file(self.message_file,self.location)
        Utils.upload_ncov_message(cookie, upload_message=upload_message)

    def _upload_use_pw(self):
        cookie_file = os.path.dirname(os.path.abspath(__file__)) + os.sep + "data" + os.sep + Utils.COOKIE_FILE_NAME
        print("use username and password to upload message, cookie file is save to " + cookie_file)
        Utils.get_cookie_from_login(self.username, self.password, cookie_file)
        cookie = Utils.load_cookie_from_file(cookie_file)
        upload_message = Utils.load_upload_message_file(self.message_file,self.location)
        Utils.upload_ncov_message(cookie, upload_message=upload_message)

    ##############################
    # External Methods #
    ##############################
    def upload(self):
        if self.cookie_file!=None and self.message_file!=None:
            self._upload_use_cookie()

        elif self.username!=None and self.message_file!=None and self.password!=None:
            self._upload_use_pw()

        else:
            print('Please specify username&password or cookie file')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username',
                        help='Student Account Username')

    parser.add_argument('-p', '--password',
                        help='Student Account Password')
    parser.add_argument('-l', '--location',
                        help='GPS location, s for south school, n for north school, default is s',default='s')
    parser.add_argument(
        "-c", "--cookie", help='Path to the Cookie file')
    parser.add_argument(
        "-f", "--message_file", help='Path to the Upload message file')
    parser.add_argument(
        "-n", "--now", help='Update Yiqingtong Right now',type=bool,default=False)
    args = parser.parse_args()

    upload_task = YiQingTong(args)
    if args.now:
        print("立即填报")
        upload_task.upload()
    else:
        scheduler = BlockingScheduler()
        # 晨检
        morning_hour=random.randint(6,11)
        morning_minute=random.randint(1,59)
        print("晨检将会在每天{:0>2d}:{:0>2d}填报".format(morning_hour,morning_minute))
        scheduler.add_job(upload_task.upload, 'cron', hour=morning_hour, minute=morning_minute)
        # 午检
        noon_hour=random.randint(12,18)
        noon_minute=random.randint(1,59)
        print("午检将会在每天{:0>2d}:{:0>2d}填报".format(noon_hour,noon_minute))
        scheduler.add_job(upload_task.upload, 'cron', hour=noon_hour, minute=noon_minute)
        # 晚检
        night_hour=random.randint(19,22)
        night_minute=random.randint(1,59)
        print("晚检将会在每天{:0>2d}:{:0>2d}填报".format(night_hour,night_minute))
        scheduler.add_job(upload_task.upload, 'cron', hour=night_hour, minute=night_minute)
        scheduler.start()
