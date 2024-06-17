import pygame
import random
from config import config

class Wheel:
    def __init__(self):
        self.wheel_image = config.wheel_image
        self.wheel_pos = config.wheel_pos
        self.pointer_image = config.pointer_image
        self.pointer_pos = config.pointer_pos

        self.fruit_names = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        self.current_fruit = random.choice(self.fruit_names)
        self.spinning = False
        self.spin_speed = 0
        self.current_angle = 0  # 当前帧的旋转角度
        self.total_angle = 0  # 累计的总旋转角度
        self.max_spin_speed = 30

    def start_spin(self):
        self.spinning = True
        self.spin_speed = self.max_spin_speed

    def stop_spin(self):
        self.spinning = False

    def update(self):
        if self.spinning:
            self.current_angle += self.spin_speed
            self.current_angle %= 360
            self.total_angle += self.spin_speed  # 累加總旋轉角度
            self.total_angle %= 360  # 對360取餘數
            self.spin_speed *= 0.95
            if self.spin_speed < 0.5:
                self.spin_speed = 0
                self.spinning = False
                self.determine_current_fruit()

    def determine_current_fruit(self):
        segment_angle = 360 / len(self.fruit_names)
        adjusted_angle = self.total_angle  # 使用總旋轉角度计算
        segment_index = int(adjusted_angle // segment_angle)
        self.current_fruit = self.fruit_names[segment_index]

    def draw(self, screen):
        screen.blit(self.wheel_image, self.wheel_pos)
        rotated_image = pygame.transform.rotate(self.pointer_image, -self.current_angle)
        new_rect = rotated_image.get_rect(center=self.pointer_pos)
        screen.blit(rotated_image, new_rect.topleft)

    def get_current_fruit(self):
        return self.current_fruit
