import json
from numpy.lib.arraysetops import unique
import pandas as pd
from math import isnan

class confirmed_contact_parser:

    def __init__(self):
        self.keywords = {"positive": 3, "negative": 2, "possible": 1, "other": 0}

    def check_nan(self, e):
        return isinstance(e, float) and isnan(e)

    def parse(self, sample):
        if self.check_nan(sample):
            return self.keywords["other"]
        low = sample.lower()
        nr = -1
        try:
            nr = int(low)
        except:
            pass
        if nr > 0:
            return self.keywords["positive"]
        if nr == 0:
            return self.keywords["negative"]
        if "nu" in low or "negativ" in low or "fara" in low or "-" == low:
            return self.keywords["negative"]
        if "da" in low or "pozitiv" in low or "focar" in low:
            return self.keywords["positive"]
        if "posibil" in low or "poate" in low or "suspici" in low or "neag" in low:
            return self.keywords["possible"]
        return self.keywords["other"]

    def parse_array(self, arr):
        return [self.parse(x) for x in arr]

def check_nan(e):
    return isinstance(e, float) and isnan(e)

def parse(s):
    low = s.lower()
    nr = -1
    try:
        nr = int(low)
    except:
        pass
    if nr > 0:
        return "positive"
    if nr == 0:
        return "negative"
    if "nu" in low or "negativ" in low or "fara" in low or "-" == low:
        return "negative"
    if "da" in low or "pozitiv" in low or "focar" in low:
        return "positive"
    if "posibil" in low or "poate" in low or "suspici" in low or "neag" in low:
        return "possible"
    return "other"

def main():

    excel_path = "../dataset.xlsx"
    # Read excel
    df = pd.read_excel(excel_path, dtype=str)

    # Store values in 2D array
    data = df.iloc[:].values
    arr = df.iloc[:,10].values
    filter_arr = []
    for e in arr:
        if check_nan(e):
            filter_arr.append(None)
        else:
            filter_arr.append(e)
    uniques = list(set(filter_arr))
    for x in uniques:
        if (x != None):
            print(x, "===>",parse(x))


if __name__ == "__main__":
    main()