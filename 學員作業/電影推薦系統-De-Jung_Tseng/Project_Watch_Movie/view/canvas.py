import tkinter as tk
from tkinter import Canvas
from PIL import Image, ImageTk

class TopCanvas(Canvas):
    """
    Custom Canvas widget that handles image display and click events.
    """
    def __init__(self, parent, image_path, image_name, on_image_click, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.image_path = image_path
        self.image_name = image_name
        self.on_image_click_callback = on_image_click

        # Load and display the image
        self.image = Image.open(self.image_path).resize((200, 150))
        self.photo = ImageTk.PhotoImage(self.image)
        self.create_image(100, 75, image=self.photo)

        # Bind click event
        self.bind("<Button-1>", self._handle_click)

    def _handle_click(self, event):
        """
        Internal handler for Canvas click events.
        """
        if self.on_image_click_callback:
            self.on_image_click_callback(self.image_name)
