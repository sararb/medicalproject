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
from medicalproject.Project.Interface.page1.Page1 import Page1
from medicalproject.Project.Interface.page2.Page2 import Page2
from medicalproject.Project.Interface.page3.Page3 import Page3

# Main application which allows us to navigate through windows
class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (Menu, Page1, Page2, Page3):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Menu)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

# Menu window
class Menu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="I Importer des données", command=lambda: controller.show_frame(Page1))
        button1.pack()
        button2 = tk.Button(self, text="II Apprentissage", command=lambda: controller.show_frame(Page2))
        button2.pack()
        button3 = tk.Button(self, text="III Interpréteur de modèle", command=lambda: controller.show_frame(Page3))
        button3.pack()

# Create the application
app = Application()
app.title("Interface d'apprentissage automatique")
app.geometry('700x700')
app.mainloop()
