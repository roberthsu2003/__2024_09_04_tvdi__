from tkinter import ttk
from PIL import ImageTk, Image


class ImageButton(ttk.Button):
    def __init__(self,master=None, **kwargs):
        self.icon_image = Image.open("refresh.png")
        self.icon_photo = ImageTk.PhotoImage(self.icon_image)
        super().__init__(master=master,image=self.icon_photo,**kwargs)

        