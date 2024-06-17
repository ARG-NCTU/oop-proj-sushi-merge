import sys
import pygame
import pymunk
import random
from cloud import Cloud
from collision import collide
from config import config, CollisionTypes
from particle import Particle
from text import score, gameover
from wall import Wall
from collections import deque

# 初始化Pygame并创建游戏窗口
pygame.init()
screen = pygame.display.set_mode((config.screen.width, config.screen.height))
pygame.display.set_caption("PySuika")
clock = pygame.time.Clock()

# 显示开始屏幕的函数
def show_start_screen(screen, start_image, start_button_image, start_button_pos):
    screen.blit(start_image, (0, 0))
    button_rect = start_button_image.get_rect(topleft=start_button_pos)
    screen.blit(start_button_image, button_rect.topleft)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# 显示游戏结束屏幕的函数
def show_game_over_screen(screen, game_over_image, again_button_image, again_button_pos):
    screen.blit(game_over_image, (0, 0))
    button_rect = again_button_image.get_rect(topleft=again_button_pos)
    screen.blit(again_button_image, button_rect.topleft)
    pygame.display.update()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    waiting = False

# 显示开始屏幕
show_start_screen(screen, config.start_image, config.start_button_image, config.start_button_pos)

# 初始化物理
space = pymunk.Space()
space.gravity = (0, config.physics.gravity)
space.damping = config.physics.damping
space.collision_bias = config.physics.bias

# 创建墙壁和云
left = Wall(config.top_left, config.bot_left, space)
bottom = Wall(config.bot_left, config.bot_right, space)
right = Wall(config.bot_right, config.top_right, space)
walls = [left, bottom, right]
cloud = Cloud()

# 游戏状态
wait_for_next = 0
game_over = False

# 碰撞处理器
handler = space.add_collision_handler(CollisionTypes.PARTICLE, CollisionTypes.PARTICLE)
handler.begin = collide
handler.data["score"] = 0

GAME_OVER_HEIGHT = config.pad.killy

# 游戏循环
while not game_over:
    # 处理用户输入
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and wait_for_next == 0:
            cloud.release(space)
            wait_for_next = config.screen.delay

    if wait_for_next > 1:
        wait_for_next -= 1
    if wait_for_next == 1:
        cloud.step()
        wait_for_next -= 1

    cloud.curr.set_x(pygame.mouse.get_pos()[0])

    # 绘制背景和粒子
    screen.blit(config.background_blit, (0, 0))
    cloud.draw(screen, wait_for_next)

    pygame.draw.line(screen, (205, 133, 63 ), (355, GAME_OVER_HEIGHT), (config.screen.width, GAME_OVER_HEIGHT), 2)
    
    for p in space.shapes:
        if isinstance(p, Pazrticle):
            p.draw(screen)
            if p.pos[1] < config.pad.killy and p.has_collided:
                gameover(screen)
                game_over = True
    
    score(handler.data['score'], screen)

    # 更新游戏状态
    space.step(1 / config.screen.fps)
    pygame.display.update()
    clock.tick(config.screen.fps)

# 显示游戏结束屏幕
show_game_over_screen(screen, config.game_over_image, config.again_button_image, config.again_button_pos)

# 游戏结束循环
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            sys.exit()
