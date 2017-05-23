import tkinter as tk
from tkinter.filedialog import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.bu1 = tk.Button(self)
        self.bu1["text"] = "Importer des données"
        self.bu1["command"] = self.import_csv
        self.bu1.pack(side="top")

        self.bu2 = tk.Button(self)
        self.bu2["text"] = "Apprentissage"
        self.bu2["command"] = self.traitement_des_textes
        self.bu2.pack(side="top")

        self.bu1 = tk.Button(self)
        self.bu1["text"] = "Interpréteur de modèle"
        self.bu1["command"] = self.intepretation_model
        self.bu1.pack(side="top")

        self.quit = tk.Button(self, text="QUITTER L'APPLICATION", fg="red",command=root.destroy,)
        self.quit.pack(side="bottom")

    def import_csv(self):
        filepath = askopenfilename(title="Import de dossiers patient",filetypes=[('csv files', '.csv'), ('all files', '.*')])
        txt = filepath.read()
        print(txt)
        print (filepath)


    def traitement_des_textes(self):
        root2 = Tk()
        root2.title("Apprentissage")
        root2.geometry('400x400+350+340')

    def intepretation_model(self):
        root3 = Tk()
        root3.title("Interprétation des modèles")
        root3.geometry('400x400+350+340')

root = tk.Tk()
root.title("Interface d'apprentissage automatique")
root.geometry('700x700+350+340')
app = Application(master=root)
app.mainloop()
