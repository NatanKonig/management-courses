from tkinter import tk


class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()

        self.call("source", "./theme/forest-dark.tcl")
        self.style.theme_use("forest-dark")

    
class JanelaLogin(tk.Toplevel):
    def __init__(self):
        