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

    def update(self, delta_time, cte = None):
        if self.velocity == 0:
            return  # No movement if velocity is zero

        # Ensure wheel angles are within bounds
        self.front_left_wheel_angle = max(min(self.front_left_wheel_angle, self.max_steering_angle), -self.max_steering_angle)
        self.front_right_wheel_angle = max(min(self.front_right_wheel_angle, self.max_steering_angle), -self.max_steering_angle)
        self.rear_left_wheel_angle = max(min(self.rear_left_wheel_angle, self.max_steering_angle), -self.max_steering_angle)
        self.rear_right_wheel_angle = max(min(self.rear_right_wheel_angle, self.max_steering_angle), -self.max_steering_angle)

            # Assuming front wheels contribute more to the steering direction
        avg_front_wheel_angle = (self.front_left_wheel_angle + self.front_right_wheel_angle) / 2
        avg_rear_wheel_angle = (self.rear_left_wheel_angle + self.rear_right_wheel_angle) / 2

            # Compute average steering angles for simplicity
        # Calculate the turning radius for the front and rear, considering non-zero angles
        turn_radius_front = float('inf') if avg_front_wheel_angle == 0 else self.length / math.tan(avg_front_wheel_angle)
        turn_radius_rear = float('inf') if avg_rear_wheel_angle == 0 else self.length / math.tan(avg_rear_wheel_angle)

        # Calculate effective turning radius
        # Use harmonic mean to avoid division by zero and handle infinite radii correctly
        if turn_radius_front != float('inf') and turn_radius_rear != float('inf'):
            turn_radius_effective = 2 / (1 / turn_radius_front + 1 / turn_radius_rear)
        else:
            turn_radius_effective = turn_radius_front if turn_radius_rear == float('inf') else turn_radius_rear
        
        # Handle the case where the effective turn radius is still infinity (straight movement)
        if turn_radius_effective != float('inf'):
            angular_velocity = self.velocity / turn_radius_effective
        else:
            angular_velocity = 0  # No angular velocity if moving straight
        
        # Update yaw and position
        self.yaw += angular_velocity * delta_time
        self.x += math.cos(self.yaw) * self.velocity * delta_time
        self.y += math.sin(self.yaw) * self.velocity * delta_time

        print(f"Front Left: {math.degrees(self.front_right_wheel_angle)}, Front Right: {math.degrees(self.rear_right_wheel_angle)}")
        print(f"Rear Left: {math.degrees(self.front_left_wheel_angle)}, Rear Right: {math.degrees(self.rear_left_wheel_angle)}")


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



