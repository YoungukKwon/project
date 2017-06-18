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
        self.escape = self.canvas.create_text(590, 640, text="Exit game: Esc", font=("Helvetica", 10, "bold"))
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
# Check if x coordinates of rabbit are in the range of position of platform
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

    def move(self):     # move method: main running method
        pass

    def coords(self):   # coords method: return coordinate of sprites
        return self.coordinates


# Platform class
# Platformtype: normal, jumping, shifting, fragile
# all platform have 100 width, 10 height
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

    def coords(self):  # get the coordinate of shifting platform every time
        pos = self.game.canvas.coords(self.image)
        self.coordinates.x1 = pos[0]
        self.coordinates.y1 = pos[1]
        self.coordinates.x2 = pos[0] + self.width
        self.coordinates.y2 = pos[1] + self.height
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
                                               fill='blue')    # Start message when game starts
        self.x = 0  # movement
        self.y = 0
        self.current_image = 0     # variable used to control animation
        self.current_image_add = 1
        self.jump_count = 0       # variable used to fall when rabbit reach the highest height
        self.last_time = time.time()
        self.coordinates = Coords()  # Find the coordinate of figure when moving
        game.canvas.bind_all("<KeyPress>", self.keymove)

    def keymove(self, event):  # method for moving and jumping rabbit using keyboard
        if event.keysym == "Left":     # go left
            self.x = -4
            self.game.canvas.delete(self.message)    # game starts right after player press keys in start message
        elif event.keysym == "Right":     # go right
            self.x = 4
            self.game.canvas.delete(self.message)     # game starts right after player press keys in start message
        elif event.keysym == "space":     # jumping
            if self.y == 0:
                self.y = -10
                self.jump_count = 0
                self.game.canvas.delete(self.message)      # game starts right after player press keys in start message
        elif event.keysym == "Escape":     # exit the game if player presses esc key
            self.game.tk.destroy()

    def animate(self):  # method for animation: change picture of rabbit when it moves or jumps
        if self.x != 0 and self.y == 0:      # when rabbit moves to right or left, static picture changes to picture for running
            if time.time() - self.last_time > 0.1:
                self.last_time = time.time()
                self.current_image += self.current_image_add
                if self.current_image >= 1:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
        if self.x < 0:
            if self.y != 0:  # when rabbit jumps and goes left, a picture for left jumping is only used.
                self.game.canvas.itemconfig(self.image, image=self.images_left[1])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_left[self.current_image])
        elif self.x > 0:
            if self.y != 0:   # when rabbit jumps and goes left, a picture for right jumping is only used.
                self.game.canvas.itemconfig(self.image, image=self.images_right[1])
            else:
                self.game.canvas.itemconfig(self.image, image=self.images_right[self.current_image])

    def coords(self):     # method for getting the current coordinate of rabbit
        pos = self.game.canvas.coords(self.image)
        self.coordinates.x1 = pos[0]
        self.coordinates.y1 = pos[1]
        self.coordinates.x2 = pos[0] + 55
        self.coordinates.y2 = pos[1] + 47
        return self.coordinates

    def move(self):  # Main playing method in every loop
        self.animate()
        if self.y < 0:  # control jumping: when rabbit jumps, jump_count increases to 20.
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 5
        if self.y > 0:  # when rabbit reach the maximum height(count 20), jump_count decreases until it falls on the platform
            self.jump_count -= 1
        co = self.coords()  # call coords method
        falling = True    # when rabbit falls, falling variable is True
        if self.x > 0 and co.x2 >= 450:  # stop rabbit when rabbit reaches the right edge.
            self.x = 0
        elif self.x < 0 and co.x1 <= 0:  # stop rabbit when rabbit reaches the left edge.
            self.x = 0
        for sprite in self.game.sprites:  # control movement of rabbit
            if sprite == self:  # sprite passes when it is rabbit.
                continue
            sprite_co = sprite.coords()  # call coords method of platform to get the coordinate of platform
            if sprite_co.y2 > 650 or sprite_co.y2 < 0:      # If a platform is not on the current screen, loop continues. It increases the speed
                if sprite_co.y2 > 650:    # If a platform is below the screen as rabbit goes up, delete the platform from sprite list
                    del self.game.sprites[self.game.sprites.index(sprite)]
                continue
            if self.y > 0 and collided_bottom(co, sprite_co):     # when rabbit is on the platform, it halts
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                    self.y = 0
            if falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(co, sprite_co) \
                    and (co.x1 >= sprite_co.x1 or co.x2 <= sprite_co.x2):
                falling = False  # After checking if rabbit is on the platform, falling variable turns to False
                self.jump_count = 0
                if sprite.platformtype == "Jumping":    # If rabbit is on the jumping platform, make rabbit jump
                    self.y = -20
                elif sprite.platformtype == "Fragile":   # If rabbit is on the Fragile platform, make it disappear and rabbit fall
                    self.y = -10
                    self.game.canvas.delete(sprite.image)
                    falling = True
        if falling and self.y == 0 and co.y2 < self.game.canvas_height:  # When there is no platform below rabbit, it falls until it reaches the ground
            self.y = 5
        if co.y2 >= self.game.canvas_height:  # When rabbit reaches the ground, game stops and go to chance method
            self.y = 0
            self.x = 0
            self.chance()
        self.game.canvas.move(self.image, self.x, self.y)    # return to start position when game restarts
        if self.game.canvas.coords(self.image)[1] <= 300:  # when rabbit reaches the half of screen, screen goes down for 20 pix and all objects goes up 20 pix.
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
            self.game.canvas.move(self.game.escape, 0, -20)
            for i in range(len(self.game.sprites)):  # change the coordinate of objects when screen moves
                if self.game.sprites[i] == self:
                    continue
                self.game.canvas.move(self.game.sprites[i], 0, -20)
                sprite_change_co = self.game.sprites[i].coords()
                sprite_change_co.y1 += 20
                sprite_change_co.y2 += 20
            r = random.randint(1, 10)
            if time.time() - self.last_time > 0.2:  # new platform occurs from above when screen moves in constant interval
                if r <= 5:     # normal platform appears by 50%
                    platform_new = Platform(g, PhotoImage(file="platform1.gif"), random.randint(0, 340),
                                            self.game.next_y, 100, 10, "Normal")
                    self.game.sprites.append(platform_new)
                elif 6 <= r <= 7:   # shifting platform appears by 20%
                    platform_new = Platform(g, PhotoImage(file="platform2.gif"), random.randint(0, 340),
                                            self.game.next_y, 100, 10, "Jumping")
                    self.game.sprites.append(platform_new)
                elif 8 <= r <= 9:    # jumping platform appears by 20%
                    platform_new = ShiftingPlatform(g, PhotoImage(file="platform3.gif"), random.randint(0, 340),
                                                    self.game.next_y, 100, 10, "Shifting")
                    self.game.sprites.append(platform_new)
                else:     # fragile platform appears by 10%
                    platform_new = Platform(g, PhotoImage(file="platform4.gif"), random.randint(0, 340),
                                            self.game.next_y, 100, 10, "Fragile")
                    self.game.sprites.append(platform_new)
                self.game.next_y -= random.randint(40, 60)     # randomly locate x-coordinate of next platforms
        if self.game.point >= self.game.highest_point:     # renew the highest score if player gets more higher score than previous
            self.game.canvas.delete(self.game.record)
            self.game.highest_point = self.game.point
            self.game.record = self.game.canvas.create_text(550, 317, text=self.game.highest_point,
                                                            font=("Helvetica", 15, "bold"))

    def chance(self):     # method for restart game after game over
        self.game.canvas.itemconfig(self.game.gameover, state=NORMAL)
        self.game.running = False
        self.game.canvas.bind_all('<KeyPress-Return>', self.restart)      # press enter when you want to regame

    def restart(self, event):     # restart game after gameover
        if self.game.running == False and self.game.canvas.coords(self.image)[1] + 47 >= self.game.canvas_height:
            self.game.canvas.itemconfig(self.game.gameover, state=HIDDEN)    # show gameover message
            self.game.canvas.delete(self.image)
            self.game.canvas.delete(self.message)
            self.game.canvas.delete(self.game.score)
            self.game.score = self.game.canvas.create_text(550, 235, text=0, font=("Helvetica", 15))    # save the previous score
            self.game.sprites.clear()
            self.game.point = 0  # score
            self.game.next_y = 0
            self.game.running = True
            initial_setting(g)    # go to the start point
        else:
            pass


