import pygame
import math
import random

# 初始化 Pygame
pygame.init()

# 窗口设置
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("弹性碰撞模拟")

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255)
]

# 小球参数
NUM_BALLS = 8
RADIUS = 20
MIN_SPEED = 3
MAX_SPEED = 5

# 创建小球列表
balls = []
for _ in range(NUM_BALLS):
    while True:
        # 生成随机位置（确保不与其他球重叠）
        x = random.randint(RADIUS, WIDTH - RADIUS)
        y = random.randint(RADIUS, HEIGHT - RADIUS)
        overlap = False
        for ball in balls:
            dx = x - ball['x']
            dy = y - ball['y']
            if math.hypot(dx, dy) < 2*RADIUS:
                overlap = True
                break
        if not overlap:
            break
    
    # 生成随机速度和颜色
    angle = random.uniform(0, 2*math.pi)
    speed = random.uniform(MIN_SPEED, MAX_SPEED)
    vx = math.cos(angle) * speed
    vy = math.sin(angle) * speed
    
    balls.append({
        'x': x,
        'y': y,
        'vx': vx,
        'vy': vy,
        'radius': RADIUS,
        'color': random.choice(COLORS)
    })

# 游戏主循环
clock = pygame.time.Clock()
running = True
while running:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 清空屏幕
    screen.fill(BLACK)

    # 更新每个小球的位置并处理碰撞
    for ball in balls:
        # 移动小球
        ball['x'] += ball['vx']
        ball['y'] += ball['vy']

        # 边界碰撞检测
        if ball['x'] < ball['radius']:
            ball['x'] = ball['radius']
            ball['vx'] = abs(ball['vx'])
        elif ball['x'] > WIDTH - ball['radius']:
            ball['x'] = WIDTH - ball['radius']
            ball['vx'] = -abs(ball['vx'])
        
        if ball['y'] < ball['radius']:
            ball['y'] = ball['radius']
            ball['vy'] = abs(ball['vy'])
        elif ball['y'] > HEIGHT - ball['radius']:
            ball['y'] = HEIGHT - ball['radius']
            ball['vy'] = -abs(ball['vy'])

        # 绘制小球
        pygame.draw.circle(screen, ball['color'], 
                         (int(ball['x']), int(ball['y'])), ball['radius'])

    # 处理小球之间的碰撞
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            b1 = balls[i]
            b2 = balls[j]
            
            dx = b2['x'] - b1['x']
            dy = b2['y'] - b1['y']
            distance = math.hypot(dx, dy)
            
            if distance < b1['radius'] + b2['radius']:
                # 计算碰撞法线方向
                if distance == 0:
                    continue  # 避免除以零
                nx = dx / distance
                ny = dy / distance
                
                # 计算相对速度
                dvx = b1['vx'] - b2['vx']
                dvy = b1['vy'] - b2['vy']
                dot_product = dvx * nx + dvy * ny
                
                if dot_product > 0:
                    # 计算冲量（质量相同）
                    impulse = 2 * dot_product / 2
                    
                    # 更新速度
                    b1['vx'] -= impulse * nx
                    b1['vy'] -= impulse * ny
                    b2['vx'] += impulse * nx
                    b2['vy'] += impulse * ny
                    
                    # 修正位置防止重叠
                    overlap = (b1['radius'] + b2['radius'] - distance) / 2
                    b1['x'] -= overlap * nx
                    b1['y'] -= overlap * ny
                    b2['x'] += overlap * nx
                    b2['y'] += overlap * ny

    # 更新显示
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
