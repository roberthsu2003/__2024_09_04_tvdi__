import tkinter as tk
from tkinter import Canvas, Scrollbar, HORIZONTAL
from PIL import Image, ImageTk

class TopCanvas(Canvas):
    """
    Custom Canvas widget that handles image display and click events.
    """
    def __init__(self, parent, image_paths, image_names, on_image_click, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.image_paths = image_paths
        self.image_names = image_names
        self.on_image_click_callback = on_image_click
        
        # ===Horizontal Scroll Bar=====
                # Set canvas scroll region
        total_width = len(image_paths) * (250 + 50) + 5  # 計算所有圖片所需的寬度
        self.config(scrollregion=(0, 0, total_width, 400))  # 假設高度 600

        # Add horizontal scrollbar
        self.h_scrollbar = Scrollbar(parent, orient=HORIZONTAL, command=self.xview)
        self.h_scrollbar.pack(side="bottom", fill="x")
        self.configure(xscrollcommand=self.h_scrollbar.set)
        # ===End Horizontal Scroll Bar=====
        


        # Load and display the images
        # x position
        start_x = 5
        poster_width = 250
        gap = 50

        self.photos = []
        for i, (path, name) in enumerate(zip(self.image_paths, self.image_names)):
            image = Image.open(path).resize((250, 375))
            photo = ImageTk.PhotoImage(image)
            x = start_x + (poster_width + gap) * i + poster_width // 2
            self.create_image(x, 200, image=photo) 
            # self.create_image(i * 250 + 200, 200, image=photo)
            self.photos.append(photo)

        # Bind click event
        self.bind("<Button-1>", self._handle_click)

    def _handle_click(self, event):
        """
        Internal handler for Canvas click events.
        """
        # Convert event.x to the actual canvas coordinate
        canvas_x = self.canvasx(event.x)  # Adjust for scrolling

        # Define the image width and gap
        poster_width = 250
        gap = 50

        # Calculate which image was clicked
        clicked_index = (canvas_x - 5) // (poster_width + gap)  # Subtract initial offset
        if 0 <= clicked_index < len(self.image_names):
            if self.on_image_click_callback:
                self.on_image_click_callback(self.image_names[int(clicked_index)])