#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.filedialog import *
import pickle
import pandas as pd


# Main class for the entire user interface
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
        self.quit1 = tk.Button(self, text="QUITTER L'APPLICATION", fg="red", command=root.destroy, )
        self.quit1.pack(side="bottom")

    # Function which creates every button on the main window
    def create_widgets(self):
        self.bu1 = tk.Button(self, text = "I Importer des données", command = lambda: self.show_frame(Application2) )
        self.bu1.pack(side="top")

        self.bu2 = tk.Button(self, text = "II Apprentissage", command = self.create_widgets_2, )
        self.bu2.pack(side="top")

        self.bu3 = tk.Button(self, text = "III Interpréteur de modèle", command = self.create_widgets_3, )
        self.bu3.pack(side="top")


    # Function which creates every button on the main window
    def create_widgets_1(self):
        self.bu1.destroy()
        self.bu2.destroy()
        self.bu3.destroy()

        self.bu4 = tk.Button(self, text="1 Importer des fichiers patients", command=self.import_des_données, )
        self.bu4.pack(side="top")

        self.entry = tk.Entry(self)
        self.entry.pack(side="bottom")

        self.retour = tk.Button(self, text = "Retour au menu principal", fg ="blue", command=self.create_widgets)
        self.retour.pack(side="bottom")

    # Function which creates every button on the main window
    def create_widgets_2(self):
        self.bu1.destroy()
        self.bu2.destroy()
        self.bu3.destroy()
        self.bu5 = tk.Button(self, text="2 Importer des fichiers patients", command=self.traitement_des_textes, )
        self.bu5.pack(side="top")

        self.entry2 = tk.Entry(self)
        self.entry2.pack(side="bottom")

        self.retour2 = tk.Button(self, text = "Retour au menu principal", fg = "blue", command = self.create_widgets)
        self.retour2.pack(side="bottom")

        # Function which creates every button on the main window
    def create_widgets_3(self):
        self.bu1.destroy()
        self.bu2.destroy()
        self.bu3.destroy()
        self.bu6 = tk.Button(self, text="3 Importer des fichiers patients", command=self.traitement_des_textes, )
        self.bu6.pack(side="top")

        self.entry3 = tk.Entry(self)
        self.entry3.pack(side="bottom")

        self.retour3 = tk.Button(self, text="Retour au menu principal", fg="blue", command=self.create_widgets)
        self.retour3.pack(side="bottom")

    #blabla
    def import_des_données(self):
        print(1)
    # Function which invokes a new window for learning models
    def traitement_des_textes(self):
        print(10)

    # Function which invokes a new window for doing predictions and interpret it
    def intepretation_model (self):
        print(20)

    def show_frame(self,cont):
        frame = self.frames[cont]
        frame.tkraise()

# SubClass for the import interface
class Application2(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.import_patient_data_widget()

    def import_patient_data_widget(self):
        self.b1 = tk.Button(self)
        self.b1["text"] = "Importer des fichiers patients"
        self.b1["command"] = self.import_patient_data
        self.b1.pack(side="top")

        self.quit2 = tk.Button(self, text="QUITTER L'IMPORT DE DONNÉES", fg="red", command=root.destroy, )
        self.quit2.pack(side="bottom")

    def import_patient_data(self):
        filepath = askopenfilename(title="Import de dossiers patient",
                                   filetypes=[('csv files', '.csv'), ('all files', '.*')])
        print(filepath)
        new_data = pd.read_csv(filepath, sep=';', encoding='utf_8')
        print(new_data.values)
        new_data.to_pickle('/home/sebastien/PycharmProjects/PFE/medicalproject/interface/new_data.csv')

    def traitement_des_textes(self):
        new_data2 = pd.read_pickle('/home/sebastien/PycharmProjects/PFE/medicalproject/interface/new_data.csv')
        print(new_data2)

# Create the application
root = tk.Tk()
app = Application(master=root)
app.master.title("Interface d'apprentissage automatique")
app.master.geometry('700x700')


# Starting the program
app.mainloop()

#root = tk.Tk()
#root.title("Interface d'apprentissage automatique")
#root.geometry('700x700+350+340')
#app = Application(master=root)
