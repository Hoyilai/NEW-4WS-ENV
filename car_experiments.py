import pygame
import sys
import math
from car_model import Car  

# Initialize Pygame
pygame.init()

# Setup display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Car Experiments")


GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
        pygame.draw.line(screen, RED, (self.x, self.y), (self.x + front_dx, self.y + front_dy), 3)
        
        # Rear steering line (optional, depending on your model)
        rear_dx = math.cos(math.radians(self.angle + self.rear_wheel_angle)) * line_length
        rear_dy = math.sin(math.radians(self.angle + self.rear_wheel_angle)) * line_length
        pygame.draw.line(screen, GREEN, (self.x, self.y), (self.x - rear_dx, self.y - rear_dy), 3)

        # Optionally, print steering angles for debugging
        print(f"Front Angle: {self.front_wheel_angle}, Rear Angle: {self.rear_wheel_angle}")

# Define colors
WHITE = (255, 255, 255)

def handle_input(car):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        car.speed += 0.1  # Increase speed
    if keys[pygame.K_DOWN]:
        car.speed -= 0.1  # Decrease speed
    if keys[pygame.K_LEFT]:
        car.front_wheel_angle += 1  # Steer left
    if keys[pygame.K_RIGHT]:
        car.front_wheel_angle -= 1  # Steer right

def reset_car():
    return Car(screen_width / 2, screen_height / 2)

def run_experiments():
    car = reset_car()
    running = True
    mode = "MANUAL"  # Start in manual control mode

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:  # Switch mode
                    mode = "MANUAL" if mode != "MANUAL" else "AUTOMATIC"

        screen.fill(WHITE)

        if mode == "MANUAL":
            handle_input(car)
        elif mode == "AUTOMATIC":
            # Example automatic behavior, replace with specific experiment logic
            car.front_wheel_angle = 5  # Constant steering angle for demonstration

        # Update and draw car
        car.update(0)  # For automatic mode, replace 0 with calculated CTE
        car.draw(screen)

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run_experiments()
