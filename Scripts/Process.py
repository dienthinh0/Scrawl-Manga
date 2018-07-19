from progressbar import *
import progressbar
import time

class Process:
    name=""
    total =0
    current = 0
    progressUI = None
    callback = None
    def setup(self,name_a, total_a,callback_a):
        self.current = 0
        self.name= name_a
        if len(self.name)>20:
            self.name = self.name[:7]+"..."+self.name[-7:]
        self.total =total_a
        self.callback = callback_a
        widget = [Bar(left=self.name+ '('+str(self.total) +')'+' [',right=']'), ' [', progressbar.Timer(), '] ']
        self.progressUI = progressbar.ProgressBar(maxval =self.total,widgets = widget)
        
    def start(self):
        self.progressUI.start()
        
    def update(self):
        self.current= self.current +1
        self.progressUI.update(self.current)
        if self.current>=self.total:
            self.progressUI.finish()
            self.callback()
        