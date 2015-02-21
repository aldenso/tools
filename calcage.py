#!/usr/bin/env python2
#
# File: calcage.py
# Author: aldenso@gmail.com
# Description: This script is used to find an age in days and years, from a date

import datetime

def deltayears(deltadays):
    years = (deltadays/365)
    return years

def main():
    answer = 0
    try:
        answer = raw_input("Please enter a date in format: dd/mm/yyyy\n")
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
