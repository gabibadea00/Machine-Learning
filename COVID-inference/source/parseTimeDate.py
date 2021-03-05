import datetime
import re
import datefinder
import os
import json
import argparse
import numpy as np
import pandas as pd
from constants import *
from dateutil.parser import parse
from pandas.io.parsers import ParserError
from dateparser.search import search_dates


test = [
    '2020-06-29 08:15:27.243860',
    'Jun 28 2020 7:40AM',
    'Jun 28 2020 at 7:40AM',
    'September 18, 2020, 22:19:55',
    'Sun, 05/12/2020, 12:30PM',
    'Mon, 21 March, 2010',
    '2020-03-12T10:12:45Z',
    '2020-06-29 17:08:00.586525+00:00',
    '2020-06-29 17:08:00.586525+05:00',
    'Tuesday , 6th September, 2020 at 4:30pm',
    '2020-04-28 00:00:00',
    '20.04.2020',
    'Medicina Interna 2',
    'NU',
    '21 04 2020',
    '29,04,2020',
    '43936',
    '08,05,2020',
    'BI Cicio Pop',
    '29,04.2020',
    '29.04,2020',
    '29,04. 2020',
    '4/9/2020  12:00:00 AM',
    '31..03.2020',
    'BIA / ATI II',
    '',
    'NEURO/ATIII',
    '10.02.020',
    '10.02 2022',
    '19.05,2020',
    '20.04.2020   2',
    '4/28/2020  12:00:00 AM',
    'internare',
    '16.04.2020.',
    '01.04.20 IN PEDI 1 TRASF BI COPII IN 05.04.2020'
]


def diff_dates(date2):
    date1 = datetime.datetime(2020, 1, 1).date()
    return (date2-date1).days


def hasNumbers(inputString):
    contor = 0
    for char in inputString:
        if char.isdigit():
            contor = contor + 1
    if contor >= 4:
        return True
    else:
        return False


def findDate(input_string):
    matches = list(datefinder.find_dates(input_string))
    if len(matches) > 0:
        return matches[len(matches)-1]
    else:
        return None


def parseTime(date, display=False):
    new_date = str(date).replace(',', '.')
    if display:
        print('Parsing: ', new_date)
    if hasNumbers(new_date):
        try:
            dt = parse(str(new_date))
            if display:
                print(dt.date())
                print('INT = ', diff_dates(dt.date()))
            return diff_dates(dt.date())
        except:
            if display:
                print("Nu e format valid de data")
                print('INT = ', None)
            return None
    else:
        if display:
            print('INT = ', None)
        return None


def main():
    config = {}
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        df = pd.read_excel(config[TRAIN_PATH], na_values=None)
        # Store values in 2D array
        data = df.iloc[:].values
        dates = []
        for entry in data:
            try:
                coloane_date = entry[3]
                new_coloane_date = str(coloane_date).replace("nan", "nu")
                dates.append(new_coloane_date)
                print("S = ", new_coloane_date)
            except AttributeError as e:
                print(e)

    index = 2
    for date in dates:
        print("------\n")
        print("INDEX = ", index)
        print("Key: ", date)
        print("Value: ", parseTime(date, display=True))
        parseTime(date, display=True)
        print("------\n")
        index = index + 1

if __name__ == "__main__":
    main()
