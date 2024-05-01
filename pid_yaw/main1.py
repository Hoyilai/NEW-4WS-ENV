import pygame
import sys
from car_4ws import Car_4ws  # 确保 car_4ws.py 在同一个目录下

# 初始化pygame
pygame.init()

# 设置屏幕大小
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 设置颜色
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 初始化车辆
car = Car_4ws(400, 550, angle=90, velocity=30)  # 车辆水平初始位置在屏幕底部中央，角度设置为90度表示向上

# 设置时钟
clock = pygame.time.Clock()

# 定义车道参数
lane_height = screen_height / 5
num_lanes = 5
lane_centers = [lane_height * (0.5 + i) for i in range(num_lanes)]
current_lane = 2  # 起始在中间车道

# 变道控制
change_count = 0
direction = -1  # -1 for up, 1 for down

# 主循环
running = True
change_time = 0  # 时间控制变道频率
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 每隔一定时间尝试变道
    if pygame.time.get_ticks() - change_time > 2000 and change_count < 10:  # 每2秒尝试一次变道
        if 0 <= current_lane + direction < num_lanes:
            current_lane += direction
            car.y = lane_centers[current_lane]
            change_count += 1
            change_time = pygame.time.get_ticks()
            if change_count % 5 == 0:  # 每五次变道后改变方向
                direction *= -1

    # 更新车辆位置
    car.update(0.05)  # 假设 delta_time 是 0.05

    # 清屏
    screen.fill(WHITE)

    # 绘制车道
    for i in range(num_lanes + 1):
        pygame.draw.line(screen, BLUE, (0, i * lane_height), (screen_width, i * lane_height), 2)

    # 绘制车辆
    car.draw(screen)

    # 刷新屏幕
    pygame.display.flip()

    # 控制帧率
    clock.tick(60)

pygame.quit()
sys.exit()
