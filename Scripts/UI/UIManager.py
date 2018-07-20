from tkinter import *
import webbrowser
from win32api import GetSystemMetrics
import UIController

class AppUI(Frame):
    MaxColumn  = 4
    def __init__(self,master=None):
        Frame.__init__(self,master,relief=RAISED,bd=2)
        self.parent = master
        
        #create UI component
        self.CreateMenu()
        self.CreateButtons()
        self.CreateDownloadField()
        
        try:
            self.master.config(menu = self.menubar)
            self.master.title("Scrawl Manga")
        except AttributeError:
            self.master.tk.call(master, "config", "-menu", self.menubar)
            
    #UI of each emelemt
    def CreateMenu(self):
        self.menubar = Menu(self)
        file = Menu(self.menubar,tearoff =0)
        self.menubar.add_cascade(label="File", menu=file)
        file.add_command (label = "Open File...",command = self.OnOpen)
        file.add_separator()
        file.add_command (label="Exit",command= self.OnExit)
        
        help = Menu(self.menubar,tearoff=0)
        self.menubar.add_cascade(label="Help",menu=help)
        help.add_command (label = "About",command=self.OnAbout)
        help.add_command (label = "Report",command=self.OnReport)
        
    def CreateButtons(self,r=0):
        panel = PanedWindow(self,width=GetSystemMetrics(0))
        panel.grid(row=r,column = 0, columnspan =self.MaxColumn,sticky=W)
        buttons = PanedWindow(self,width=GetSystemMetrics(0))
        buttons.grid(row=r,column=0, columnspan=self.MaxColumn,sticky=W)
        
        start = Button(buttons, text="start", compound = LEFT,command = self.OnStast)
        start.grid(row=0, column=0,sticky=W)
        
        stop= Button(buttons, text="stops",command = self.OnStop)
        stop.grid(row=0, column=1,sticky=W)
        

    def CreateDownloadField(self,r=1):
        panel = PanedWindow(self)
        panel.grid(row=r,column = 0, columnspan =self.MaxColumn,sticky=W)
        
    #Function in UI
    def OnStast(self):
        pass
        print ("OnStart Click")
        
    def OnOpen(self):
        pass
        print ("OnOpen Click")
    def OnStop(self):
        pass
        print ("OnStop Click")
    def OnExit(self):
        self.quit()
    def OnAbout(self):
        pass
        print ("OnAbout Click")
        
    def OnReport(self):
        pass
        webbrowser.open("https://github.com/dienthinh0/Scrawl-Manga/issues/new")
        
root = Tk()
root.minsize(500, 250)
root.pack_propagate(0)
app = AppUI(root)
app.pack()

root.mainloop()
