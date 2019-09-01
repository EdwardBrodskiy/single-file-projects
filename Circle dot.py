from tkinter import *
from random import randint
import time, math


class Path:
    def __init__(self, root, settings):
        # base settings
        self.settings = dict(settings)
        
        self.counter = time.clock()

        # Upper frame partition
        self.visual = Frame(root)
        self.ui = Frame(root)
        self.visual.grid(row=0, column=0)
        self.ui.grid(row=0, column=1)

        # Visual setup

        self.buff = 10
        self.size = 750
        self.lx = int(self.size)
        self.ly = int(self.size)
        self.can = Canvas(self.visual, width=self.lx + 2 * self.buff, height=self.ly + 2 * self.buff, bg='#000000')
        self.can.pack()

        self.points = []
        self.joints = []
        self.lines = []

        # Graphics

        # outer circle
        self.can.create_oval(self.buff, self.buff, self.lx + self.buff, self.ly + self.buff, outline='#ffffff')

        # guide lines
        for i in range(self.settings['point_num']['data']):
            angle = i * math.pi / self.settings['point_num']['data']
            x = 0.5 * self.lx * (1 + math.cos(angle)) 
            opx = 0.5 * self.lx * (1 + math.cos(angle + math.pi))
            y = 0.5 * self.ly * (1 + math.sin(angle))
            opy = 0.5 * self.ly * (1 + math.sin(angle + math.pi))
            self.lines.append([{'croods': [x, y, opx, opy], 'col': '#000000'},
                               self.can.create_line(x + self.buff, y + self.buff, opx + self.buff, opy + self.buff,
                                                    fill='#000000')])

        # points
        c = 0
        self.last = time.clock()
        self.first = True
        for i in range(self.settings['point_num']['data']):
            angle = i * math.pi / self.settings['point_num']['data']
            x = 0.5 * self.lx * (1 + math.cos(angle))
            y = 0.5 * self.ly * (1 + math.sin(angle))
            '''
            if c == self.settings['study point']['data']:
                self.prev = [x + self.buff,y + self.buff]
            '''    
            self.points.append([[x - 0.5 * self.lx, y - 0.5 * self.ly, angle],
                                self.draw_point((x - 0.5 * self.lx) * math.sin(self.counter + angle) + 0.5 * self.lx,
                                                (y - 0.5 * self.ly) * math.sin(self.counter + angle) + 0.5 * self.ly,
                                                6, self.settings['colour']['data'])]
                               )
            c += 1

        # UI setup

        self.output_settings()

        button = Button(self.ui, text="Show lines", bg="#1FC76D")
        button.bind("<Button-1>", self.fade_start)
        button.grid(row=len(self.settings) * 2 + 1, column=0)
        self.fadepro = False
        self.fadec = 0

        button = Button(self.ui, text="Reset", bg="#E9C654")
        button.bind("<Button-1>", self.reset)
        button.grid(row=len(self.settings) * 2 + 2, column=0)

    def next(self):
        self.counter = time.clock()
        #self.counter += self.settings['shift']['data']
        c = 0

        for i in self.points:
            if self.first and c == self.settings['study point']['data']:
                nx = i[0][0] * math.sin(self.counter*self.settings['x shift']['data'] + i[0][2]) + 0.5 * self.lx + self.buff
                ny = i[0][1] * math.sin(self.counter*self.settings['y shift']['data'] + i[0][2]) + 0.5 * self.ly + self.buff
                self.prev = [nx, ny]
                self.last = self.counter
                self.first = False
                
            elif c == self.settings['study point']['data'] and self.counter >self.last+0.1:
                nx = i[0][0] * math.sin(self.counter*self.settings['x shift']['data'] + i[0][2]) + 0.5 * self.lx + self.buff
                ny = i[0][1] * math.sin(self.counter*self.settings['y shift']['data'] + i[0][2]) + 0.5 * self.ly + self.buff
                self.can.create_line(self.prev[0], self.prev[1], nx, ny, fill = 'red')
                self.prev = [nx, ny]
                self.last = self.counter

            self.move_point(i[0][0] * math.sin(self.counter*self.settings['x shift']['data'] + i[0][2]) + 0.5 * self.lx,
                            i[0][1] * math.sin(self.counter*self.settings['y shift']['data'] + i[0][2]) + 0.5 * self.ly,
                            6, i[1])
            c +=1
        if self.fadepro and not self.fadec % 1000:
            self.fade(self.lines)

        self.fadec += 1
    def draw_point(self, x, y, size, colour):
        return self.can.create_oval(x - size / 2 + self.buff, y - size / 2 + self.buff,
                                    x + size / 2 + self.buff, y + size / 2 + self.buff,
                                    fill=colour, outline=colour, width=1)

    def move_point(self, x, y, size, it):
        self.can.coords(it, x - size / 2 + self.buff, y - size / 2 + self.buff,
                        x + size / 2 + self.buff, y + size / 2 + self.buff)

    def mid_point(self, va, vb, magnitude):
        return [round(va[0] + (vb[0] - va[0]) * magnitude, 0), round(va[1] + (vb[1] - va[1]) * magnitude, 0)]

    def adb(self, thing):
        if type(int) or type(float):
            return thing + self.buff
        else:
            for i in range(len(thing)):
                thing[i] += self.buff
            return thing

    def output_settings(self):
        row_c = 0
        for i in self.settings:

            self.settings[i]['label'] = Label(self.ui, text=i)
            self.settings[i]['label'].grid(column=0, row=row_c)
            row_c += 1

            if self.settings[i]['type'] == 'int_entry':
                self.settings[i]['variable'] = IntVar(self.ui, value=self.settings[i]['data'])
                self.settings[i]['widget'] = Entry(self.ui, textvariable=self.settings[i]['variable'])

            elif self.settings[i]['type'] == 'float_entry':
                self.settings[i]['variable'] = DoubleVar(self.ui, value=self.settings[i]['data'])
                self.settings[i]['widget'] = Entry(self.ui, textvariable=self.settings[i]['variable'])

            elif self.settings[i]['type'] == 'string_entry':
                self.settings[i]['variable'] = StringVar(self.ui, value=self.settings[i]['data'])
                self.settings[i]['widget'] = Entry(self.ui, textvariable=self.settings[i]['variable'])

            elif self.settings[i]['type'] == 'menu':
                self.settings[i]['variable'] = StringVar(self.ui, value=self.settings[i]['data'])

                if i == 'choice':
                    self.settings[i]['widget'] = OptionMenu(self.ui, self.settings[i]['variable'], *choices)
                elif i == 'mode':
                    self.settings[i]['widget'] = OptionMenu(self.ui, self.settings[i]['variable'], *modes)

            self.settings[i]['widget'].grid(column=0, row=row_c)
            row_c += 1

    def fade_start(self, event):
        self.fadepro = True

    def fade(self, things):
        for i in things:
            newcol = self.inc_hex(i[0]['col'], 1)
            if newcol:
                i[0]['col'] = newcol
                self.can.itemconfig(i[1], fill=newcol)
            else:
                newcol = '#ffffff'
                i[0]['col'] = newcol
                self.can.itemconfig(i[1], fill=newcol)
                self.fadepro = False

    def inc_hex(self, h, inc):
        nh = '#'
        full = 0
        for i in range(len(h) // 2):
            temp = self.dec(h[i * 2 + 1:(i + 1) * 2 + 1]) + inc
            if temp >= 255:
                full += 1
                temp = 255
            if len(hex(temp)[2:]) == 1:
                nh += '0' + hex(temp)[2:]
            else:
                nh += hex(temp)[2:]

        if full == 3:
            return False
        return nh

    def dec(self, num):
        a = '0123456789abcdef'
        p = 0
        out = 0
        for i in range(len(num)):
            x = a.find(num[len(num) - i - 1])
            out += x * 16 ** i
        return out

    def reset(self, event):
        global done
        done = False

        for i in self.settings:
            self.settings[i]['data'] = self.settings[i]['variable'].get()

        self.__init__(root, self.settings)


root = Tk()
root.title("Chaos Game")
# base setting states
types = ('int_entry', 'float_entry', 'menu', 'menu')
choices = ('random', 'max streak of 1', 'no consecutive pillars', 'pillars on either side ignored',
           'can not be on the opposite side')
modes = ('random positions', '4 pillar special setup', 'distributed in a circle')
# base settings
settings = {
    'point_num': {'data': 8, 'type': 'int_entry'},  # number of points,
    'study point': {'data': 1, 'type': 'int_entry'},
    'x shift': {'data': 0.7, 'type': 'float_entry'},  # how far to move each iteration in the x
    'y shift': {'data': 0.7, 'type': 'float_entry'},  # how far to move each iteration in the y
    'colour': {'data': '#FFFFFF', 'type': 'string_entry'}
}
'''

'choice': {'data': 'no consecutive pillars', 'type': 'menu'},  # chances and rules to select pillars
'mode': {'data': 'distributed in a circle', 'type': 'menu'},  # how to position the pillars
'iteration_depth': {'data': 10000, 'type': 'int_entry'},

'''
path = Path(root, settings)
count = 0
done = False
while True:

    if not count % 500 or done:
        root.update_idletasks()
        root.update()
    else:
        path.next()
    count += 1
