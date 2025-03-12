import pgzrun
import random
import math

WIDTH = 600
HEIGHT = 600

ball = Actor('ball3.png',(100,100))

def draw():
    screen.fill((255,255,255))
    ball.draw()

r = 25
ball.angle = random.randint(0,360)
v = 10

def update():
    if ball.x < r or ball.x > WIDTH - r:
        ball.angle = 180 - ball.angle
    if ball.y < r or ball.y > HEIGHT - r:
        ball.angle = -ball.angle
    ball.x += v * math.cos(math.radians(ball.angle))
    ball.y += v * math.sin(math.radians(ball.angle))

pgzrun.go()