from tkinter import *
import random

class Ui:
    def __init__(self, root):
        self.root = root
        
class pick:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        
    def plot(self):
        tkStart = self.endNodes[0]
        tkEnd = self.endNodes[1]
        self.image = self.canvas.create_line(*tkStart, *tkEnd, fill = '#0000FF')
        #print(*tkStart, *tkEnd)
        #input(self.)
    def removeNode(self, node):
        self.endNodes.remove(node)

    def die(self):
        self.canvas.itemconfig(self.image, fill = '#000000')
        return self.image
        
class vertical(pick):
    def __init__(self, canvas, x, y, size):
        super().__init__(canvas, x, y, size)
        self.endNodes = [(x,y+self.size),(x,y-self.size)]
        self.plot()
        
    def fillNode(self, node):
        '''
        return horizontal(self.canvas, *node, self.size)
        '''
        
        return horizontal(self.canvas, *node, self.size)
        

class horizontal(pick):
    def __init__(self, canvas, x, y, size):
        super().__init__(canvas, x, y, size)
        self.endNodes = [(x+self.size,y),(x-self.size,y)]
        self.plot()

    def fillNode(self, node):
        '''
        return vertical(self.canvas, *node, self.size)
        '''
        
        return vertical(self.canvas, *node, self.size)
        
        
class DeadSpace:
    def __init__(self):
        self.outerNodes = {}
        self.deletedCount = 0

    def addNode(self, node):
        connections = 0
        full = []
        for i in self.outerNodes:
            xDifference = (node[0]-i[0])**2
            yDifference = (node[1]-i[1])**2
            if  xDifference == size**2 and yDifference == 0 or xDifference == 0 and yDifference == size**2:
                self.outerNodes[i] -= 1
                if self.outerNodes[i] == 0:
                    full.append(i)
                connections += 1
                
        for i in full:
            del self.outerNodes[i]
            
        self.deletedCount += len(full)
        
        self.outerNodes[node] = 4 - connections
        

        
root = Tk()
root.title("Toothpicks")

w = 700
h = 700
canvas = Canvas(root, width = w, height = h)
canvas.pack()

size = 5
picks = [horizontal(canvas, w//2, h//2, size)]
tkOldPicks = []
deadPicks = DeadSpace()

while True:
    newpicks = []
    for i in range(len(picks)):
        
        for node in picks[i].endNodes:
            free = True
            for j in range(i+1, len(picks)):
                if node[0] == picks[j].x and node[1] == picks[j].y:
                    free = False
                elif node in picks[j].endNodes:
                    free = False
                    picks[j].removeNode(node)
            
            if node in deadPicks.outerNodes:
                free = False
            
            if free:
                newpicks.append(picks[i].fillNode(node))

    for i in range(len(picks)):
        deadPicks.addNode((picks[i].x,picks[i].y))
        tkOldPicks.append(picks[i].die())

    picks = list(newpicks)
        

    #input(deadPicks.deletedCount )
    
    root.update_idletasks()
    root.update()
