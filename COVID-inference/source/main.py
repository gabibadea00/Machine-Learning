import os
import json
import argparse
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constants import *
from covid_detector import covid_detector

def main():
    config = {}
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    detector = covid_detector(config)
    detector.train()
    
if __name__ == "__main__":
    main()