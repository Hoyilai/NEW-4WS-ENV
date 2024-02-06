import pygame
import math
import matplotlib.pyplot as plt

from car_model import Car

# Initialize Pygame
pygame.init()

# Setup display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Define experiment parameters
steering_angles = range(-30, 35, 5)  # From -30 to 30 degrees, in steps of 5
turning_radii = []

# Function to calculate turning radius from car's path
def calculate_turning_radius(car_path):
    # Implement a method to calculate the turning radius based on car_path
    # This could be as simple as finding the max deviation from a straight line
    # For simplicity, this example will not provide a complex calculation
    return 100  # Placeholder value

for angle in steering_angles:
    car = Car(screen_width // 2, screen_height // 2)
    car.steering_angle = angle  # Set car's steering angle
    
    car_path = []  # Store the car's path to calculate turning radius
    
    # Reset Pygame clock
    clock = pygame.time.Clock()
    
    for _ in range(60):  # Run each experiment for a few seconds
        car.update_position()
        car_path.append((car.x, car.y))
        
        # Clear screen and redraw (optional, for visualization)
        screen.fill((255, 255, 255))
        car.draw(screen)
        pygame.display.flip()
        
        clock.tick(60)  # Maintain a steady framerate
    
    # Calculate and record turning radius for current angle
    turning_radius = calculate_turning_radius(car_path)
    turning_radii.append(turning_radius)

# Plotting results
plt.plot(steering_angles, turning_radii, marker='o')
plt.xlabel('Steering Angle (degrees)')
plt.ylabel('Turning Radius')
plt.title('Turning Radius by Steering Angle')
plt.grid(True)
plt.show()

# Quit Pygame
pygame.quit()
