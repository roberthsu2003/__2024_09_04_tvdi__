from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
import view
from tkinter import messagebox

class Window(ThemedTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Watch new movie now!')
        
        # ====Geometry====
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
        # 設定樣式
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel', font=('Arial', 20))
        
        # 創建主容器
        main_container = ttk.Frame(self, padding=10)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # =====Top Frame=====
        self.top_frame = ttk.LabelFrame(main_container, text="你可能會喜歡", padding=10)
        self.top_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        # ====Top Canvas=====

        self.canvas = view.TopCanvas(
            self.top_frame, 
            image_name= "我想當瑪奇瑪小姐的狗",
            image_path= "C:/Users/USER/Documents/GitHub/Salt_Eagle_Project/Images/puppy.png",
            on_image_click=self.add_to_watch_list,
            width=200,
            height=150,
            bg="gray",
        )
        self.canvas.pack(fill="both", expand=True)
        # ====End Top Canvas=====
        
        # Top frame label
        self.top_label = ttk.Label(self.top_frame, text="推薦影片區")
        self.top_label.pack(anchor=tk.W)
        # =====End Top Frame=====
        
        # =====Bottom Container=====
        bottom_container = ttk.Frame(main_container)
        bottom_container.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # =====Bottom Frame Left=====
        self.bottom_frame_left = ttk.LabelFrame(bottom_container, text="待播清單", padding=10)
        
        
        # Bottom left frame label
        self.bottom_left_label = ttk.Label(self.bottom_frame_left, text="待播影片")
        self.bottom_left_label.pack(anchor=tk.W)

        # ====Watch List Treeview====
        self.watch_list = view.TreeViewWidget(self.bottom_frame_left, "待播清單")
        self.watch_list.pack(fill="both", expand=True)
        print(type(self.watch_list))
        # =====End =Watch List Treeview====
        self.bottom_frame_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        # =====End Bottom Frame Left=====


        
        # =====Bottom Frame Right=====
        self.bottom_frame_right = ttk.LabelFrame(bottom_container, text="觀看清單", padding=10)
        
        
        # Bottom right frame label
        self.bottom_right_label = ttk.Label(self.bottom_frame_right, text="已觀看影片")
        self.bottom_right_label.pack(anchor=tk.W)

        # =====Played List Treeview====
        self.played_list = view.TreeViewWidget(self.bottom_frame_right, "觀看清單")
        self.played_list.pack(fill="both", expand=True)
        # =====End Played List Treeview====

        self.bottom_frame_right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 0))
        # =====End Bottom Frame Right=====
    
    def add_to_watch_list(self, movie_name):
        """
        Callback function to add the movie name to the watch list.
        """
        # 確保 watch_list 是正確的 Treeview
        assert hasattr(self.watch_list, "get_children"), "watch_list 必須是 ttk.Treeview 或有 get_children 方法"

        # 防止重複加入
        for child in self.watch_list.get_children():
            if self.watch_list.item(child, "values")[0] == movie_name:
                messagebox.showinfo("提示", f"'{movie_name}' 已經存在於列表中!")
                return

        # 添加到 Treeview 中
        self.watch_list.insert("", "end", values=(movie_name,))


def main():
    window = Window(theme="breeze")
    window.mainloop()

if __name__ == '__main__':
    main()