import math
import pygame
from pid_controller import PIDController
from constants import *

class Car:
    def __init__(self, x, y, angle=0, velocity=15):
        self.x = x
        self.y = y
        self.yaw = math.radians(angle)  # Convert to radians for consistency in calculations
        self.velocity = velocity
        self.front_wheel_angle = 0
        self.rear_wheel_angle = 0
        self.pid_controller = PIDController(Kp=0.1, Ki=0.0, Kd=0.01)
        self.length = 50  # Length of the car for drawing and dynamics
        self.width = 20  # Width of the car

        self.max_steering_angle = math.radians(60)  # Maximum steering angle in radians

    def update(self, delta_time, cte):
        # PID control for front steering based on CTE
        steering_adjustment = self.pid_controller.update(cte, delta_time)
        self.front_wheel_angle = max(min(steering_adjustment, self.max_steering_angle), -self.max_steering_angle)

        # Simplified rear steering logic (for demonstration)
        # Adjusts rear steering based on velocity: counter-phase at low speeds, in-phase at high speeds
        if self.velocity < 10:  # Threshold velocity for switching steering phase
            self.rear_wheel_angle = -steering_adjustment / 2  # Counter-phase steering at low speeds
        else:
            self.rear_wheel_angle = steering_adjustment / 4  # In-phase steering at high speeds
        
        # Update car yaw and position
        self.yaw += (self.velocity * math.tan(steering_adjustment) / self.length) * delta_time
        self.x += self.velocity * math.cos(self.yaw) * delta_time
        self.y += self.velocity * math.sin(self.yaw) * delta_time

    def draw(self, screen):
        # Calculate car corners for rectangular representation
        car_corners = self.calculate_corners()
        
        # Draw car body
        pygame.draw.polygon(screen, BLUE, car_corners)

        # Visualize steering angles with lines for front and rear
        self.draw_steering_lines(screen, car_corners)

    def calculate_corners(self):
        # Calculate the four corners of the car based on its position, yaw, and dimensions
        front_left = (self.x + (self.length / 2) * math.cos(self.yaw) - (self.width / 2) * math.sin(self.yaw),
                      self.y + (self.length / 2) * math.sin(self.yaw) + (self.width / 2) * math.cos(self.yaw))
        front_right = (self.x + (self.length / 2) * math.cos(self.yaw) + (self.width / 2) * math.sin(self.yaw),
                       self.y + (self.length / 2) * math.sin(self.yaw) - (self.width / 2) * math.cos(self.yaw))
        rear_left = (self.x - (self.length / 2) * math.cos(self.yaw) - (self.width / 2) * math.sin(self.yaw),
                     self.y - (self.length / 2) * math.sin(self.yaw) + (self.width / 2) * math.cos(self.yaw))
        rear_right = (self.x - (self.length / 2) * math.cos(self.yaw) + (self.width / 2) * math.sin(self.yaw),
                      self.y - (self.length / 2) * math.sin(self.yaw) - (self.width / 2) * math.cos(self.yaw))
        return [front_left, front_right, rear_right, rear_left]

    def draw_steering_lines(self, screen, car_corners):
        # Draw lines from the center of the front and rear axles to represent steering direction
        front_center = ((car_corners[0][0] + car_corners[1][0]) / 2, (car_corners[0][1] + car_corners[1][1]) / 2)
        rear_center = ((car_corners[2][0] + car_corners[3][0]) / 2, (car_corners[2][1] + car_corners[3][1]) / 2)
        
        # Calculate end points for steering lines based on current steering angles
        front_line_end = (front_center[0] + math.cos(self.yaw + self.front_wheel_angle) * 30, 
                          front_center[1] + math.sin(self.yaw + self.front_wheel_angle) * 30)
        rear_line_end = (rear_center[0] + math.cos(self.yaw + self.rear_wheel_angle) * 30, 
                         rear_center[1] + math.sin(self.yaw + self.rear_wheel_angle) * 30)

        # Drawing the steering lines for front and rear
        pygame.draw.line(screen, RED, front_center, front_line_end, 2)
        pygame.draw.line(screen, GREEN, rear_center, rear_line_end, 2)

        print(f"Front Angle: {self.front_wheel_angle}, Rear Angle: {self.rear_wheel_angle}")