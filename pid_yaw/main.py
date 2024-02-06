import math
import pygame
from constants import *
from path_generation import generate_smooth_random_path, generate_circle, switch_path_mode
from car import Car

# Initialize Pygame
pygame.init()


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

 # Main loop setup
running = True
clock = pygame.time.Clock()
car = Car(screen_width // 2, screen_height // 2 - radius)

while running:
    delta_time = clock.tick(60) / 1000.0  # Convert to seconds
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                # Switch to circular mode and regenerate the path from the car's location
                switch_path_mode(car, 'circle')
            elif event.key == pygame.K_r:
                # Switch to random path mode and regenerate the path from the car's location
                switch_path_mode(car, 'random')


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


