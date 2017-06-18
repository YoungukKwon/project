### June 16 2017
### Team1 Final Project
### Version 3


from tkinter import *
import random
import time


# Main Part
class Game:
    def __init__(self):
        self.tk = Tk()
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas = Canvas(self.tk, width=650, height=650, highlightthickness=0, background="#F0F8FF")
        self.canvas.pack()
        self.tk.update()
        self.canvas_height = 650     # Size of Canvas
        self.canvas_width = 650
        self.bg = PhotoImage(file="Background.gif")
        self.background = self.canvas.create_image(0, 0, anchor='nw', image=self.bg)
        self.sprites = []  # sprites: 발판(platform)과 토끼(Figure)가 있는 list
        self.running = True  # execute if running == True
        # design on the right side
        self.title = PhotoImage(file="title.gif")
        self.TITLE = self.canvas.create_image(500, 0, anchor='nw', image=self.title)
        self.rabbit = PhotoImage(file="rabbit.gif")
        self.RABBIT = self.canvas.create_image(500, 80, anchor='nw', image=self.rabbit)
        self.score = self.canvas.create_text(550, 235, text=0, font=("Helvetica", 15))
        self.Score = PhotoImage(file="score.gif")
        self.SCORE = self.canvas.create_image(478, 170, anchor='nw', image=self.Score)
        self.tips = PhotoImage(file="tips.gif")
        self.TIPS = self.canvas.create_image(480, 350, anchor='nw', image=self.tips)
        self.Tip = PhotoImage(file="Tip.gif")
        self.TIP = self.canvas.create_image(460, 400, anchor='nw', image=self.Tip)
        self.control = PhotoImage(file="control.gif")
        self.CONTROL = self.canvas.create_image(475, 545, anchor='nw', image=self.control)
        self.left = PhotoImage(file="left.gif")
        self.LEFT = self.canvas.create_image(455, 585, anchor='nw', image=self.left)
        self.right = PhotoImage(file="right.gif")
        self.RIGHT = self.canvas.create_image(500, 585, anchor='nw', image=self.right)
        self.space = PhotoImage(file="space.gif")
        self.SPACE = self.canvas.create_image(553, 588, anchor='nw', image=self.space)
        # score and record
        self.point = 0  # score
        self.highest_point = 0    # highest score player gets
        self.record = self.canvas.create_text(550, 320, text=self.highest_point,
                                              font=("Helvetica", 15, "bold"))
        self.next_y = 0
        self.gameover = self.canvas.create_text(250, 350, text="Game Over", font=("Helvetica", 20, "bold"), fill="red",
                                                state=HIDDEN)
        self.MAX = PhotoImage(file="maxscore.gif")
        self.max = self.canvas.create_image(478, 250, anchor='nw', image=self.MAX)

    def mainloop(self):     # mainloop
        while 1:
            if self.running:
                for sprite in self.sprites:        # sprite: platform, rabbit(figure)
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            time.sleep(0.01)


# Coordinate class: get coordinates of sprite
class Coords:
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


# Function used for class
# Check if x coordinates of rabbit are in the range of positon of platform
def within_x(co1, co2):
    if (co2.x1 < co1.x1 < co2.x2) \
            or (co2.x1 < co1.x2 < co2.x2):
        return True
    else:
        return False


# Check if y coordinates of rabbit are in the range of position of platform
def within_y(co1, co2):
    if (co2.y1 < co1.y1 < co2.y2) \
            or (co2.y1 < co1.y2 < co2.y2) \
            or (co1.y1 < co2.y1 < co1.y2) \
            or (co2.y2 < co1.y1 < co2.y2):
        return True
    else:
        return False


# Check if rabbit falls on the platform
def collided_bottom(co1, co2):
    if within_x(co1, co2):
        if co2.y1 <= co1.y2 <= co2.y2:
            return True
    return False


# Main Objects
# class for inheriting to the figure and platform class
class Sprite:
    def __init__(self, game):
        self.game = game
        self.coordinates = None

    def move(self):
        pass

    def coords(self):
        return self.coordinates


# Platform class
# Platformtype: normal, jumping, shifting, fragile
class Platform(Sprite):
    def __init__(self, game, photo_image, x, y, width, height, platformtype):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.platformtype = platformtype
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor="nw")
        self.coordinates = Coords(x, y, x + width, y + height)  # Find the coordinate of platform when occurring


