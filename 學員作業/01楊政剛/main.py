import pandas as pd
import numpy as np
import requests
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter import ttk


class Window(ThemedTk):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.title("Stock Analysis")
        #===============================
        style = ttk.Style(self)
        #===============================
        ttk.Label(self,text="Stock Analysis").pack()







def main():
    window= Window(theme='arc')
    window.mainloop()


if __name__ == '__main__':
    main()





