### picture, gameplace size 조정

from tkinter import *
import random as rnd
import time as tt

# canvas size = 800 * 600
tk = Tk()
tk.title("Game")
tk.resizable(0,0)
tk.wm_attributes("-topmost",1)
canvas = Canvas(tk, width = 800, height = 600, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

##### images
# picture size = 694 * 353
# picture position = (55, 200)
picture = PhotoImage(file = 'new_example.gif')
canvas.create_image(55, 200, anchor = NW, image = picture)

# background
background = PhotoImage(file = 'background.gif')
canvas.create_image(0,0, anchor = NW, image = background)

# game_place
game_place = PhotoImage(file = 'gameplace.gif')
gameplace = canvas.create_image(55 ,200, anchor = NW, image = game_place)
# game_place = canvas.create_polygon(55,200,55,553,749,553,749,200, fill='silver',outline="cyan", width=3)

# Interface
interface = PhotoImage(file = 'interface.gif')
canvas.create_image(0,0, anchor = NW, image = interface)

# Title
title = PhotoImage(file = 'title.gif')
canvas.create_image(310, 70, anchor = NW, image = title)


##### Text - stage, life, time, percent(goals)
# Stage position
stage_num = 1
canvas.create_text(60, 30, anchor = NW,text =  "STAGE %d"%(stage_num), fill = 'white', font =('Helvetica', 20, 'bold'))

# Life position
canvas.create_text(570, 30, anchor = NW,text = "LIFE", fill = 'white',font =('Helvetica', 20, 'bold'))
life = PhotoImage(file = 'life.gif')
life_list = [canvas.create_image(660, 25, anchor = NW, image = life), canvas.create_image(690, 25, anchor = NW, image = life), canvas.create_image(720, 25, anchor = NW, image = life)]

# percent(goals)
goals = 80
canvas.create_text(60, 95, anchor = NW, text = '%d %%'%(goals),
                   fill = 'white', font = ('Helvetica', 20, 'bold'))
# Stage position
stage_num = 1
stage = canvas.create_text(60, 30, anchor = NW,text =  "STAGE %d"%(stage_num), fill = 'white', font =('Helvetica', 20, 'bold'))


### Game Characters
def distance(a,b):
    return ((b[0]-a[0])**2 + (b[1]-a[1])**2)**0.5

# player
player = PhotoImage(file = 'player.gif')
ghost = PhotoImage(file = 'ghost.gif')
class Ghost1:
    def __init__(self, canvas, ghost):
        self.canvas = canvas
        self.id = canvas.create_image(200, 300, anchor = CENTER, image = ghost)
        move_dx = [-2.5,2.5]
        move_dy = [-2.5,2.5]
        rnd.shuffle(move_dx)
        rnd.shuffle(move_dy)
        self.dx = move_dx[0]
        self.dy = move_dy[0]
        self.pos_ghost1 = self.canvas.coords(self.id)
        self.make_area = False
    def draw(self):
        self.canvas.move(self.id, self.dx, self.dy)
        pos_ghost1 = self.canvas.coords(self.id)
        if pos_ghost1[1] <= 220:    #200+20
            self.dy = 2
        if pos_ghost1[1] >= 538:   #558-20
            self.dy = -2
        if pos_ghost1[0] <= 74.5:   #55+19.5
            self.dx = 2
        if pos_ghost1[0] >= 735.5:  #755-19.5
            self.dx = -2

class Ghost2:
    def __init__(self, canvas, ghost):
        self.canvas = canvas
        self.id = canvas.create_image(500, 350, anchor = CENTER, image = ghost)
        move_dx = [-2,2]
        move_dy = [-2,2]
        rnd.shuffle(move_dx)
        rnd.shuffle(move_dy)
        self.dx = move_dx[0]
        self.dy = move_dy[0]
        self.pos_ghost2 = self.canvas.coords(self.id)
        self.make_area = False
    def draw(self):
        self.canvas.move(self.id, self.dx, self.dy)
        pos_ghost2 = self.canvas.coords(self.id)
        if pos_ghost2[1] <= 220:
            self.dy = 2
        if pos_ghost2[1] >= 538:
            self.dy = -2
        if pos_ghost2[0] <= 74.5:
            self.dx = 2
        if pos_ghost2[0] >= 735.5:
            self.dx = -2

class Knight:
    def __init__(self, canvas, player):
        self.canvas = canvas
        self.id = canvas.create_image(55, 220, anchor = CENTER, image=player)
        self.nw = (55, 200)
        self.sw = (55, 553)
        self.se = (749, 553)
        self.ne = (749, 200)
        self.dx = 0
        self.dy = 0
        self.hit_ghost = False
        self.canvas.bind_all("<KeyPress>", self.move)
    def move(self, event):
        self.event = event.keysym
        if self.event == "Left":
            self.dx = -2
            self.dy = 0
            self.canvas.move(self.id, self.dx, self.dy)
        elif self.event == "Right":
            self.dx = 2
            self.dy = 0
            self.canvas.move(self.id, self.dx, self.dy)
        elif self.event == "Up":
            self.dy = -2
            self.dx = 0
            self.canvas.move(self.id, self.dx, self.dy)
        elif self.event == "Down":
            self.dx = 0
            self.dy = 2
            self.canvas.move(self.id, self.dx, self.dy)
    def draw(self):
        self.node = self.canvas.coords(self.id)
        self.canvas.move(self.id, self.dx, self.dy)
        self.node_next = self.canvas.coords(self.id)
        line = self.canvas.create_line(self.node[0], self.node[1], self.node_next[0], self.node_next[1], fill="cyan", width=3)
        pos_knight = self.canvas.coords(self.id)
        if pos_knight[0] == 55:
            self.dx = 0
        elif pos_knight[0] <= 52:
            self.dx = 2
            canvas.itemconfig(line, fill="")
        if pos_knight[0] == 749:
            self.dx = 0
        elif pos_knight[0] >= 752:
            self.dx = -2
            canvas.itemconfig(line, fill="")
        if pos_knight[1] == 200:
            self.dy = 0
        elif pos_knight[1] <= 197:
            self.dy = 2
            canvas.itemconfig(line, fill="")
        elif pos_knight[1] == 553:
            self.dy = 0
        elif pos_knight[1] >= 556:
            self.dy = -2
            canvas.itemconfig(line, fill="")
        if distance(pos_knight, self.canvas.coords(ghost1.id)) <= 20*(2**0.5) or distance(pos_knight, self.canvas.coords(ghost2.id)) <= 20*(2**0.5):
            self.hit_ghost = True
            self.press_enter = self.canvas.create_text(400, 330, text="Press Enter", font=("Helvetica", 30, 'bold'))
    def game_chance(self, evt):
        self.canvas.delete(self.id)
        self.canvas.delete(self.press_enter)
        self.id = canvas.create_image(55, 200, anchor = CENTER, image=player)
        canvas.delete(life_list.pop())
        canvas.delete(stage)
        self.hit_ghost = False

## Object
ghost1 = Ghost1(canvas, ghost)
ghost2 = Ghost2(canvas, ghost)
knight = Knight(canvas, player)

## Execute
time = 30.00
while time>0:
    now = canvas.create_text(570, 95, anchor = NW, text = 'TIME  %0.2f'%(time), fill = 'white', font = ('Helvetica',20,'bold'))
    tt.sleep(0.01)
    if knight.hit_ghost == False:
        knight.draw()
        ghost1.draw()
        ghost2.draw()
        time -= 0.01
    else:
        knight.canvas.bind_all('<KeyPress-Return>', knight.game_chance)
    if life_list == []:
        canvas.create_text(400, 330, text="Game over", fill="orange", font=("Helvetica", 30, 'bold'))
        break
    tk.update_idletasks()
    tk.update()
    canvas.delete(now)




