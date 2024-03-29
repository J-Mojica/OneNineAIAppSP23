import os
import warnings
import sys
import google
import pickle
import pandas as pd
import numpy as np
import random
from django.db import models
from django.contrib.auth.models import User
from django.views import View
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNet
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import mlflow
import mlflow.sklearn
import logging
import subprocess
import webbrowser

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger(__name__)

tags = {"team": "OneNiAI", 
            "dataset": "Iris",
            "release.version": "0.0.1"}

mlflow.set_tracking_uri('http://localhost:5000')
mlflow.sklearn.autolog()

iris = datasets.load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

def model_Monitor(request):
        mlflow_server_cmd = "mlflow ui"
        subprocess.Popen(mlflow_server_cmd, shell=True)
        if request.POST['method'] == 'linearRegression':
                exp_id = mlflow.set_experiment(experiment_name="Linear_regression")
                with mlflow.start_run(run_name="exp_linearRegrssion_"+str(random.randint(1,100))):
                        mlflow.set_tags(tags)
                        # Execute ElasticNet
                        lr = ElasticNet(alpha=0.2, l1_ratio=0.2, random_state=42)
                        lr.fit(X_train, y_train)
                        predicted_qualities = lr.predict(X_test)
                        score = lr.score(X_test, y_test)
                        mlflow.log_metric("accuracy", score)
                        mlflow.sklearn.log_model(lr, "linear-regression-model")
                

        if request.POST['method'] == 'logisticRegression':
                mlflow.set_experiment(experiment_name="Logistic_regression")
                with mlflow.start_run(run_name="exp_logisticRegression_"+str(random.randint(101,200))):
                        lgr = LogisticRegression()
                        lgr.fit(X_train, y_train)
                        score = lgr.score(X_test, y_test)
                        mlflow.log_metric("accuracy", score)
                        mlflow.log_param("penalty", lgr.penalty)
                        mlflow.log_param("C", lgr.C)
                        mlflow.sklearn.log_model(lgr, "logistic-regression-model")
                

        if request.POST['method'] == 'decisionTrees':
                mlflow.set_experiment(experiment_name="Decision_trees")
                with mlflow.start_run(run_name="exp_decisionTrees_"+str(random.randint(201,300))):
                        mlflow.set_tags(tags)
                        dt_clf = DecisionTreeClassifier()
                        dt_clf.fit(X_train, y_train)
                        score = dt_clf.score(X_test, y_test)
                        mlflow.log_metric("accuracy", score)
                        mlflow.log_param("criterion", dt_clf.criterion)
                        mlflow.log_param("max_depth", dt_clf.max_depth)
                        mlflow.sklearn.log_model(dt_clf, "decision-tree-model")
                
        
        if request.POST['method'] == 'randomForest':
                mlflow.set_experiment(experiment_name="Random_Forest")
                with mlflow.start_run(run_name="exp_randomForest_"+str(random.randint(301,400))):
                        mlflow.set_tags(tags)
                        rf_clf = RandomForestClassifier()
                        rf_clf.fit(X_train, y_train)
                        score = rf_clf.score(X_test, y_test)
                        mlflow.log_metric("accuracy", score)
                        mlflow.log_param("n_estimators", rf_clf.n_estimators)
                        mlflow.log_param("max_depth", rf_clf.max_depth)
                        mlflow.sklearn.log_model(rf_clf, "random-forest-model")
                
        mlflow.end_run()
        return HttpResponseRedirect('http://localhost:5000/')

