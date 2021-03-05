from typing import Type
import numpy as np
import pandas as pd
import json
import pickle
from math import isnan, nan 
from constants import *
from confirmed_contact_parser import confirmed_contact_parser, check_nan
from label_parser import institution_parser, sex_parser, age_parser, result_parser
from symptom_parser import *
from parseTimeDate import parseTime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, roc_curve, roc_auc_score, plot_confusion_matrix

class covid_detector:

    def __init__(self, config):
        with open(config, "r") as config_file:
            self.config = json.load(config_file)
        self.contact_parser = confirmed_contact_parser()
        if self.config[MODE] == TRAIN:
            self.train()
        elif self.config[MODE] == PREDICT:
            self.model = pickle.load(open(MODEL_NAME + ".pkl", "rb"))

    def check_nan(self, e):
        return isinstance(e, float) and isnan(e)

    # Takes one sample in the dataset and performs FX
    def extract_features(self, sample):
        try:
            # Parse the source institution
            if sample[0] == None or sample[1] == None or sample[2] == None:
                return None
            inst = institution_parser(sample[0])

            # Parse the person's sex
            s = sex_parser(sample[1])

            # Parse the age
            age = age_parser(str(sample[2]), self.config[MEAN_AGE])

            # Parse declared symptoms
            decl_sympt = []
            if sample[4] != None:
                decl_sympt = parse_symptoms(str(sample[4]))
            else:
                decl_sympt = parse_symptoms(str(nan))

            # Parse the symptoms the pacient had when being admitted in the hospital
            actual_symptoms = []
            if sample[6] != None:
                actual_symptoms = parse_symptoms(str(sample[6]))
            else:
                actual_symptoms = parse_symptoms(str(nan))

            # Parse the patient's contact history
            had_contact_with_infected_person = self.contact_parser.parse(str(sample[10]))

            # Parse the test results' date
            results_date = parseTime(sample[11])
            if results_date == None:
                return None

            result = []
            result.append(inst)
            result.append(s)
            result.append(age)
            result.append(had_contact_with_infected_person)
            result.append(results_date)
            for i in range(len(decl_sympt)):
                result.append(decl_sympt[i])
            for i in range(len(actual_symptoms)):
                result.append(actual_symptoms[i])

            return result
        except TypeError as e:
            return None

    # istoric de calatorie, mijloace de transport

    def train(self):
        # Read excel
        if self.config[VERBOSE] == True:
            print("=== Reading data ===", flush=True)
        df = pd.read_excel(self.config[TRAIN_PATH], na_values=None)

        # Store data in labels in separate arrays
        data = df.iloc[:, :12].values
        labels = df.iloc[:, 12].values
        
        if self.config[VERBOSE] == True:
            print("=== Preprocessing data ===", flush=True)
        # Ignore mislabeled data
        X_aux = []
        y_aux = []
        n = len(data)
        for i in range(n):
            if self.check_nan(labels[i]) == False:
                if result_parser(labels[i]) != 2:
                    X_aux.append(data[i])
                    y_aux.append(result_parser(labels[i]))
        
        X = []
        y = []
        n = len(X_aux)
        # Calculate mean_age
        self.mean_age = 0
        for i in range(n):
            if self.check_nan(X_aux[i][2]) == False:
                self.mean_age += int(age_parser(str(X_aux[i][2])))
        self.mean_age = round(self.mean_age / n)
        for i in range(n):
            if self.check_nan(X_aux[i][2]):
                X_aux[i][2] = self.mean_age

        # Extract features
        if self.config[VERBOSE] == True:
            print("=== Extracting features ===", flush=True)
        for i in range(n):
            feat = self.extract_features(X_aux[i])
            if feat == None:
                continue
            X.append(feat)
            y.append(y_aux[i])

        X = np.array(X)
        y = np.array(y)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

        if self.config[VERBOSE] == True:
            print("=== Training model ===", flush=True)
        self.model = RandomForestClassifier(n_estimators = 50, n_jobs = -1, criterion = "gini", max_depth = 6, random_state = 42, verbose = 0)
        self.model.fit(X_train, y_train)

        if self.config[VERBOSE] == True:
            print("=== Saving metrics ===", flush=True)
        with open("metrics.txt", "w") as metric_file:
            y_pred = self.model.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            metric_file.write("Accuracy:" + str(round(acc * 100, 2)) +"%\n")
            tn, fp, fn, tp = confusion_matrix(y_test, y_pred).ravel()
            metric_file.write("Precision:" + str(tp/(tp+fp)) + "\n")
            metric_file.write("Recall:" + str(tp/(tp+fn)) + "\n")
            metric_file.write("True positives:" + str(tp) + "\n")
            metric_file.write("False positives:" + str(fp) + "\n")
            metric_file.write("True negatives:" + str(tn) + "\n")
            metric_file.write("False negatives:" + str(fn) + "\n")
            y_proba = self.model.predict_proba(X_test)[::,1]
            fpr, tpr, thresholds = roc_curve(y_test, y_proba)
            auc = roc_auc_score(y_test, y_proba)
            metric_file.write('AUC: %.3f' % auc)
            plt.plot(fpr,tpr,label="AUC="+str(round(auc,3)))
            plt.title("AUC Curve")
            plt.legend(loc=4)
            plt.savefig("auc_curve.png", dpi=300, bbox_inches='tight')
            plot_confusion_matrix(self.model, X_test, y_test)
            plt.title("Confusion matrix")
            plt.savefig("confusion_matrix.png", dpi=300, bbox_inches='tight')
        
        pickle.dump(self.model, open(MODEL_NAME + ".pkl", 'wb'))
        if self.config[VERBOSE] == True:
            print("=== DONE ===", flush=True)

    def format_entry(self, entry):
        res = []
        res.append(entry["instituția sursă"])
        res.append(entry["sex"])
        res.append(entry["vârstă"])
        res.append(entry["dată debut simptome declarate"])
        res.append(entry["simptome declarate"])
        res.append(entry["dată internare"])
        res.append(entry["simptome raportate la internare"])
        res.append(entry["diagnostic și semne de internare"])
        res.append(entry["istoric de călătorie"])
        res.append(entry["mijloace de transport folosite"])
        res.append(entry["confirmare contact cu o persoană infectată"])
        res.append(entry["data rezultat testare"])
        return res

    # Function to be used for predicting on data through the API
    def predict(self, data):
        processed_data = data
        X = []
        n = len(data)
        for i in range(n):
            feat = self.extract_features(self.format_entry(processed_data[i]))
            if feat != None:
                processed_data[i]["predictie"] = "date suficiente"
                X.append(feat)
            else:
                processed_data[i]["predictie"] = "date insuficiente"
        X = np.array(X)
        y = self.model.predict_proba(X)[::, 1]
        counter = 0
        for i in range(n):
            if processed_data[i]["predictie"] == "date suficiente":
                processed_data[i]["predictie"] = round(y[counter] * 100, 2)
                counter += 1
        return processed_data

if __name__ == "__main__":

    detector = covid_detector("config.json")