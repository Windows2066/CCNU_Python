import random
import math
import time
import pgzrun

# 游戏窗口尺寸
WIDTH = 480
HEIGHT = 852

# 游戏状态
READY = 0
PLAYING = 1
GAME_OVER = 2
game_status = READY

# 得分
score = 0
high_score = 0

# 玩家飞机
hero = Actor('hero')
hero.pos = (WIDTH // 2, HEIGHT - 100)
hero.lives = 3
hero.is_hit = False
hero.hit_timer = 0

# 敌机列表
enemies = []
enemy_spawn_timer = 0
enemy_spawn_interval = 1.0  # 每秒生成一个敌机

# 子弹列表
bullets = []
bullet_cooldown = 0
bullet_cooldown_time = 0.2  # 射击冷却时间

# 爆炸效果列表
explosions = []

# 游戏开始时间
start_time = 0

# 初始化游戏
def init_game():
    global game_status, score, hero, enemies, bullets, explosions, enemy_spawn_timer, bullet_cooldown, start_time
    
    game_status = PLAYING
    score = 0
    
    hero.pos = (WIDTH // 2, HEIGHT - 100)
    hero.lives = 3
    hero.is_hit = False
    hero.hit_timer = 0
    
    enemies = []
    enemy_spawn_timer = 0
    
    bullets = []
    bullet_cooldown = 0
    
    explosions = []
    
    start_time = time.time()
    
    # 播放游戏背景音乐
    sounds.game_music.play(-1)  # -1参数表示循环播放
    sounds.game_music.set_volume(0.5)

# 更新游戏
def update(dt):
    global game_status, score, high_score, enemy_spawn_timer, bullet_cooldown
    
    if game_status == PLAYING:
        # 更新玩家状态
        update_hero(dt)
        
        # 生成敌机
        enemy_spawn_timer += dt
        if enemy_spawn_timer >= enemy_spawn_interval:
            spawn_enemy()
            enemy_spawn_timer = 0
            
        # 更新敌机
        update_enemies(dt)
        
        # 射击冷却
        if bullet_cooldown > 0:
            bullet_cooldown -= dt
            
        # 检测按键
        if keyboard.space and bullet_cooldown <= 0:
            fire_bullet()
            bullet_cooldown = bullet_cooldown_time
            
        # 更新子弹
        update_bullets(dt)
        
        # 碰撞检测
        check_collisions()
        
        # 更新爆炸效果
        update_explosions(dt)
        
        # 检查游戏结束条件
        if hero.lives <= 0:
            game_status = GAME_OVER
            sounds.game_music.stop()
            high_score = max(high_score, score)

# 更新玩家状态
def update_hero(dt):
    # 处理被击中状态
    if hero.is_hit:
        hero.hit_timer -= dt
        if hero.hit_timer <= 0:
            hero.is_hit = False
    
    # 移动控制
    speed = 300  # 玩家移动速度
    if keyboard.left and hero.left > 0:
        hero.x -= speed * dt
    if keyboard.right and hero.right < WIDTH:
        hero.x += speed * dt
    if keyboard.up and hero.top > 0:
        hero.y -= speed * dt
    if keyboard.down and hero.bottom < HEIGHT:
        hero.y += speed * dt
    
    # 确保玩家不会移出屏幕
    hero.x = max(hero.width // 2, min(WIDTH - hero.width // 2, hero.x))
    hero.y = max(hero.height // 2, min(HEIGHT - hero.height // 2, hero.y))

# 生成敌机
def spawn_enemy():
    enemy = Actor('enemy')
    enemy.x = random.randint(enemy.width // 2, WIDTH - enemy.width // 2)
    enemy.y = -enemy.height // 2
    enemy.speed = random.uniform(100, 200)  # 敌机速度
    enemies.append(enemy)

# 更新敌机
def update_enemies(dt):
    for enemy in enemies[:]:
        enemy.y += enemy.speed * dt
        
        # 如果敌机飞出屏幕底部，移除敌机
        if enemy.top > HEIGHT:
            enemies.remove(enemy)

# 发射子弹
def fire_bullet():
    bullet = Actor('bullet')
    bullet.pos = hero.pos
    bullet.speed = 500  # 子弹速度
    bullets.append(bullet)
    sounds.gun.play()

# 更新子弹
def update_bullets(dt):
    for bullet in bullets[:]:
        bullet.y -= bullet.speed * dt
        
        # 如果子弹飞出屏幕顶部，移除子弹
        if bullet.bottom < 0:
            bullets.remove(bullet)

# 碰撞检测
def check_collisions():
    global score
    
    # 子弹与敌机碰撞
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                # 移除子弹和敌机
                if bullet in bullets:
                    bullets.remove(bullet)
                if enemy in enemies:
                    enemies.remove(enemy)
                
                # 创建爆炸效果
                create_explosion(enemy.pos)
                
                # 增加得分
                score += 10
                
                # 播放击中敌机音效
                sounds.got_enemy.play()
                
                break
    
    # 玩家与敌机碰撞
    if not hero.is_hit:
        for enemy in enemies[:]:
            if hero.colliderect(enemy):
                # 移除敌机
                enemies.remove(enemy)
                
                # 创建爆炸效果
                create_explosion(enemy.pos)
                
                # 玩家受伤
                hero.lives -= 1
                hero.is_hit = True
                hero.hit_timer = 2  # 无敌时间2秒
                
                # 播放爆炸音效
                sounds.explode.play()
                
                break

# 创建爆炸效果
def create_explosion(pos):
    explosion = Actor('hero_blowup')
    explosion.pos = pos
    explosion.timer = 0.5  # 爆炸效果持续时间
    explosions.append(explosion)

# 更新爆炸效果
def update_explosions(dt):
    for explosion in explosions[:]:
        explosion.timer -= dt
        if explosion.timer <= 0:
            explosions.remove(explosion)

# 绘制游戏
def draw():
    screen.clear()
    screen.blit('background', (0, 0))
    
    if game_status == READY:
        # 显示游戏开始画面
        screen.draw.text("太空飞机大战", centerx=WIDTH//2, centery=HEIGHT//2 - 50, fontname="s", fontsize=60, color="white")
        screen.draw.text("按空格键开始游戏", centerx=WIDTH//2, centery=HEIGHT//2 + 50, fontname="s", fontsize=30, color="white")
    
    elif game_status == PLAYING:
        # 绘制玩家飞机（闪烁效果表示无敌状态）
        if not hero.is_hit or int(time.time() * 5) % 2 == 0:
            hero.draw()
        
        # 绘制敌机
        for enemy in enemies:
            enemy.draw()
        
        # 绘制子弹
        for bullet in bullets:
            bullet.draw()
        
        # 绘制爆炸效果
        for explosion in explosions:
            explosion.draw()
        
        # 显示得分和生命值
        screen.draw.text(f"分数: {score}", (10, 10), fontname="s", fontsize=30, color="white")
        screen.draw.text(f"生命: {hero.lives}", (10, 50), fontname="s", fontsize=30, color="white")
    
    elif game_status == GAME_OVER:
        # 显示游戏结束画面
        screen.draw.text("游戏结束", centerx=WIDTH//2, centery=HEIGHT//2 - 50, fontname="s", fontsize=60, color="white")
        screen.draw.text(f"最终得分: {score}", centerx=WIDTH//2, centery=HEIGHT//2 + 10, fontname="s", fontsize=30, color="white")
        screen.draw.text(f"最高得分: {high_score}", centerx=WIDTH//2, centery=HEIGHT//2 + 50, fontname="s", fontsize=30, color="white")
        screen.draw.text("按空格键重新开始", centerx=WIDTH//2, centery=HEIGHT//2 + 100, fontname="s", fontsize=30, color="white")

# 处理按键事件
def on_key_down(key):
    global game_status
    
    if key == keys.SPACE:
        if game_status == READY or game_status == GAME_OVER:
            init_game()

pgzrun.go()