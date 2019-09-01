from tkinter import *
from random import randint

class Path:
    def __init__(self,root):
        buff=10
        self.buff=buff
        self.lx=1000
        self.ly=1000
        self.can=Canvas(root,width=self.lx+buff,height=self.ly+buff,bg='#000000')
        self.can.pack()
        self.curve=[1,0,3]
        self.itteration=1
        self.output=[]
        self.plot()
        root.bind("a", self.nextcurve)
    def nextcurve(self, event):
        self.itteration+=1
        right=list(self.changedirection(self.rotate(-1)))
        left=list(self.changedirection(self.rotate(1)))
        self.curve=right+[1]+self.curve+[0]+self.curve+[3]+left
        self.plot()
        
    def rotate(self,halfpi):
        c=list(self.curve)
        for i in range(len(c)):
            c[i]=(c[i]+halfpi)%4
        return c

    def changedirection(self,d):
        c=list(d)
        for i in range(len(c)):
            if c[i]==1 or c[i]==3:
                c[i]=(c[i]+2)%4
        return c
                

    def plot(self):
        size=0
        for i in self.curve:
            if i==0:
                size+=1
            elif i==2:
                size-=1
                
        #size=self.itteration**3
        step=self.ly/size
        pos=[self.buff//2,self.ly+self.buff//2]
        if self.output!=[]:
            for i in self.output:
                self.can.delete(i)
            self.output=[]
        for i in self.curve:
            if i==0:
                newpos=[pos[0]+step,pos[1]]
            elif i==1:
                newpos=[pos[0],pos[1]-step]
            elif i==2:
                newpos=[pos[0]-step,pos[1]]
            else:
                newpos=[pos[0],pos[1]+step]
            
            self.output.append(self.can.create_line(pos[0],pos[1],newpos[0],newpos[1],fill='#FFDF00'))
            pos=list(newpos)
            
root = Tk()
root.title("Hilbert's Curve")


path=Path(root)

while True:
    root.update_idletasks()
    root.update()

root.mainloop()
