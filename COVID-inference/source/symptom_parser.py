import os
import json
import argparse
import sklearn
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from constants import simptom_dict as dict
from constants import *
import re


def main():
    config = {}
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
    df = pd.read_excel(config[TRAIN_PATH], na_values=None)
    data = df.iloc[:].values

    list = []
    for entry in data:
        val = re.split("^\s+|\s*,\s*|\s+$", str(entry[6]))

        for i in val:

            i = i.lower()
            if i != '':
                if i[0] != ' ' and i[0] != 'n':
                    ok = 0
                    for j in list:
                        if j == i:
                            ok = 1
                    if ok == 0:
                        list.append(i)
    dict = {}
    i = 0
    nr = 0
    while i < len(list) - 1:
        new = []
        for j in list[i: len(list) - 1]:
            k = 0
            value = ''
            for c in j:
                if k < len(list[i]) and c == list[i][k]:
                    k += 1
                elif k > 4:
                    value = j
                    break
                else:
                     k = 0
            if value != '':
                new.append(j)
                list.remove(j)
        if len(new) > 1:
            new.append(list[i])
            dict[list[i]] = new
            nr += 1
            list.remove(list[i])
        i += 1
    print(parse_symptoms("DURERI HIPOCONDRUL DREPT, GREATA, SUBFEBRILITATI"))
    pass
# functia search primeste urmatorii parametrii
# index reprezinta indexul de unde va incepe cautarea in symptoms
# functia returneaza un tuplu
# prima valaore este indexul din symptoms unde a ramas cautarea
#                             (e utilizat in principiu ca in cazul in acre simptom e din doua cuvinte
#                                       sa pot sa-l gasesc pe al doilea)
# al doiela este true sau false , in functie daca este gasit simptomul respectiv sau nu
# ultimul este numarul de caractere comune cu elementul comun din symptoms
def search(index, symptoms, simptom):

    j = 0
    miss = 0
    i = index
    if i >= len(symptoms) - 1:
        return (0, False)

    #exista un caz separat pentru temperatura pentru o parsare separata
    if simptom[0] == '<':
        if symptoms[i] in '1234567890':
            nr = 0
            while i < len(symptoms) and symptoms[i] in '1234567890':
                nr = nr*10 + ord(symptoms[i]) - ord('0')
                i += 1
            return (i, True, nr);
        else:
            return (0, False)
    # se itereaza prin tot string-ul symptoms pentru a gasi cuvantul salvat in simptom
    while i < len(symptoms):
        if symptoms[i] == simptom[j] and j < len(simptom) - 1:
            j += 1
        #urmatoarele doua conditii sunt pentru oprire
        #condtia  de len > 4 este folosite in aczul simptomelor cu putine caractere
        elif j > len(simptom) - 2 and len(simptom) > 4:
            while i < len(symptoms) and symptoms[i] != ' ' and symptoms[i] != ',':
                i += 1
            while i < len(symptoms) and (symptoms[i] == ' ' or symptoms[i] == ','):
                i += 1
            return (i, True, j)
        #simptomele cu putine caractere sunt tratate pe aceasta conditie
        elif j == len(simptom) - 1 and miss == 0:
            while i < len(symptoms) and symptoms[i] != ' ' and symptoms[i] != ',':
                i += 1
            while i < len(symptoms) and (symptoms[i] == ' ' or symptoms[i] == ','):
                i += 1
            return (i, True, j)
        #in cazul in care un caracter este gresit din dataset il tratam ca o litera lipsa
        elif j > 1 and miss == 0:
            miss = 1
            j += 1
            i -= 1
        else:
            j = 0
        i += 1

    return (0, False)
#returneaza un tuplu
# 1 prima valaore fiin true sau false inc azul in care simptom se gaseste in symptoms
# 2 se foloseste doar in cazul temperaturii
def search_value(symptoms, simptom):

    res = []
    temp = 0
    symptoms = symptoms.lower()
    if (" " in simptom):
        res = re.split("\s+", simptom)
    if len(res) == 0:
        x = search(0,symptoms, simptom)
        return (x[1], temp)
    #in cazul in care simptomul este format din mai multe cuvinte
    # se cauta fiecare cuvant in parte in symptoms
    else:
        index = 0
        list = []
        nr = 0
        score = 0
        length = 0
        for i in res:
            #functia search cauta cuvantul i in symptoms de la index
            val = search(index, symptoms, i)
            list.append(val)
            length += len(i) - 1
            #conditie separata pentru temperatura
            if i[0] == '<':
                score += len(i)
                if val[1]:
                    temp = val[2]
                else:
                    temp = 38
            elif val[1]:
                index = val[0]
                nr += 1
                score += val[2]
        #daca nuamrul de caractere gasite e mai mult decat media caracterelor
        # cautate am considreat ca e gasit
        if (score > length/(len(res))):
            return (True, temp)

    return (False, temp)


def parse_symptoms(symptoms):


    # reconstructing the data as a dictionary
    list = [0] * (len(dict) - 1)
    list[22] = 36.5
    for key in dict:
        val = search_value(symptoms, key)
        if val[0]:
            if val[1] > 0:
                list[dict[key]] = val[1]
            else:
                list[dict[key]] = 1
    return list



if __name__ == "__main__":
    main()