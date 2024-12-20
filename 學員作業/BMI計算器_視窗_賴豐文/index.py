import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from tkinter import messagebox
from tools import CustomMessagebox

class Window(ThemedTk):
    def __init__(self,theme:str|None,**kwargs):
        super().__init__(**kwargs)
        self.title("BMI計算器")
       
        self.resizable(False,False)
        style = ttk.Style()
        style.configure('input.TFrame',background='#ffffff')
        style.configure('press.TButton',font=('arial',17))
       
        titleFrame = ttk.Frame(self)
        title_label = ttk.Label(self, text="BMI計算器", font=("Arial", 20))
        title_label.pack(pady=10)
        titleFrame.pack(padx=100,pady=(0,5))
        
        input_frame = ttk.Frame(self,style='Input.TFrame')
        
        label_name = ttk.Label(input_frame, text="姓名(name):")
        label_name.grid(row=0, column=0, padx=10, pady=10,sticky=tk.E)

        self.name_value = tk.StringVar()
        self.name_value.set('')
        entry_name = ttk.Entry(input_frame,textvariable=self.name_value)
        entry_name.grid(row=0, column=1, padx=20, pady=20)

       
        label_height = ttk.Label(input_frame, text="身高 (cm):")
        label_height.grid(row=1, column=0, padx=10, pady=10,sticky=tk.E)

        self.hight_value = tk.StringVar()
        self.hight_value.set('')
        entry_height = ttk.Entry(input_frame,textvariable=self.hight_value)
        entry_height.grid(row=1, column=1, padx=20, pady=20)

        label_weight = ttk.Label(input_frame, text="體重 (kg):")
        label_weight.grid(row=2, column=0, padx=10, pady=10,sticky=tk.E)

        self.weight_value = tk.StringVar()
        self.weight_value.set('')
        entry_weight = ttk.Entry(input_frame,textvariable=self.weight_value)
        entry_weight.grid(row=2, column=1, padx=20, pady=20)    

        input_frame.pack(pady=50,padx=100)
        
        button_frame = ttk.Frame(self)
        button_calculate = ttk.Button(button_frame, text="計算", command=self.show_bmi_result,style='press.TButton')
        button_calculate.pack(side=tk.RIGHT,expand=True,fill=tk.X)

        button_close = ttk.Button(button_frame, text="關閉",command=self.destroy,style='press.TButton')
        button_close.pack(side=tk.LEFT,expand=True,fill=tk.X)
        button_frame.pack(padx=30,fill=tk.X,pady=(0,30))

    
    
    def show_bmi_result(self):
        try:
            name:str = self.name_value.get()
            height:int = int(self.hight_value.get())
            weight:int = int(self.weight_value.get())
        
        
        except ValueError:
            messagebox.showwarning("Warning","格式錯誤,欄位沒有填寫")
        except Exception:
            messagebox.showwarning("Warning","不知明的錯誤")
        else:
            self.show_result(name=name,height=height,weight=weight)


    def show_result(self,name:str,height:int,weight:int):
            bmi = weight / (height / 100) ** 2
            if bmi < 18.5:
                status = "體重過輕是怎樣~想當紙片人嗎!"
                ideal_weight = 18.5 * (height / 100) ** 2
                weight_change = ideal_weight - weight
                status_color = "red"
                advice = f"您需要至少增加 {abs(weight_change):.2f} 公斤才不會被風吹走。"
            elif 18.5 <= bmi <= 24.9:
                status = "唉呦正常喔~給您按個讚!"
                status_color = "blue"
                advice = "您的體重怎麼保持的~教一下吧！"
            else:
                status = "體重過重啦~有那麼好吃嗎?吃的那麼胖!"
                ideal_weight = 24.9 * (height / 100) ** 2
                weight_change = weight - ideal_weight
                status_color = "red"
                advice = f"您需要減肥 {abs(weight_change):.2f} 公斤才能再繼續吃。"

            CustomMessagebox(self,title="BMI",name=name,bmi=bmi,status=status,advice=advice,status_color=status_color)
            
            
            

def main():
    window = Window(theme='arc')
    window.mainloop()

if __name__ == '__main__':
    main()