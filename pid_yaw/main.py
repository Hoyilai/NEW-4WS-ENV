import math
import pygame
from constants import *
from car import Car
from car_4ws import Car_4ws
from path_generation import generate_circle, generate_smooth_random_path
from pid_controller import PIDController


# Initialize Pygame
pygame.init()


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Enhanced Autonomous 4WS Car Simulation")

# Function to display mode selection options
def display_mode_selection(screen):
    screen.fill(WHITE)  # Clear the screen
    font = pygame.font.Font(None, 36)  # Create a font object

    # Render text for each mode
    circle_text = font.render("Press '1' for Circle Mode", True, BLACK)
    random_text = font.render("Press '2' for Random Trace Mode", True, BLACK)
    manual_text = font.render("Press '3' for Manual Steering Mode", True, BLACK)

    # Get rects for text positioning
    circle_rect = circle_text.get_rect(center=(screen_width / 2, screen_height / 3))
    random_rect = random_text.get_rect(center=(screen_width / 2, screen_height / 2))
    manual_rect = manual_text.get_rect(center=(screen_width / 2, screen_height * 2 / 3))

    # Blit (copy) text surfaces to the main screen surface
    screen.blit(circle_text, circle_rect)
    screen.blit(random_text, random_rect)
    screen.blit(manual_text, manual_rect)

    pygame.display.flip()  # Update the screen to show the text


# Function to handle user input for mode selection
def get_user_mode_selection(screen):
    display_mode_selection(screen)  # Display the selection options
    mode_selection = None  # Variable to store user's selection

    while mode_selection is None:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    mode_selection = 'circle'
                elif event.key == pygame.K_2:
                    mode_selection = 'random'
                elif event.key == pygame.K_3:
                    mode_selection = 'manual'
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()

    return mode_selection


def calculate_cte(car, circle_center, radius):
    dx = car.x - circle_center[0]
    dy = car.y - circle_center[1]
    distance = math.sqrt(dx**2 + dy**2)
    return distance - radius

def find_lookahead_point(car, path, lookahead_distance):
    for point in path:
        dx = point[0] - car.x
        dy = point[1] - car.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance >= lookahead_distance:
            # Calculate angle to the lookahead point
            angle_to_point = math.atan2(dy, dx)
            # Calculate the steering angle needed
            angle_diff = angle_to_point - car.yaw
            # Normalize the angle difference
            angle_diff = (angle_diff + math.pi) % (2 * math.pi) - math.pi
            return angle_diff
    return None

def update_car_steering(car, path, lookahead_distance):
    angle_diff = find_lookahead_point(car, path, lookahead_distance)
    if angle_diff is not None:
        car.front_wheel_angle = angle_diff  # Simplified, consider PID controller for smoothing
        # Apply limits to the steering angle if necessary


mode_selection = get_user_mode_selection(screen)

# Based on the mode_selection, set up the initial conditions for the simulation
if mode_selection == 'random':
    # Set up for random trace mode
    pass
elif mode_selection == 'manual':
    # Set up for manual steering mode
    pass
else:
    # Default to circle mode if no selection or 'circle' is selected
    pass

# Initialize the car and path based on the selection
car = Car(screen_width // 2, screen_height // 2, angle=0, velocity=30)
if mode_selection == 'random':
    current_path = generate_smooth_random_path((car.x, car.y), num_segments=10, segment_length=50)
else:  # Default to a circle if not random
    radius = 100
    current_path = generate_circle(car.x, car.y, radius, points=100)

if mode_selection == 'manual':
    car = Car_4ws(screen_width // 2, screen_height // 2)
else:
    car = Car(screen_width // 2, screen_height // 2, angle=0, velocity=30)  # Assuming this is for autonomous modes
     

# Main simulation loop
running = True
clock = pygame.time.Clock()
while running:
    delta_time = clock.tick(60) / 1000.0  # Convert milliseconds to seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    lookahead_distance = 50  # Adjust based on your simulation needs

    # Within the simulation loop:
    if mode_selection == 'random':
        update_car_steering(car, current_path, lookahead_distance)
    # Update car dynamics here...

    else:
        # Existing CTE calculation for circular paths
        dx = car.x - current_path[0][0]
        dy = car.y - current_path[0][1]
        cte = math.sqrt(dx**2 + dy**2) - radius

    car.update(delta_time, cte)

    # Clear screen and draw everything
    screen.fill(WHITE)
    if mode_selection == 'circle':
        pygame.draw.circle(screen, RED, current_path[0], radius, 1)
    else:
        for i in range(1, len(current_path)):
            pygame.draw.line(screen, RED, current_path[i - 1], current_path[i], 2)
    
    car.draw(screen)
    pygame.display.flip()

pygame.quit()


