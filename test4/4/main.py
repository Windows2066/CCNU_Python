import pgzrun
import random

WIDTH = 350
HEIGHT = 600

background = "background"
bar_up = "bar_up"
bar_down = "bar_down"
bird_image = "bird"

bird = Actor(bird_image, (100, 250))
bird.velocity = 0
g = 0.5     # 降低重力值
fs = -10  # 跳跃强度
bars = []
score = 0
flag = False
gap = 200  # 柱子之间的间隙大小
passed = set()  # 用于跟踪已通过的柱子

def draw():
    # 清除屏幕，防止拖影
    screen.clear()
    screen.blit(background, (0, 0))
    
    for bar in bars:
        bar.draw()
    
    bird.draw()
    screen.draw.text(f'Score: {int(score)}', topleft=(10, 10), fontsize=30, color="white")
    
    if flag:
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2), fontsize=60, color="red")
        screen.draw.text("Press R to restart", center=(WIDTH//2, HEIGHT//2 + 60), fontsize=30, color="white")

def update():
    global flag, score
    
    if not flag:
        bird.velocity += g
        bird.y += bird.velocity
        
        for bar in bars:
            bar.x -= 3
            
            if "up" in bar.image and 95 <= bar.x <= 98 and bar not in passed:
                passed.add(bar)
                score += 1
            
            if bar.x < -50:
                if bar in passed:
                    passed.remove(bar)
                bars.remove(bar)
                
                if len(bars) <= 2:
                    add_bar()
            
            if bird.colliderect(bar):
                flag = True
        
        if bird.y < 0 or bird.y > HEIGHT:
            flag = True

def add_bar():
    gap_y = random.randint(200, HEIGHT - 200)
    
    bar_up_actor = Actor(bar_up)
    bar_up_actor.pos = (WIDTH + 100, gap_y - gap//2 - bar_up_actor.height//2)
    
    bar_down_actor = Actor(bar_down)
    bar_down_actor.pos = (WIDTH + 100, gap_y + gap//2 + bar_down_actor.height//2)
    
    bars.append(bar_up_actor)
    bars.append(bar_down_actor)

def on_key_down(key):
    global flag
    if key == keys.SPACE and not flag:
        bird.velocity = fs
    elif key == keys.R and flag:
        reset_game()

def reset_game():
    global score, flag, bars, passed
    score = 0
    flag = False
    bird.pos = (100, 250)
    bird.velocity = 0
    bars = []
    passed = set()
    
    add_bar()
    
    temp_bars = bars.copy()
    for bar in temp_bars:
        bar.x += 200

    add_bar()

reset_game()

pgzrun.go()