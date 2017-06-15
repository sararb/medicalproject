#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter.filedialog import *
from tkinter.messagebox import showerror
import pickle
import pandas as pd
import MySQLdb
import os
import glob
from sqlalchemy import create_engine

from medicalproject.Project.Interface.preprocessing.processing_nltk import data_preprocessing


# Windows which allows the user to train new models, store models
class Page2(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Retour au menu principal", command=lambda: controller.show_frame(Menu))
        button1.pack(side="bottom")

        button2 = tk.Button(self, text="Importer des fichiers patients", command=self.learning_randomForest, )
        button2.pack(side="top")

    def learning_randomForest(self):
        engine = create_engine('mysql+mysqldb://root:Kaoutar08Ftouhi@localhost/medical_database?charset=utf8',
                               encoding='latin3')
        data = pd.read_sql('SELECT * from patient_database', engine)
        print(data)
        print(data.__class__)
        data = data_preprocessing.load_data_text(df=data, clean_string=True, nltk_clean=True, stemm=True)
        print(data)
