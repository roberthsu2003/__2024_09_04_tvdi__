from ttkthemes import ThemedTk
# import datasource


class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
    print("Hello Tkinter and Python")
    pass



def main():
    # datasource.download_data() #下載至資料庫
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()