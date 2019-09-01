from tkinter import *
from random import randint
import time, math


class Path:
    def __init__(self, root, settings):
        # base settings
        self.settings = dict(settings)

        # Upper frame partition
        self.visual = Frame(root)
        self.ui = Frame(root)
        self.visual.grid(row=0, column=0)
        self.ui.grid(row=0, column=1)

        # Visual setup

        self.prev_r = -1
        self.pillar_col = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#00FFFF', '#FF00FF']
        self.buff = 10
        self.size = 600
        self.lx = int(self.size)
        self.ly = self.size
        self.can = Canvas(self.visual, width=self.lx + 2 * self.buff, height=self.ly + 2 * self.buff, bg='#000000')
        self.can.pack()

        self.set_val = [[self.lx, self.ly * 0.75], [self.lx * 0.25, self.ly], [0, self.ly * 0.5], [self.lx * 0.5, 0]]
        self.pillars = []
        self.joints = []

        for i in range(self.settings['pillar_num']['data']):
            if self.settings['mode']['data'] == modes[0]:
                x = randint(self.buff, self.buff + self.lx)
                y = randint(self.buff, self.buff + self.ly)

            elif self.settings['mode']['data'] == modes[1]:
                x = self.set_val[i][0]
                y = self.set_val[i][1]

            elif self.settings['mode']['data'] == modes[2]:
                angle = i * 2 * math.pi / self.settings['pillar_num']['data']
                x = 0.5 * self.lx * (1 + math.cos(angle))
                y = 0.5 * self.ly * (1 + math.sin(angle))
            self.pillars.append([[x, y], self.draw_point(x, y, 3, '#FFFFFF')])
        self.points = []
        x = randint(0, self.lx)
        y = randint(0, self.ly)
        self.points.append([[x, y], self.draw_point(x, y, 3, '#000000')])

        # UI setup
        button = Button(self.ui, text="Reset", bg="#E9C654")
        button.bind("<Button-1>", self.reset)
        button.grid(row=len(self.settings) * 2 + 1, column=0)

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

        self.counter = 0

    def next(self):

        r_pillar = randint(0, self.settings['pillar_num']['data'] - 1)
        if self.settings['choice']['data'] == choices[1]:
            while self.prev_r == r_pillar:
                r_pillar = randint(0, self.settings['pillar_num']['data'] - 1)
        elif self.settings['choice']['data'] == choices[2]:
            while (self.prev_r + 1) % self.settings['pillar_num']['data'] == r_pillar:
                # or (self.prev_r-1)%self.self.settings['pillar_num'] == r_pillar:
                r_pillar = randint(0, self.settings['pillar_num']['data'] - 1)
        elif self.settings['choice']['data'] == choices[3]:
            while (self.prev_r + 1) % self.settings['pillar_num']['data'] == r_pillar or (self.prev_r - 1) % \
                    self.settings['pillar_num']['data'] == r_pillar:
                r_pillar = randint(0, self.settings['pillar_num']['data'] - 1)
        elif self.settings['choice']['data'] == choices[4]:
            while (self.prev_r + self.settings['pillar_num']['data'] // 2) % self.settings['pillar_num'][
                'data'] == r_pillar:
                r_pillar = randint(0, self.settings['pillar_num']['data'] - 1)
        new_point = self.mid_point(self.points[-1][0], self.pillars[r_pillar][0], self.settings['percent']['data'])
        if len(self.settings['colour']['data'])==7 and self.settings['colour']['data']<='f':
            self.points.append(
                [new_point, self.draw_point(new_point[0], new_point[1], 1, self.settings['colour']['data'])])
        else:
            self.points.append([new_point, self.draw_point(new_point[0], new_point[1], 1, self.pillar_col[r_pillar % 6])])
        self.prev_r = r_pillar

        if self.settings['iteration_depth']['data'] < self.counter:
            global done
            done = True
        self.counter += 1

    def draw_point(self, x, y, size, colour):
        return self.can.create_line(x + self.buff, y + self.buff,
                                    x + size / 2 + self.buff, y + size / 2 + self.buff,
                                    fill=colour, width=1)

    def mid_point(self, va, vb, magnitude):
        return [round(va[0] + (vb[0] - va[0]) * magnitude, 0), round(va[1] + (vb[1] - va[1]) * magnitude, 0)]

    def adb(self, thing):
        if type(int) or type(float):
            return thing + self.buff
        else:
            for i in range(len(thing)):
                thing[i] += self.buff
            return thing

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
    'pillar_num': {'data': 4, 'type': 'int_entry'},  # number of pillars,
    'percent': {'data': 0.5, 'type': 'float_entry'},  # how far to move towards the pillar
    'choice': {'data': 'no consecutive pillars', 'type': 'menu'},  # chances and rules to select pillars
    'mode': {'data': 'distributed in a circle', 'type': 'menu'},  # how to position the pillars
    'iteration_depth': {'data': 10000, 'type': 'int_entry'},
    'colour':{'data':'#', 'type':'string_entry'}
}

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
