from  tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
import view


class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Watch new movie now!')
        # ====Geomerty====
        # 設定視窗大小並置中
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        window_width = 800
        window_height = 450
        position_x = (screen_width - window_width) // 2
        position_y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

        # 禁止改變大小
        self.resizable(False, False)
        # =====End Geometry=====
        # 創建所有視窗元件
        self.create_widgets()
        
        # 處理登入對話框
        self.withdraw()  # 隱藏主視窗
        self.login_dialog = view.LoginDialog(self, title="登入")
        
        # 如果登入對話框被取消，關閉應用程序
        if not self.login_dialog.result:
            self.quit()
            return

    def create_widgets(self):
        # 將所有視窗元件的創建移到這個方法中
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel', font=('Arial', 20))
        
        # =====Main Frame=====
        self.main_frame = ttk.Frame(self.master, padding="10")
        self.main_frame.pack()
        # =====End Main Frame====


        # =====Top Frame====
        self.top_frame = ttk.LabelFrame(self.main_frame, text="Top Frame", padding="10")
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # 頂部框架的標籤
        self.top_label = ttk.Label(self.top_frame, text="Label")
        self.top_label.grid(row=0, column=0, sticky=tk.W)

        
        # ====End Top Frame===

        # =====Bottom Frame====
        self.bottom_frame_left = ttk.LabelFrame(self.main_frame, text="Bottom Frame Left", padding="10")
        self.bottom_frame_left.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # 底部左框架的標籤
        self.bottom_left_label = ttk.Label(self.bottom_frame_left, text="Label")
        self.bottom_left_label.grid(row=0, column=0, sticky=tk.W)
        
        # 底部右框架
        self.bottom_frame_right = ttk.LabelFrame(self.main_frame, text="Bottom Frame Right", padding="10")
        self.bottom_frame_right.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 底部右框架的標籤
        self.bottom_right_label = ttk.Label(self.bottom_frame_right, text="Label")
        self.bottom_right_label.grid(row=0, column=0, sticky=tk.W)






        # =====End Bottom Frame====
        #end laypot here

    #define instance function below
    def instancefunction():
        pass

# create function of the document
def main():
    # create an instance in class Window, named "window"
    #give a theme style to this window
    window=Window(theme="breeze")
    window.mainloop()
if __name__=='__main__':
    main()
