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
# Main application which allows us to navigate through windows
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)

        self.frames = {}

        for F in (Menu, Page1, Page2, Page3):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row = 0, column = 0, sticky = "nsew")


        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#Menu window
class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="I Importer des données", command=lambda: controller.show_frame(Page1))
        button1.pack()
        button2 = tk.Button(self, text="II Apprentissage", command=lambda: controller.show_frame(Page2))
        button2.pack()
        button3 = tk.Button(self, text="III Interpréteur de modèle", command=lambda: controller.show_frame(Page3))
        button3.pack()


# Windows which allows the user to load new data
class Page1(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Retour au menu principal", command=lambda: controller.show_frame(Menu))
        button1.pack(side="bottom")

        button2 = tk.Button(self, text="Importer des fichiers patients", command=self.importer_des_données, )
        button2.pack(side="top")

        button3 = tk.Button(self, text="Afficher les fichiers patients", command=self.see_database_content, )
        button3.pack(side="top")

        button4 = tk.Button(self, text="Ajouter des données à la BDD", command=self.write_in_database, )
        button4.pack(side="top")

    def importer_des_données(self):

        #Getting path to directory we want to load
        directory = askdirectory(title="Import de dossiers patients")
        print("The path to directory is "+directory)
        cover = [file for file in glob.glob(directory+"/**/*.csv", recursive=True)]
        print ("These are all the files paths"+', '.join(cover))
        print("this is the csv content")
        for j in cover:
            try:
                data = pd.read_csv(j, sep=';', encoding='utf_8')
                #for index, row in data.iterrows():
                    #print (row['patient_id'], row['review'])
                for row in data.itertuples():
                    print(row)
                print(data)
                print (data.values)
                print(data.size)
                print(data.__class__)
                print(cover.__class__)
                print(j)
            except:
                showerror()
            return

        #Getting path to the file we want to load
        # filepath = askopenfilename(title="Import de dossier patient", filetypes=[('csv files', '.csv'), ('all files', '.*')])
        # if filepath:
        #     try:
        #         # Putting data into a dataframe
        #         new_data = pd.read_csv(filepath, sep=';', encoding='utf_8')
        #         print (new_data)
        #     except:  # <- naked except is a bad idea
        #         showerror("Open Source File", "Failed to read file\n'%s'" % filepath)
        #     return




    def see_database_content(self):
        connection = MySQLdb.connect(host="localhost", user="root", passwd="Kaoutar08Ftouhi", db="medical_database")

        c = connection.cursor()
        c.execute("SELECT * FROM patient_database")
        rows = c.fetchall()
        for eachRow in rows:
            print(eachRow)

    def write_in_database(self):
        connection = MySQLdb.connect(host="localhost", user="root", passwd="Kaoutar08Ftouhi", db="medical_database")

        c = connection.cursor()
        c.execute("INSERT INTO patient_database (id_patient, review, class) VALUES (%s, %s, %s)",
                  (99, 'patient 99 review',0))
        connection.commit()

# Windows which allows the user to train new models, store models
class Page2(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Retour au menu principal", command=lambda: controller.show_frame(Menu))
        button1.pack(side="bottom")

# Windows which allows the user to make predictions and interpret it
class Page3(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Retour au menu principal", command=lambda: controller.show_frame(Menu))
        button1.pack(side="bottom")


# Create the application
app = Application()
app.title("Interface d'apprentissage automatique")
app.geometry('700x700')
app.mainloop()
