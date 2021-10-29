import turtle
import random
import math
import os

class Lives(turtle.Turtle):
  FONT = ("Arial", 24, "normal")
  def __init__(self, lives):
    super().__init__()
    self.lives = lives
    self.color("red")
    self.hideturtle()
    self.penup()
    self.speed(0)
    self.goto(130, 160)
    self.lost_life()
  
  def lost_life(self):
    self.lives -= 1
    self.clear()
    self.write("Lives: " + str(self.lives), font=self.FONT)
    if self.lives == 0:
      quit()

lives = Lives(11)

screen = turtle.Screen()
screen.bgpic('bg.gif')

trajectories = [lambda x: 2.25*math.cos(x/25),
                lambda x: 0.0035*x,
                lambda x: 0.3,
                lambda x: (0.35*x)/abs(x),
                lambda x: 0]

class Crewmate(turtle.Turtle):
  def __init__(self, image):
    super().__init__()
    screen.addshape(image)
    self.shape(image)
    self.penup()
    self.speed(0)
    self.onclick(self.clicked)
    self.return_to_left()
  
  def return_to_left(self):
    self.dx = random.randint(10, 14)
    self.trajectory = random.choice(trajectories)
    self.hideturtle()
    yval = random.randint(-100, 100)
    self.goto(-266, yval)
    self.showturtle()
  
  def clicked(self, *args):
    self.return_to_left()
  
  def go_forward(self):
    x = self.xcor()+self.dx
    y = self.ycor()
    try:
      y += self.trajectory(x)*self.dx
    except ZeroDivisionError:
      pass
    self.goto(x, y)

    if x > 266:
      lives.lost_life()
      self.return_to_left()

crewmates = []
for filename in os.listdir():
    if not filename.startswith("bg") and filename.endswith(".gif"):
        crewmates.append(Crewmate(filename))

def game_loop():
  for crewmate in crewmates:
    crewmate.go_forward()
  turtle.ontimer(game_loop, t=1)

game_loop()
screen.mainloop()
