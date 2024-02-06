# Import necessary libraries
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Four Wheel Steering Simulation")

# Main simulation loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Fill the screen with a color (white in this case)
    screen.fill((255, 255, 255))
    
    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

# Save this script as `simulation_init.py` for now.
# This script initializes the simulation environment. We will expand upon this with subsequent steps.

