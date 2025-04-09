import pgzrun
import random

WIDTH=800
HEIGHT=600
balls=[]

def draw():
    screen.fill('white')
    for ball in balls:
        screen.draw.filled_circle((ball[0], ball[1]),ball[4], (ball[5], ball[6], ball[7]))
        for x in range(1,ball[4],3):
            screen.draw.filled_circle((ball[0],ball[1]), ball[4]-x, (random.randint(ball[5],255), random.randint(ball[6],255),random.randint(ball[7], 255)))

def update():
    for ball in balls:
        ball[0]=ball[0] + ball[2]
        ball[1]=ball[1] + ball[3]
        if ball[0]>WIDTH-ball[4]or ball[0]<ball[4]:
            ball[2]=-ball[2]
        if ball[1]>HEIGHT-ball[4] or ball[1]<ball[4]:#当小球碰到上下边界时,y方向速度反转
            ball[3]= -ball[3]

def on_mouse_move(pos,rel, buttons):
    if mouse.LEFT in buttons:
        x=pos[0]
        y=pos[1]
        speed_x= random.randint(1,5)
        speed_y= random.randint(1,5)
        r= random.randint(5,50)
        colorR = random.randint(10,255)
        colorG = random.randint(10, 255)
        colorB=random.randint(10,255)
        ball=[x,y,speed_x,speed_y,r,colorR, colorG,colorB]
        balls.append(ball)

pgzrun.go()