def initial_setting(g):
    # initial location of platforms
    platform1 = Platform(g, PhotoImage(file="platform1.gif"), 40, 560, 100, 10, "Normal")
    platform2 = Platform(g, PhotoImage(file="platform1.gif"), 300, 500, 100, 10, "Normal")
    platform3 = Platform(g, PhotoImage(file="platform1.gif"), 100, 430, 100, 10, "Normal")
    platform4 = Platform(g, PhotoImage(file="platform1.gif"), 160, 300, 100, 10, "Normal")
    platform5 = Platform(g, PhotoImage(file="platform1.gif"), 300, 240, 100, 10, "Normal")
    platform6 = Platform(g, PhotoImage(file="platform2.gif"), 70, 170, 100, 10, "Jumping")
    platform7 = Platform(g, PhotoImage(file="platform1.gif"), 250, 100, 100, 10, "Normal")
    platform8 = Platform(g, PhotoImage(file="platform1.gif"), 20, 40, 100, 10, "Normal")

    g.sprites.append(platform1)     # Sprite list contains platforms and rabbit
    g.sprites.append(platform2)
    g.sprites.append(platform3)
    g.sprites.append(platform4)
    g.sprites.append(platform5)
    g.sprites.append(platform6)
    g.sprites.append(platform7)
    g.sprites.append(platform8)

    sf = Figure(g)       # rabbit
    g.sprites.append(sf)


# execute
g = Game()
initial_setting(g)
g.mainloop()
