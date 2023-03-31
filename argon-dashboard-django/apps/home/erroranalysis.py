from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import pandas as pd
import numpy as np
import json as json
import raiwidgets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from raiwidgets import ErrorAnalysisDashboard
import pickle

def createDashboard():
    clf = pickle.load(open('./users/antran416/model.pkl', 'rb'))
    df = pd.read_csv('./users/antran416/admission_prediction.csv')
    target = ['admit']
    y = df[target]
    X = df.drop(target, axis = 1)
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.8, random_state = 0)
    feature_names = clf.feature_names_in_
    y_pred = clf.predict(X_test)
    return ErrorAnalysisDashboard(dataset=X_test, true_y=np.ravel(y_test), features=feature_names, pred_y=y_pred)

createDashboard()