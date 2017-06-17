### June 6 2016
### Team1 Final Project
### Version 1


from tkinter import *
import random
import time


### Main Part 주실행부
class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.resizable(0,0)
        self.tk.wm_attributes("-topmost",1)
        self.canvas = Canvas(self.tk, width=650, height=650, highlightthickness=0)
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 650
        self.canvas_width = 650
        self.bg = PhotoImage(file="Background.gif")
        self.background = self.canvas.create_image(0,0, anchor='nw', image=self.bg)
        self.sprites = []        # sprites: 발판(platform)과 토끼(Figure)가 있는 list
        self.running = True     # running = True 실행
        # design oo the right side
        self.title1 = self.canvas.create_text(550,70, text="Game", font=("Helvetica", 20,"bold"), fill="Blue")
        self.title2 = self.canvas.create_text(500, 300, text="Score", font=("Helvetica", 20, "bold"))
        self.score = self.canvas.create_text(580, 300, text=0, font=("Helvetica", 20))
        self.point = 0     # score
        self.y_list = []
    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)



### Coords: 좌표 반환 class
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

### Function used for class
## 토끼와 발판이 수평으로 겹치는 것을 감지(co1, co2)
## Check if x coordinates of rabbit are in the range of positon of platform
def within_x(co1, co2):
    if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
            or (co1.x2 > co2.x1 and co1.x2 < co2.x2):
            # or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
            # or (co2.x2 > co1.x1 and co2.x2 < co1.x1):
        return True
    else:
        return False

## 토끼와 발판이 수직으로 겹치는 것을 감지(co1, co2)
## Check if y coordinates of rabbit are in the range of postion of platform
def within_y(co1, co2):
    if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
            or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
            or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
            or (co2.y2 > co1.y1 and co2.y2 < co1.y1):
        return True
    else:
        return False

## 토끼가 발판에 닿는 것을 감지(co1, co2)
## Check if rabbit falls on the platform
def collided_bottom(co1,co2):
    if within_x(co1,co2):
        if co1.y2 >= co2.y1 and co1.y2 <= co2.y2:
            return True
    return False

### Main Objects
## class for inheriting to the figure and platform class
class Sprite:
    def __init__(self, game):
        self.game = game
        self.coordinates = None
    def move(self):
        pass
    def coords(self):
        return self.coordinates

## Platform class
class Platform(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor="nw")
        self.coordinates = Coords(x, y, x+width, y + height)     # Find the coordinate of platform when occuring


