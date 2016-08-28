#!/usr/bin/python
# @Author: Aldo Sotolongo
# @Date:   2016-08-28T15:37:01-04:00
# @Email:  aldenso@gmail.com
# @Last modified by:   Aldo Sotolongo
# @Last modified time: 2016-08-28T15:42:00-04:00
# File: calcage_py3.py
# Description: This script is used to find an age in days and years.

import datetime


def deltayears(deltadays):
    years = (deltadays/365)
    return years


def main():
    answer = 0
    try:
        answer = input("Please enter a date in format: dd/mm/yyyy\n")
        day, month, year = answer.split("/")
        now = datetime.datetime.now()
        date = datetime.datetime(int(year), int(month), int(day))
        deltadays = (now-date).days
        print("Delta in days is: {0}".format(deltadays))
        print("Delta in years is: {0}".format(deltayears(deltadays)))

    except Exception as e:
        print("Not valid input, Error => {0}".format(e))

if __name__ == "__main__":
    main()
