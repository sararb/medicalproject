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


# Windows which allows the user to load new data
class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Retour au menu principal", command=lambda: controller.show_frame(Menu))
        button1.pack(side="bottom")
        # Learning DATA
        button2 = tk.Button(self, text="Importer des fichiers patients (apprentissage)", command=self.import_learning_data, )
        button2.pack(side="top")

        button3 = tk.Button(self, text="Importer un fichier patient (apprentissage)", command=self.import_unique_learning_data, )
        button3.pack(side="top")

        button4 = tk.Button(self, text="Afficher les données d'apprentissage", command=self.see_learning_table, )
        button4.pack(side="top")

        button5 = tk.Button(self, text="Vider la base de donnée d'apprentissage", command=self.clear_learning_table, )
        button5.pack(side="top")

        # Prediction DATA
        button6 = tk.Button(self, text="Importer des fichiers patients (prédiction)", command=self.import_prediction_data, )
        button6.pack(side="top")

        button7 = tk.Button(self, text="Importer un fichier patient (prédiction)", command=self.import_unique_prediction_data, )
        button7.pack(side="top")

        button8 = tk.Button(self, text="Afficher les données de prédiction", command=self.see_prediction_table, )
        button8.pack(side="top")

        button9 = tk.Button(self, text="Vider la base de donnée de prédiction", command=self.clear_prediction_table, )
        button9.pack(side="top")

    def clean_df_db_dups(self, df, tablename, engine, dup_cols=[],
                         filter_continuous_col=None, filter_categorical_col=None):
        """
        Remove rows from a dataframe that already exist in a database
        Required:
            df : dataframe to remove duplicate rows from
            engine: SQLAlchemy engine object
            tablename: tablename to check duplicates in
            dup_cols: list or tuple of column names to check for duplicate row values
        Optional:
            filter_continuous_col: the name of the continuous data column for BETWEEEN min/max filter
                                   can be either a datetime, int, or float data type
                                   useful for restricting the database table size to check
            filter_categorical_col : the name of the categorical data column for Where = value check
                                     Creates an "IN ()" check on the unique values in this column
        Returns
            Unique list of values from dataframe compared to database table
        """
        args = 'SELECT %s FROM %s' % (', '.join(['"{0}"'.format(col) for col in dup_cols]), tablename)
        args_contin_filter, args_cat_filter = None, None
        if filter_continuous_col is not None:
            if df[filter_continuous_col].dtype == 'datetime64[ns]':
                args_contin_filter = """ "%s" BETWEEN Convert(datetime, '%s')
                                              AND Convert(datetime, '%s')""" % (filter_continuous_col,
                                                                                df[filter_continuous_col].min(),
                                                                                df[filter_continuous_col].max())

        if filter_categorical_col is not None:
            args_cat_filter = ' "%s" in(%s)' % (filter_categorical_col,
                                                ', '.join(["'{0}'".format(value) for value in
                                                           df[filter_categorical_col].unique()]))

        if args_contin_filter and args_cat_filter:
            args += ' Where ' + args_contin_filter + ' AND' + args_cat_filter
        elif args_contin_filter:
            args += ' Where ' + args_contin_filter
        elif args_cat_filter:
            args += ' Where ' + args_cat_filter

        df.drop_duplicates(dup_cols, keep='last', inplace=True)
        df = pd.merge(df, pd.read_sql(args, engine), how='left', on=dup_cols, indicator=True)
        df = df[df['_merge'] == 'left_only']
        df.drop(['_merge'], axis=1, inplace=True)
        return df

    def import_learning_data(self):

        # Getting path to directory we want to load
        directory = askdirectory(title="Import de dossiers patients")
        # Getting the list of all files to import
        cover = glob.glob(directory + "/**/*.csv", recursive=True)
        # Initialize list of all patients observation (id, review, class)
        patients = []
        # Creating engine using sqlachemy to use data.to_sql function
        engine = create_engine('mysql+mysqldb://root:Kaoutar08Ftouhi@localhost/medical_database?charset=utf8',
                               encoding='latin3')
        # For each file in the directory, read the content and copy it to the database
        for j in cover:
            data = pd.read_csv(j, sep=',', encoding='latin_1')
            #patient_id, review_text and the Class
            col_list = ['patient_id', 'review_text', 'Class']
            data = self.clean_df_db_dups(data, 'patient_labeled_table', engine, col_list)
            data.to_sql(name='patient_labeled_table', con=engine, index=False, if_exists='append')

    def import_prediction_data(self):

        # Getting path to directory we want to load
        directory = askdirectory(title="Import de dossiers patients")
        # Getting the list of all files to import
        cover = glob.glob(directory + "/**/*.csv", recursive=True)
        # Initialize list of all patients observation (id, review, class)
        patients = []
        # Creating engine using sqlachemy to use data.to_sql function
        engine = create_engine('mysql+mysqldb://root:Kaoutar08Ftouhi@localhost/medical_database?charset=utf8',
                               encoding='latin3')
        # For each file in the directory, read the content and copy it to the database
        for j in cover:
            data = pd.read_csv(j, sep=',', encoding='latin_1')
            #patient_id, review_text and the Class
            col_list = ['patient_id', 'review_text']
            data = self.clean_df_db_dups(data, 'patient_unlabeled_table', engine, col_list)
            data.to_sql(name='patient_unlabeled_table', con=engine, index=False, if_exists='append')

    def import_unique_learning_data(self):
        engine = create_engine('mysql+mysqldb://root:Kaoutar08Ftouhi@localhost/medical_database?charset=utf8',
                               encoding='latin3')
        filepath = askopenfilename(title="Import d'un dossiers patient",
                                   filetypes=[('csv files', '.csv'), ('all files', '.*')])

        data = pd.read_csv(filepath, sep=',', encoding='latin_1')
        col_list = ['patient_id', 'review_text', 'Class']
        data = self.clean_df_db_dups(data, 'patient_labeled_table', engine, col_list)
        data.to_sql(name='patient_labeled_table', con=engine, index=False, if_exists='append')

    def import_unique_prediction_data(self):
        engine = create_engine('mysql+mysqldb://root:Kaoutar08Ftouhi@localhost/medical_database?charset=utf8',
                               encoding='latin3')
        filepath = askopenfilename(title="Import d'un dossiers patient",
                                   filetypes=[('csv files', '.csv'), ('all files', '.*')])

        data = pd.read_csv(filepath, sep=',', encoding='latin_1')
        col_list = ['patient_id', 'review_text']
        data = self.clean_df_db_dups(data, 'patient_unlabeled_table', engine, col_list)
        data.to_sql(name='patient_unlabeled_table', con=engine, index=False, if_exists='append')


    def see_learning_table(self):
        connection = MySQLdb.connect(host="localhost", user="root", passwd="Kaoutar08Ftouhi", db="medical_database")

        c = connection.cursor()
        c.execute("SELECT * FROM patient_labeled_table")
        rows = c.fetchall()
        for eachRow in rows:
            print(eachRow)

    def see_prediction_table(self):
        connection = MySQLdb.connect(host="localhost", user="root", passwd="Kaoutar08Ftouhi", db="medical_database")

        c = connection.cursor()
        c.execute("SELECT * FROM patient_unlabeled_table")
        rows = c.fetchall()
        for eachRow in rows:
            print(eachRow)

    def clear_learning_table(self):
        connection = MySQLdb.connect(host="localhost", user="root", passwd="Kaoutar08Ftouhi", db="medical_database")

        c = connection.cursor()
        c.execute("DELETE FROM patient_labeled_table")
        connection.commit()

    def clear_prediction_table(self):
        connection = MySQLdb.connect(host="localhost", user="root", passwd="Kaoutar08Ftouhi", db="medical_database")

        c = connection.cursor()
        c.execute("DELETE FROM patient_unlabeled_table")
        connection.commit()
