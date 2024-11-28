from tkinter import ttk
import tkinter as tk

class CustomerFrame(ttk.Frame):
    def __init__(self, master=None, customers=None, **kwargs):
        super().__init__(master=master, **kwargs)
        self.selected_customer = tk.StringVar()
        for idx, customer in enumerate(customers):
            ttk.Radiobutton(
                self, text=customer, value=customer,
                variable=self.selected_customer, command=self.radio_button_selected
            ).grid(row=idx, column=0, sticky='w')

    def radio_button_selected(self):
        self.event_generate("<<Radio_Button_Selected>>")