# Shifting(moving) Platform
class ShiftingPlatform(Platform):
    def __init__(self, game, photo_image, x, y, width, height, platformtype):
        Platform.__init__(self, game, photo_image, x, y, width, height, platformtype)
        self.x = 3  # speed of shifting platform
        self.last_time = time.time()
        self.width = width
        self.height = height

    def coords(self):  # get the coordinate of shifting block every time
        xy = self.game.canvas.coords(self.image)
        self.coordinates.x1 = xy[0]
        self.coordinates.y1 = xy[1]
        self.coordinates.x2 = xy[0] + self.width
        self.coordinates.y2 = xy[1] + self.height
        return self.coordinates

    def move(self):
        if time.time() - self.last_time > 0.03:  # if time passes for 0.03s, move block(animation)
            self.last_time = time.time()
            self.game.canvas.move(self.image, self.x, 0)
            co = self.coords()
            if co.x2 >= 450 or co.x1 <= 0:  # if shifting block reached the side edge, change direction
                self.x = self.x * (-1)


# Figure(Rabbit, Design, next platform) class
class Figure(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.co = None
        self.images_right = [PhotoImage(file="figure1_fix.gif"),
                             PhotoImage(file="figure2_fix.gif")]  # picture for right movement: normal, jumping
        self.images_left = [PhotoImage(file="figure3_fix.gif"),
                            PhotoImage(file="figure4_fix.gif")]  # picture for left movement: normal, jumping
        self.image = game.canvas.create_image(40, 463, image=self.images_left[0], anchor="nw")  # Start Point
        self.message = game.canvas.create_text(250, 300, text="Start!", font=("Helvetica", 20, "bold"),
                                               fill='blue')
        self.x = 0  # movement
        self.y = 0
        self.current_image = 0
        self.current_image_add = 1
        self.jump_count = 0
        self.side_count = 0
        self.last_time = time.time()
        self.coordinates = Coords()  # Find the coordinate of figure when moving
        game.canvas.bind_all("<KeyPress>", self.keymove)

    def keymove(self, event):  # keys for moving and jumping rabbit
        if event.keysym == "Left":
            self.x = -4
            self.game.canvas.delete(self.message)
        elif event.keysym == "Right":
            self.x = 4
            self.game.canvas.delete(self.message)
        elif event.keysym == "space":
            if self.y == 0:
                self.y = -10
                self.jump_count = 0
                self.game.canvas.delete(self.message)

    def animate(self):  # animation part: change picture of rabbit when moving at every 0.1 sec
        if self.x != 0 and self.y == 0:
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 1:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:  # when rabbit jumps, a picture for jumping is only used.
                self.game.canvas.itemconfig(self.image, image=self.images_left[1])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:
                self.game.canvas.itemconfig(self.image, image=self.images_right[1])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

    def coords(self):
        pos = self.game.canvas.coords(self.image)
        self.coordinates.x1 = pos[0]
        self.coordinates.y1 = pos[1]
        self.coordinates.x2 = pos[0] + 55
        self.coordinates.y2 = pos[1] + 47
        return self.coordinates

    def move(self):  # Main movement in every loop
        self.animate()
        if self.y < 0:  # control jumping: when rabbit jumps, jump_count increases to 20.
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 5
        if self.y > 0:  # when rabbit reach the maximum height(count 20), jump_count decreases until it falls on the platform
            self.jump_count -= 1
        co = self.coords()  # current coordinate of rabbit
        falling = True
        if self.x > 0 and co.x2 >= 450:  # stop rabbit when rabbit cross the right edge.
            self.x = 0
        elif self.x < 0 and co.x1 <= 0:  # stop rabbit when rabbit cross the left edge.
            self.x = 0
        for sprite in self.game.sprites:  # control movement of rabbit
            if sprite == self:  # sprite passes when it is rabbit.
                continue
            sprite_co = sprite.coords()  # coordinate of platform
            if sprite_co.y2 > 650 or sprite_co.y2 < 0:
                if sprite_co.y2 > 650:
                    del self.game.sprites[self.game.sprites.index(sprite)]
                continue
            if self.y > 0 and collided_bottom(co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
            if falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(co, sprite_co) \
                    and (co.x1 >= sprite_co.x1 or co.x2 <= sprite_co.x2):
                falling = False  # When there is any platform below rabbit, it falls until it reaches the platform. (falling -> False)
                self.jump_count = 0
                if sprite.platformtype == "Jumping":
                    self.y = -20
                elif sprite.platformtype == "Fragile":
                    self.y = -10
                    self.game.canvas.delete(sprite.image)
                    falling = True
        if falling and self.y == 0 and co.y2 < self.game.canvas_height:  # When there is no platform below rabbit, it falls until it reaches the ground
            self.y = 5
        if co.y2 >= self.game.canvas_height:  # When rabbit reaches the ground, game stops and 'game over pop up'
            self.y = 0
            self.x = 0
            self.chance()
        self.game.canvas.move(self.image, self.x, self.y)
        if self.game.canvas.coords(self.image)[1] <= 300:  # when rabbit reaches the half of screen, all objects go down
            self.game.canvas.move(ALL, 0, 20)
            self.game.point += 10  # score increaes 10 points every time screen moves
            self.game.canvas.itemconfig(self.game.score, text=self.game.point)
            self.game.canvas.move(self.game.background, 0, -20)
            self.game.canvas.move(self.game.TITLE, 0, -20)
            self.game.canvas.move(self.game.RABBIT, 0, -20)
            self.game.canvas.move(self.game.score, 0, -20)
            self.game.canvas.move(self.game.SCORE, 0, -20)
            self.game.canvas.move(self.game.TIPS, 0, -20)
            self.game.canvas.move(self.game.TIP, 0, -20)
            self.game.canvas.move(self.game.CONTROL, 0, -20)
            self.game.canvas.move(self.game.LEFT, 0, -20)
            self.game.canvas.move(self.game.RIGHT, 0, -20)
            self.game.canvas.move(self.game.SPACE, 0, -20)
            self.game.canvas.move(self.game.record, 0, -20)
            self.game.canvas.move(self.game.gameover, 0, -20)
            self.game.canvas.move(self.game.max, 0, -20)
            for i in range(len(self.game.sprites)):  # change coordinate of objects when screen moves
                if self.game.sprites[i] == self:
                    continue
                self.game.canvas.move(self.game.sprites[i], 0, -20)
                sprites_co = self.game.sprites[i].coords()
                sprites_co.y1 += 20
                sprites_co.y2 += 20
            r = random.randint(1, 10)
            if time.time() - self.last_time > 0.2:  # new platform occurs from above when screen moves in constant interval
                if r <= 5:
                    platform_new = Platform(g, PhotoImage(file="platform1.gif"), random.randint(0, 340),
                                            self.game.next_y, 100, 10, "Normal")
                    self.game.sprites.append(platform_new)
                elif 6 <= r <= 7:
                    platform_new = Platform(g, PhotoImage(file="platform2.gif"), random.randint(0, 340),
                                            self.game.next_y, 100, 10, "Jumping")
                    self.game.sprites.append(platform_new)
                elif 8 <= r <= 9:
                    platform_new = ShiftingPlatform(g, PhotoImage(file="platform3.gif"), random.randint(0, 340),
                                                    self.game.next_y, 100, 10, "Shifting")
                    self.game.sprites.append(platform_new)
                else:
                    platform_new = Platform(g, PhotoImage(file="platform4.gif"), random.randint(0, 340),
                                            self.game.next_y, 100, 10, "Fragile")
                    self.game.sprites.append(platform_new)
                self.game.next_y -= random.randint(40, 60)
        if self.game.point >= self.game.highest_point:
            self.game.canvas.delete(self.game.record)
            self.game.highest_point = self.game.point
            self.game.record = self.game.canvas.create_text(550, 317, text=self.game.highest_point,
                                                            font=("Helvetica", 15, "bold"))

    def chance(self):
        self.game.canvas.itemconfig(self.game.gameover, state=NORMAL)
        self.game.running = False
        self.game.canvas.bind_all('<KeyPress-Return>', self.restart)

    def restart(self, event):
        if self.game.running == False and self.game.canvas.coords(self.image)[1] + 47 >= self.game.canvas_height:
            self.game.canvas.itemconfig(self.game.gameover, state=HIDDEN)
            self.game.canvas.delete(self.image)
            self.game.canvas.delete(self.message)
            self.game.canvas.delete(self.game.score)
            self.game.score = self.game.canvas.create_text(550, 235, text=0, font=("Helvetica", 15))
            self.game.sprites.clear()
            self.game.point = 0  # score
            self.game.next_y = 0
            self.game.running = True
            initial_setting(g)
        else:
            pass


def initial_setting(g):
    # platform initial location
    platform1 = Platform(g, PhotoImage(file="platform1.gif"), 40, 560, 100, 10, "Normal")
    platform2 = Platform(g, PhotoImage(file="platform1.gif"), 300, 500, 100, 10, "Normal")
    platform3 = Platform(g, PhotoImage(file="platform1.gif"), 100, 430, 100, 10, "Normal")
    platform4 = Platform(g, PhotoImage(file="platform1.gif"), 160, 300, 100, 10, "Normal")
    platform5 = Platform(g, PhotoImage(file="platform1.gif"), 300, 240, 100, 10, "Normal")
    platform6 = Platform(g, PhotoImage(file="platform2.gif"), 70, 170, 100, 10, "Jumping")
    platform7 = Platform(g, PhotoImage(file="platform1.gif"), 250, 100, 100, 10, "Normal")
    platform8 = Platform(g, PhotoImage(file="platform1.gif"), 20, 40, 100, 10, "Normal")

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


g = Game()
initial_setting(g)
g.mainloop()
