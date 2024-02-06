import pygame
import math

from car_model import Car

# Initialize Pygame
pygame.init()

# Setup display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Autonomous Car with Four-Wheel Steering")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Car:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle  # Car's overall orientation in degrees
        self.front_wheel_angle = 0  # Steering angle of the front wheels
        self.rear_wheel_angle = 0  # Steering angle of the rear wheels
        self.speed = 2  # Speed of the car
        self.length = 50  # Distance between front and rear axles, correcting the missing attribute

        # PID components
        self.Kp = 0.1  # Proportional gain
        self.Ki = 0.01  # Integral gain
        self.Kd = 0.05  # Derivative gain
        self.previous_error = 0
        self.integral_error = 0


    def calculate_steering(self, target_x, target_y):
        # Calculate the angle to the target point
        dx = target_x - self.x
        dy = target_y - self.y
        target_angle_rad = math.atan2(dy, dx)
        target_angle = math.degrees(target_angle_rad) % 360

        # Determine the front and rear wheel steering angles needed
        angle_to_target = (target_angle - self.angle + 360) % 360
        if angle_to_target > 180:
            angle_to_target -= 360  # Ensure shortest turning direction

        # Simplified steering logic for demonstration
        self.front_wheel_angle = angle_to_target * 0.5
        self.rear_wheel_angle = self.front_wheel_angle * 0.3  # Rear wheels have a smaller steering angle

        print(f"Front steering angle: {self.front_wheel_angle:.2f}, Rear steering angle: {self.rear_wheel_angle:.2f}")

    def update_position(self):
        # Convert steering angles and car orientation to radians for calculation
        front_rad = math.radians(self.front_wheel_angle)
        rear_rad = math.radians(self.rear_wheel_angle)
        car_rad = math.radians(self.angle)

        # Simulate car movement based on front and rear wheel steering
        turn_radius_front = self.length / math.sin(front_rad) if front_rad else float('inf')
        turn_radius_rear = self.length / math.sin(rear_rad) if rear_rad else float('inf')

        # Average the turn radii for simplified car movement
        turn_radius = (turn_radius_front + turn_radius_rear) / 2

        # Update car orientation
        if turn_radius != float('inf'):
            turn_angle = (self.speed / turn_radius) * (180 / math.pi)
            self.angle = (self.angle + turn_angle) % 360

        # Update car position
        self.x += math.cos(car_rad) * self.speed
        self.y += math.sin(car_rad) * self.speed

    def draw(self, screen):
        car_front = (self.x + 15 * math.cos(math.radians(self.angle)), self.y + 15 * math.sin(math.radians(self.angle)))
        car_back = (self.x - 15 * math.cos(math.radians(self.angle)), self.y - 15 * math.sin(math.radians(self.angle)))
        pygame.draw.line(screen, BLUE, car_front, car_back, 15)  # Car body
        pygame.draw.circle(screen, RED, (int(car_front[0]), int(car_front[1])), 5)  # Car front indicator

        wheel_length = 20  # Length of the line representing the wheel direction
        
        # Front wheels
        front_wheel_origin = (self.x + math.cos(math.radians(self.angle)) * self.length / 2,
                              self.y + math.sin(math.radians(self.angle)) * self.length / 2)
        front_wheel_end = (front_wheel_origin[0] + math.cos(math.radians(self.angle + self.front_wheel_angle)) * wheel_length,
                           front_wheel_origin[1] + math.sin(math.radians(self.angle + self.front_wheel_angle)) * wheel_length)

        # Rear wheels
        rear_wheel_origin = (self.x - math.cos(math.radians(self.angle)) * self.length / 2,
                             self.y - math.sin(math.radians(self.angle)) * self.length / 2)
        rear_wheel_end = (rear_wheel_origin[0] + math.cos(math.radians(self.angle + self.rear_wheel_angle)) * wheel_length,
                          rear_wheel_origin[1] + math.sin(math.radians(self.angle + self.rear_wheel_angle)) * wheel_length)

        # Draw the lines representing the front and rear wheels
        pygame.draw.line(screen, RED, front_wheel_origin, front_wheel_end, 3)
        pygame.draw.line(screen, BLUE, rear_wheel_origin, rear_wheel_end, 3)


# Circular trace generation
def generate_circular_trace(cx, cy, r, n_points=100):
    return [(cx + r * math.cos(2 * math.pi * t / n_points), cy + r * math.sin(2 * math.pi * t / n_points)) for t in range(n_points)]

# Setup for circular trace
cx, cy, r = screen_width // 2, screen_height // 2, 150
circular_trace = generate_circular_trace(cx, cy, r)

# Create the car instance
car = Car(circular_trace[0][0], circular_trace[0][1], 0)

# Main game loop
running = True
clock = pygame.time.Clock()
trace_index = 0

while running:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 2. Game State Updates
    
    # Update the car's steering based on the current target point
    if trace_index < len(circular_trace):
        target_point = circular_trace[trace_index]
        car.calculate_steering(target_point[0], target_point[1])
        car.update_position()

        # Increment trace index, handling looping
        trace_index = (trace_index + 1) % len(circular_trace)
    
    # 3. Rendering
    screen.fill(WHITE)  # Clear the screen with a white background
    
    # Draw the circular trace
    for point in circular_trace:
        pygame.draw.circle(screen, RED, (int(point[0]), int(point[1])), 2)
    
    # Draw the car
    car.draw(screen)
    
    pygame.display.flip()  # Update the display with the new frame
    
    clock.tick(60)  # Cap the game at 60 frames per second

pygame.quit()