## Figure(Rabbit, Design) class
file_list = [["platform1.gif",100], ["platform2.gif",60]]
score = 0
class Figure(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_right = [PhotoImage(file="figure1_fix.gif"), PhotoImage(file="figure2_fix.gif")]    # picture for right movement: normal, jumping
        self.images_left = [PhotoImage(file="figure3_fix.gif"), PhotoImage(file="figure4_fix.gif")]     # picture for left movement: normal, jumping
        self.image = game.canvas.create_image(40, 463, image=self.images_left[0], anchor="nw")     # Start Point
        self.x = 0    # movement
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()    # Find the coordinate of figure when moving
        game.canvas.bind_all("<KeyPress>", self.keymove)
    def keymove(self, event):    # keys for moving and jumping rabbit
        if event.keysym == "Left":
            self.x = -3
        elif event.keysym == "Right":
            self.x = 3
        elif event.keysym == "space":
            if self.y == 0:
                self.y = -10
                self.jump_count = 0
    def animate(self):    # animation part: change picture of rabbit when moving at every 0.1 sec
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 1:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:    # when rabbit jumps, a picture for jumping is only used.
                self.game.canvas.itemconfig(self.image, image=self.images_left[1])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x >0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[1])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])
    def coords(self):   # get the four coordinates of rabbit
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + 55
        self.coordinates.y2 = xy[1] + 47
        return self.coordinates
    def move(self):     # Main movement in every loop
        self.animate()
        if self.y < 0:    # control jumping: when rabbit jumps, jump_count increases to 20.
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 5
        if self.y > 0:    # when rabbit reach the maximum height(count 20), jump_count decreases until it falls on the platform
            self.jump_count -= 1
        co = self.coords()    # current coordinate of rabbit
        left = True
        right = True
        falling = True
        if self.x > 0 and co.x2 >= 450:    # stop rabbit when rabbit cross the right edge.
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:    # stop rabbit when rabbit cross the left edge.
            self.x = 0
            left = False
        for sprite in self.game.sprites:    ## control movement of rabbit
            if sprite == self:    ## sprite passes when it is rabbit.
                continue
            sprite_co = sprite.coords()     ## coordinate of platform
            if self.y > 0 and collided_bottom(co, sprite_co):    # when rabbit falls on the platform, it jumps
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:     # when rabbit reaches the highest point, it falls (refer to below)
                    self.y = 0
            if falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(co, sprite_co) \
                    and (co.x1 >= sprite_co.x1 or co.x2 <= sprite_co.x2):
                falling = False    # When there is any platform below rabbit, it falls until it reaches the platform. (falling -> False)
        if falling and self.y == 0 and co.y2 < self.game.canvas_height:    # When there is no platform below rabbit, it falls until it reaches the ground
            self.y = 5
        if co.y2 >= self.game.canvas_height:  # When rabbit reaches the ground, game stops and 'game over pop up'
            self.y = 0
            self.x = 0
            self.game.canvas.create_text(250, 350, text="Game Over", font=("Helvetica", 20, "bold"), fill="red")
            self.game.running = False
        self.game.canvas.move(self.image, self.x, self.y)

        if self.game.canvas.coords(self.image)[1] <= 300:   ## when rabbit reaches the half of screen, all objects go down
            self.game.canvas.move(ALL, 0, 20)
            if self.game.canvas.coords(self.image)[1] >= 313:    ## score increaes 10 points every time screen moves
                self.game.point += 10
                self.game.canvas.itemconfig(self.game.score, text=self.game.point)
            self.game.canvas.move(self.game.background, 0, -20)
            self.game.canvas.move(self.game.title1, 0, -20)
            self.game.canvas.move(self.game.title2, 0, -20)
            self.game.canvas.move(self.game.score, 0, -20)
            for i in range(len(self.game.sprites)):   ## change coordinate of objects when screen moves
                if self.game.sprites[i] == self:
                    continue
                self.game.canvas.move(self.game.sprites[i], 0, -20)
                sprites_co = self.game.sprites[i].coords()
                sprites_co.y1 += 20
                sprites_co.y2 += 20
                self.game.y_list.append(sprites_co.y1)
                r = random.randint(0,1)
            if time.time()-self.last_time > 0.27:    # new platform occurs from above when screen moves in constant interval
                y_top = self.game.sprites[-1].coords().y1
                platform_new = Platform(g, PhotoImage(file=file_list[r][0]), random.randint(0,340), 0, file_list[r][1], 10)
                self.game.sprites.append(platform_new)


g = Game()
platform1 = Platform(g, PhotoImage(file="platform1.gif"), 40,560, 100, 10)
platform2 = Platform(g, PhotoImage(file="platform2.gif"), 300,500, 60, 10)
platform3 = Platform(g, PhotoImage(file="platform1.gif"), 100, 430, 100, 10)
platform4 = Platform(g, PhotoImage(file="platform1.gif"), 160, 300, 100, 10)
platform5 = Platform(g, PhotoImage(file="platform2.gif"), 300, 240, 60, 10)
platform6 = Platform(g, PhotoImage(file="platform1.gif"), 70, 170, 100, 10)
platform7 = Platform(g, PhotoImage(file="platform2.gif"), 250, 100, 60, 10)
platform8 = Platform(g, PhotoImage(file="platform1.gif"), 20, 40, 100, 10)


g.sprites.append(platform1)
g.sprites.append(platform2)
g.sprites.append(platform3)
g.sprites.append(platform4)
g.sprites.append(platform5)
g.sprites.append(platform6)
g.sprites.append(platform7)
g.sprites.append(platform8)

sf = Figure(g)
g.sprites.append(sf)
g.mainloop()

