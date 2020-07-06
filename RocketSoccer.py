#https://py3.codeskulptor.org/#user305_sPRE0Yv6Iv_10.py

import simplegui
import math
import random

WIDTH = 800
HEIGHT = 500
BOARD_HEIGHT = 100
MARGIN = 10

FRICTION = 0.99
#The lower the friction constant is, the more quickly things will slow down
#if the constant is higher than 1, than the object will accelerate naturally

class RocketSoccer:
    """
    don't sue me psyonix
    """
    def __init__(self, o_car, b_car, ball):
        self.o_car = o_car
        self.b_car = b_car
        self.ball = ball
        self.playing = False;
        self.goal_height = 100
        
        self.orange_score = 0
        self.blue_score = 0
        
    def begin_playing(self, click = (0, 0)):
        self.playing = True
        
    def score_goal(self, team):
        if team == "Orange":
            self.orange_score += 1
        if team == "Blue":
            self.blue_score += 1
        self.reset()
       
    def reset(self):
        lis = [self.o_car, self.b_car, self.ball]
        for obj in lis:
            obj.set_vel([0, 0])
            obj.set_acc(0, 0)
            obj.set_acc(1, 0)
            
        self.ball.set_pos([WIDTH/2, HEIGHT/2])
        self.o_car.set_pos([WIDTH/4, HEIGHT*(0.1 + 0.8*random.random())])
        self.b_car.set_pos([3*WIDTH/4, 0.1 + 0.8*HEIGHT*random.random()])
    
        
    def draw(self, canvas):
        #draw the stadium
        canvas.draw_polygon([(0, 0), (WIDTH, 0), (WIDTH, HEIGHT), (0, HEIGHT)], MARGIN, "Green")
        canvas.draw_line((WIDTH/2, HEIGHT), (WIDTH/2, HEIGHT + BOARD_HEIGHT), MARGIN/2, "Green")
            
        #draw the goal
        canvas.draw_line((0, (HEIGHT - self.goal_height)/2), (0, (HEIGHT + self.goal_height)/2), MARGIN, "White")
        canvas.draw_line((WIDTH, (HEIGHT - self.goal_height)/2), (WIDTH, (HEIGHT + self.goal_height)/2), MARGIN, "White")
        
        #draw handler for canvas
        if self.playing:
            #orange car
            self.o_car.draw(canvas)
            self.o_car.update_pos()
            collide(self.o_car, self.ball)
            
            #blue car
            self.b_car.draw(canvas)
            self.b_car.update_pos()
            collide(self.b_car, self.ball)
            
            #ball physics
            self.ball.draw(canvas)
            #scoring calculations
            if self.ball.update_pos():
                if self.ball.get_pos()[1] > (HEIGHT-self.goal_height)/2 and self.ball.get_pos()[1] < (HEIGHT + self.goal_height)/2:
                    if self.ball.get_pos()[0] <= self.ball.get_radius() + MARGIN: self.score_goal("Blue")
                    else: self.score_goal("Orange")
                      
            #score
            os_width = frame.get_canvas_textwidth(str(self.orange_score), BOARD_HEIGHT*0.9)
            canvas.draw_text(str(self.orange_score), (WIDTH/2 - os_width-10, HEIGHT + BOARD_HEIGHT*0.9), BOARD_HEIGHT*0.9, "Orange")
            canvas.draw_text(str(self.blue_score), (WIDTH/2 + 10, HEIGHT + BOARD_HEIGHT*0.9), BOARD_HEIGHT*0.9, "Blue")
            
            
        else:
            #loading screen
            message = "Click to start"
            m_size = 60
            m_width = frame.get_canvas_textwidth(message, m_size)
            canvas.draw_text(message, ((WIDTH-m_width)/2, (HEIGHT)/2), m_size, "Red")
            
        #print(get_distance(ball, car))

