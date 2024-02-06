import pygame
import math
import random

# Initialize Pygame
pygame.init()


# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Screen setup
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Enhanced Autonomous 4WS Car Simulation")

# Display mode selection instructions
font = pygame.font.Font(None, 36)
screen.fill(WHITE)
text = font.render("Press 'C' for Circle, 'R' for Random", True, BLACK)
text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
screen.blit(text, text_rect)
pygame.display.flip()

mode_selection = 'circle'  # default
waiting_for_input = True
while waiting_for_input:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                mode_selection = 'circle'
                waiting_for_input = False
            elif event.key == pygame.K_r:
                mode_selection = 'random'
                waiting_for_input = False
        elif event.type == pygame.QUIT:
            pygame.quit()
            exit()

# Initialize variables for path and car here
circle_center = (screen_width // 2, screen_height // 2)
radius = 100

def generate_smooth_random_path(start_point, num_segments=5, segment_length=100):
    """
    Generates a smooth, random path starting from 'start_point'.
    
    :param start_point: A tuple of (x, y) coordinates to start the path.
    :param num_segments: Number of segments (or points) to generate.
    :param segment_length: Approximate length of each segment.
    :return: A list of tuples representing the points along the path.
    """
    points = [start_point]
    direction = random.uniform(0, 2 * math.pi)
    for _ in range(num_segments - 1):
        direction += random.uniform(-math.pi / 4, math.pi / 4)  # Slight direction change
        new_point = (points[-1][0] + math.cos(direction) * segment_length,
                     points[-1][1] + math.sin(direction) * segment_length)
        points.append(new_point)
    return points



def generate_circle(cx, cy, radius, points=100):
    circle = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        circle.append((x, y))
    # Ensure the path is continuous by appending the starting point at the end
    circle.append(circle[0])
    return circle

# Place path generation functions (generate_circle and generate_smooth_random_path) here

if mode_selection == 'random':
    current_path = generate_smooth_random_path((screen_width // 2, screen_height // 2), num_segments=10, segment_length=50)
    path_mode = 'random'
else:
    current_path = generate_circle(circle_center[0], circle_center[1], radius)
    path_mode = 'circle'


def calculate_cte(car, circle_center, radius):
    dx = car.x - circle_center[0]
    dy = car.y - circle_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance - radius



def generate_smooth_random_path(start_point, num_segments=5, segment_length=100):
    points = [start_point]
    direction = random.uniform(0, 2 * math.pi)
    for _ in range(num_segments):
        direction += random.uniform(-math.pi / 4, math.pi / 4)  # Slight direction change
        end_x = points[-1][0] + math.cos(direction) * segment_length
        end_y = points[-1][1] + math.sin(direction) * segment_length
        points.append((end_x, end_y))
    return points


class PIDController:
    def __init__(self, Kp, Ki, Kd):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.previous_error = 0
        self.integral = 0

    def update(self, error, delta_time):
        self.integral += error * delta_time
        derivative = (error - self.previous_error) / delta_time if delta_time > 0 else 0
        self.previous_error = error
        return self.Kp * error + self.Ki * self.integral + self.Kd * derivative

class Car:
    def __init__(self, x, y, angle=0, velocity=30):
        self.x = x
        self.y = y
        self.yaw = math.radians(angle)  # Convert to radians for consistency in calculations
        self.velocity = velocity
        self.front_wheel_angle = 0
        self.rear_wheel_angle = 0
        self.pid_controller = PIDController(Kp=0.1, Ki=0.0, Kd=0.01)
        self.length = 50  # Length of the car for drawing and dynamics
        self.width = 20  # Width of the car

    def update(self, delta_time, cte):
        # PID control for front steering based on CTE
        steering_adjustment = self.pid_controller.update(cte, delta_time)
        self.front_wheel_angle = steering_adjustment

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

def generate_circle(cx, cy, radius, points=100):
    """
    Generates a list of points along the perimeter of a circle.
    
    :param cx: x-coordinate of the circle's center
    :param cy: y-coordinate of the circle's center
    :param radius: Radius of the circle

car = Car(screen_width // 2, screen_height // 2 - radius)
    :return: List of tuples, where each tuple represents the x and y coordinates of a point
    """
    circle = []
    for i in range(points):
        angle = 2 * math.pi * i / points
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        circle.append((x, y))
    return circle

      

# Main loop setup
running = True
clock = pygame.time.Clock()
car = Car(screen_width // 2, screen_height // 2 - radius)

while running:
    delta_time = clock.tick(60) / 1000.0  # Convert to seconds



    # Calculate CTE for the circular path
    cte = calculate_cte(car, circle_center, radius)

    # Update the car's state based on the CTE
    car.update(delta_time, cte)

    # Clear the screen
    screen.fill(WHITE)

    # Draw the current path
    if path_mode == 'circle':
        pygame.draw.circle(screen, RED, circle_center, radius, 1)
    else:  # Random path mode
        for i in range(1, len(current_path)):
            pygame.draw.line(screen, RED, current_path[i - 1], current_path[i], 2)

    # For simplicity, we'll update the car's movement here directly
    # This should be replaced with your logic for following the path
    cte = calculate_cte(car, circle_center, radius) if path_mode == 'circle' else 0  # Simplify for random path

    car.update(delta_time, cte)
    car.draw(screen)

    pygame.display.flip()


