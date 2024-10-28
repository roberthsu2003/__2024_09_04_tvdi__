import datasource

from tkinter import ttk
import tkinter as tk
from ttkthemes import ThemedTk
from tkinter.messagebox import showinfo

class Window(ThemedTk):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('登入')
        #==============style===============
        style = ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Helvetica',20))
        #============end style===============
        
        #==============top Frame===============

        topFrame = ttk.Frame(self)
        ttk.Label(topFrame,text='空氣品質指標(AQI)(歷史資料)',style='TopFrame.TLabel').pack()
        topFrame.pack(padx=20,pady=20)
        
        #==============end topFrame===============

        #==============bottomFrame===============
        bottomFrame = ttk.Frame(self)
        sitenames = datasource.get_sitename()
        self.selected_site = tk.StringVar()
        sitenames_cb = ttk.Combobox(bottomFrame, textvariable=self.selected_site,values=sitenames,state='readonly')
        self.selected_site.set('請選擇站點')
        sitenames_cb.pack(side='left',expand=True,anchor='n')        
        

        # define columns
        columns = ('first_name', 'last_name', 'email')

        tree = ttk.Treeview(bottomFrame, columns=columns, show='headings')

        # define headings
        tree.heading('first_name', text='First Name')
        tree.heading('last_name', text='Last Name')
        tree.heading('email', text='Email')

        # generate sample data
        contacts = []
        for n in range(1, 100):
            contacts.append((f'first {n}', f'last {n}', f'email{n}@example.com'))

        # add data to the treeview
        for contact in contacts:
            tree.insert('', tk.END, values=contact)
        
        tree.pack(side='right')
        bottomFrame.pack(expand=True,fill='x',padx=20,pady=(0,20),ipadx=10,ipady=10)

            #==============end bottomFrame===============
        
        def agreement_changed(self):
            showinfo(
                title='Agreement',
                message= self.agreement.get()

            )
    
    
        

def main():
    window = Window(theme="arc")
    window.mainloop()

if __name__ == '__main__':
    main()