class Object:
    """
    class Object
    Either the ball or a car
    has position, velocity, and acceleration, can bounce off of walls
    """
    def __init__(self, pos, vel, acc, mass, friction, radius, color):
        self.pos = list(pos)
        self.vel = [vel[0], vel[1]]
        self.acc = [acc[0], acc[1]]
        self.mass = mass
        self.friction = friction
        self.radius = radius;
        self.color = color
        self.horsepower = 0.6
    
    def get_pos(self):
        return self.pos
    
    def get_vel(self):
        return self.vel
    
    def get_mass(self):
        return self.mass
    
    def get_radius(self):
        return self.radius
    
    def update_pos(self):
        #returns true if the object bounces off one of the x-walls
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.vel[0] = self.friction*FRICTION*(self.vel[0] + self.acc[0])
        self.vel[1] = self.friction*FRICTION*(self.vel[1] + self.acc[1])
        
        output = False;
        if (self.pos[0] - MARGIN - self.radius) < 0: self.vel[0] = abs(self.vel[0]); output = True
        if (self.pos[0] + MARGIN + self.radius) > WIDTH: self.vel[0] = -abs(self.vel[0]); output = True
        if (self.pos[1] - MARGIN - self.radius) < 0: self.vel[1] = abs(self.vel[1])
        if (self.pos[1] + MARGIN + self.radius) > HEIGHT: self.vel[1] = -abs(self.vel[1]) 
        return output
    
    #setters (yes, I am aware how horrendously non-systemtimatic these are)
    def set_pos(self, new_pos):
        self.pos = new_pos
    
    def set_vel(self, new_vel):
        self.vel = new_vel
    
    def add_vel(self, axis, new_vel):
        self.vel[axis] += new_vel
        
    def reduce_vel(self, axis, percentage):
        self.vel[axis] *= percentage
    
    def set_acc(self, axis, sign):
        #0 for the x-axis, 1 for the y-axis
        self.acc[axis] = self.horsepower*sign
        
    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius-1, 1, self.color, self.color)


#Helper Functions
def get_distance(object1, object2):
    return math.sqrt((object1.get_pos()[0]-object2.get_pos()[0])**2 
                     + (object1.get_pos()[1]-object2.get_pos()[1])**2)

def collide(car, ball):
    if get_distance(car, ball) <= (car.get_radius() + ball.get_radius()):
        KICKBACK = 0.1
        car.reduce_vel(0, 1-KICKBACK); car.reduce_vel(1, 1-KICKBACK)
        ball.add_vel(0, car.get_mass()/ball.get_mass()*KICKBACK*car.get_vel()[0])
        ball.add_vel(1, car.get_mass()/ball.get_mass()*KICKBACK*car.get_vel()[1])
            
def keydown(key):
    if key == simplegui.KEY_MAP['w']:
        o_car.set_acc(1, -1)
    elif key == simplegui.KEY_MAP['s']:
        o_car.set_acc(1, 1)
    elif key == simplegui.KEY_MAP['a']:
        o_car.set_acc(0, -1)
    elif key == simplegui.KEY_MAP['d']:
        o_car.set_acc(0, 1)
        
    if key == simplegui.KEY_MAP['up']:
        b_car.set_acc(1, -1)
    elif key == simplegui.KEY_MAP['down']:
        b_car.set_acc(1, 1)
    elif key == simplegui.KEY_MAP['left']:
        b_car.set_acc(0, -1)
    elif key == simplegui.KEY_MAP['right']:
        b_car.set_acc(0, 1)
        
def keyup(key):
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        o_car.set_acc(1, 0)
    elif key == simplegui.KEY_MAP['a'] or key == simplegui.KEY_MAP['d']:
        o_car.set_acc(0, 0)
        
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        b_car.set_acc(1, 0)
    elif key == simplegui.KEY_MAP['left'] or key == simplegui.KEY_MAP['right']:
        b_car.set_acc(0, 0)

        
#create everything
o_car = Object([WIDTH/4, HEIGHT/2], (0, 0), (0, 0), 20, 0.92, 12, "Orange")
b_car = Object([3*WIDTH/4, HEIGHT/2], (0, 0), (0, 0), 20, 0.92, 12, "Blue")
ball = Object([WIDTH/2, HEIGHT/2], (0, 0), (0, 0), 1, 0.98, 10, "White")

game = RocketSoccer(o_car, b_car, ball)
game.reset()

#create canvas
frame = simplegui.create_frame('Frame', WIDTH, HEIGHT + BOARD_HEIGHT)
frame.set_draw_handler(game.draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(game.begin_playing)

#run program
frame.start()
