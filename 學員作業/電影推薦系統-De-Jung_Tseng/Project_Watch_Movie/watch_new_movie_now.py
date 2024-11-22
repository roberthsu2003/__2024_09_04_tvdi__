from  tkinter import ttk
from ttkthemes import ThemedTk
import view
# define a class Window inherited from Themedtk
class Window(ThemedTk):
    #initialize this class
    # pop out a dialogue windows upon initializing
    # 3 frame : top, bottom, bottom left, bottom right 
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #start laypot from here!
        self.title('Whach new movie now!')
        self.resizable(False,False)
        style=ttk.Style(self)
        style.configure('TopFrame.TLabel',font=('Arial',20))

        # ======Dialog========
        # not yet build the class of Logindialog
        self.login_dialog = view.LoginDialog(self, self.check_credentials)
        self.withdraw()  # 隱藏主視窗直到登入成功
        # ======End Dialog========
        # =====Top Frame====
        top_frame=ttk.Frame(self)
        # =====Top Frame===
        # ====End Top Frame===

        # =====Bottom Frame====



        
        # =====End Bottom Frame====



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
