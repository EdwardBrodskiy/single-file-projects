from tkinter import *
from random import randint
import time


class Path:
    def __init__(self, root):
        self.buff = 10
        self.lx = 400
        self.ly = 200
        self.can = Canvas(root, width=self.lx + self.buff, height=self.ly + self.buff, bg='#000000')
        self.can.pack()
        self.c = 0
        self.siz = 200 / self.lx
        self.per = self.can.create_text(self.lx / 2 + self.buff, self.buff + 50, text='0.0%', fill='#FFFFFF')
        self.rec1 = self.can.create_rectangle(self.lx / 4 + self.buff, self.ly / 2 + self.buff - 20,
                                              3 * self.lx / 4 + self.buff, self.ly / 2 + self.buff + 20,
                                              outline='#FFFFFF')
        self.rec2 = self.can.create_rectangle(self.lx / 4 + self.buff, self.ly / 2 + self.buff - 20,
                                              self.c + self.lx / 4 + self.buff, self.ly / 2 + self.buff + 20,
                                              fill='#FFFFFF', outline='#FFFFFF')

    def next(self):
        self.c += 2
        self.can.coords(self.rec2, self.lx / 4 + self.buff, self.ly / 2 + self.buff - 20,
                        self.c + self.lx / 4 + self.buff, self.ly / 2 + self.buff + 20)
        self.can.itemconfig(self.per, text=(self.c * self.siz, '%'))


root = Tk()
root.title("Plz wait...")

path = Path(root)

while True:
    path.next()
    time.sleep(0.25)
    root.update_idletasks()
    root.update()

root.mainloop()
