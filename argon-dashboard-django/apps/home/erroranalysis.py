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
from raiwidgets import ErrorAnalysisDashboard
import pickle
import socket

def createDashboard(request):
    df=pd.read_csv('./users/'+request.user.username+'/'+request.POST['fileName'],skipinitialspace=True) #Turns all blank cells into NaN
    model = pickle.load(open('./users/'+request.user.username+'/'+request.POST['modelName'], 'rb'))
    training_features = model.feature_names_in_
    column_names = set(df.columns)
    testing_feature = list(column_names-set(training_features))
    y_test = df[testing_feature]
    X_test = df.drop(testing_feature, axis=1)
    y_pred = model.predict(X_test)
    # find a free port
    sock = socket.socket()
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    ErrorAnalysisDashboard(dataset=X_test, true_y=np.ravel(y_test), port=5008, features=training_features, pred_y=y_pred)
    return port