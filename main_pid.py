import pygame
import math

from car_model import Car

# Initialize Pygame
pygame.init()

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Following Path with PID Control")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Car:
    def __init__(self, x, y, angle=0):
        self.x = x
        self.y = y
        self.angle = angle  # Car's orientation
        self.speed = 2  # Speed
        self.front_wheel_angle = 0  # Initialize front wheel steering angle
        self.rear_wheel_angle = 0  # Initialize rear wheel steering angle
        # PID coefficients
        self.Kp = 12
        self.Ki = 0.
        self.Kd = 0.
        # PID error terms
        self.previous_error = 0
        self.integral = 0

    def update(self, cte):
        # Calculate PID terms
        proportional = cte
        self.integral += cte
        derivative = cte - self.previous_error
        self.previous_error = cte

        # Calculate steering angle
        steering = (self.Kp * proportional) + (self.Ki * self.integral) + (self.Kd * derivative)
        
        # Apply steering (simplified model for demonstration)
        self.angle += steering
        self.angle = self.angle % 360  # Ensure angle is within 0-360 degrees

        # Move car forward in current direction
        self.x += math.cos(math.radians(self.angle)) * self.speed
        self.y += math.sin(math.radians(self.angle)) * self.speed

        pid_output = self.Kp * cte  # Simplified example; expand with full PID logic
        self.front_wheel_angle = pid_output  # Directly use PID output for front wheel angle in this example
        self.rear_wheel_angle = -pid_output / 2  # Example: rear wheel angle is half and opposite

    def draw(self, screen):
        # Basic car representation
        car_rect = pygame.Rect(self.x - 20, self.y - 10, 40, 20)  # Example car size
        car_surface = pygame.Surface((40, 20), pygame.SRCALPHA)  # Transparent surface
        pygame.draw.rect(car_surface, BLUE, car_rect)  # Draw the car on the surface
        
        # Rotate the car surface to match the car's orientation
        rotated_car = pygame.transform.rotate(car_surface, -self.angle)
        car_position = rotated_car.get_rect(center=(self.x, self.y))

        screen.blit(rotated_car, car_position.topleft)

        # Visualize steering angles with lines
        line_length = 30  # Length of the lines representing wheel direction
        # Front steering line
        front_dx = math.cos(math.radians(self.angle + self.front_wheel_angle)) * line_length
        front_dy = math.sin(math.radians(self.angle + self.front_wheel_angle)) * line_length
        pygame.draw.line(screen, RED, (self.x, self.y), (self.x + front_dx, self.y + front_dy), 3)
        
        # Rear steering line (optional, depending on your model)
        rear_dx = math.cos(math.radians(self.angle + self.rear_wheel_angle)) * line_length
        rear_dy = math.sin(math.radians(self.angle + self.rear_wheel_angle)) * line_length
        pygame.draw.line(screen, GREEN, (self.x, self.y), (self.x - rear_dx, self.y - rear_dy), 3)

        # Optionally, print steering angles for debugging
        print(f"Front Angle: {self.front_wheel_angle}, Rear Angle: {self.rear_wheel_angle}")

def generate_circle(cx, cy, radius, points=100):
    return [(math.cos(2 * math.pi / points * x) * radius + cx, math.sin(2 * math.pi / points * x) * radius + cy) for x in range(points)]

def calculate_cte(car, circle_center, radius):
    dx = car.x - circle_center[0]
    dy = car.y - circle_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance - radius

# Circle path setup
circle_center = (screen_width // 2, screen_height // 2)
radius = 100
path = generate_circle(*circle_center, radius)

# Car setup
car = Car(screen_width // 2, screen_height // 2 - radius)

# Main loop
running = True
clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    # Draw path
    for point in path:
        pygame.draw.circle(screen, RED, (int(point[0]), int(point[1])), 2)

    # Update and draw car
    cte = calculate_cte(car, circle_center, radius)
    car.update(cte)
    car.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
