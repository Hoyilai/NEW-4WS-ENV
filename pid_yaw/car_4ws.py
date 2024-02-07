import math
import pygame
from pid_controller import PIDController
from constants import *

class Car_4ws:
    def __init__(self, x, y, angle=0, velocity=0):
        self.x, self.y = x, y
        self.yaw = math.radians(angle)
        self.velocity = velocity
        self.front_left_wheel_angle = 0
        self.front_right_wheel_angle = 0
        self.rear_left_wheel_angle = 0
        self.rear_right_wheel_angle = 0
        self.length, self.width = 50, 20
        self.max_steering_angle = math.radians(30)

    def update(self, delta_time):
        # Assuming front wheels contribute more to the steering direction
        avg_front_wheel_angle = (self.front_left_wheel_angle + self.front_right_wheel_angle) / 2
        avg_rear_wheel_angle = (self.rear_left_wheel_angle + self.rear_right_wheel_angle) / 2
        steering_angle = (avg_front_wheel_angle + avg_rear_wheel_angle) / 2  # Simplified model

        self.yaw += (self.velocity * math.tan(steering_angle) / self.length) * delta_time
        self.x += math.cos(self.yaw) * self.velocity * delta_time
        self.y += math.sin(self.yaw) * self.velocity * delta_time

    def draw(self, screen):
        # Draw car body
        pygame.draw.rect(screen, BLUE, (self.x - self.length / 2, self.y - self.width / 2, self.length, self.width), 2)
        # Draw wheels as lines
        for angle, offset in [(self.front_left_wheel_angle, (-self.length / 4, -self.width / 4)),
                              (self.front_right_wheel_angle, (self.length / 4, -self.width / 4)),
                              (self.rear_left_wheel_angle, (-self.length / 4, self.width / 4)),
                              (self.rear_right_wheel_angle, (self.length / 4, self.width / 4))]:
            start_pos = (self.x + offset[0], self.y + offset[1])
            end_pos = (start_pos[0] + 20 * math.cos(self.yaw + angle), start_pos[1] + 20 * math.sin(self.yaw + angle))
            pygame.draw.line(screen, GREEN, start_pos, end_pos, 3)



