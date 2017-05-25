#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter.filedialog import *
import pickle
import pandas as pd

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

    def importer_des_données(self):
        filepath = askopenfilename(title="Import de dossiers patient",
                                   filetypes=[('csv files', '.csv'), ('all files', '.*')])
        new_data = pd.read_csv(filepath, sep=';', encoding='utf_8')
        new_data.to_pickle('/home/sebastien/PycharmProjects/PFE/medicalproject/interface/new_data.csv')
        print(new_data.head(10))


# Windows which allows the user to train new models
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
