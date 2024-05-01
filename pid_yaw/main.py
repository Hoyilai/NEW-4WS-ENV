
import math
from time import clock_getres
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

# Lane definitions
lane_width = 40
lane_centers = [screen_height // 2 - lane_width, screen_height // 2, screen_height // 2 + lane_width]
current_lane_index = 1  # Start in the middle lane


def draw_lanes(screen):
    for lane_center in lane_centers:
        pygame.draw.line(screen, GREY, (0, lane_center), (screen_width, lane_center), 5)


def set_wheel_angles_manually(car):
    print("Enter wheel angles in degrees (Front Left, Front Right, Rear Left, Rear Right):")
    angles = input().split()  # Expecting four numbers separated by spaces
    if len(angles) == 4:
        try:
            fl_angle, fr_angle, rl_angle, rr_angle = [math.radians(float(angle)) for angle in angles]
            car.front_left_wheel_angle = fl_angle
            car.front_right_wheel_angle = fr_angle
            car.rear_left_wheel_angle = rl_angle
            car.rear_right_wheel_angle = rr_angle
        except ValueError:
            print("Invalid input. Setting all angles to 0.")
    else:
        print("Invalid input. Expected four angles.")


def handle_manual_control(car, event):
    if isinstance(car, Car_4ws):
        angle_increment = math.radians(5)
        if event.key == pygame.K_w:  # Increase velocity
            car.velocity += 1
        elif event.key == pygame.K_s:  # Decrease velocity
            car.velocity -= 1

        elif event.key == pygame.K_a: # Turn left
            car.front_right_wheel_angle += angle_increment
            car.rear_right_wheel_angle += angle_increment

        elif event.key == pygame.K_d: # Turn right
            car.front_right_wheel_angle += angle_increment
            car.rear_right_wheel_angle += angle_increment

def handle_lane_change(car, event):
    global current_lane_index
    if event.key == pygame.K_a and current_lane_index > 0:  # Move to the left lane
        current_lane_index -= 1
    elif event.key == pygame.K_d and current_lane_index < len(lane_centers) - 1:  # Move to the right lane
        current_lane_index += 1
    car.y = lane_centers[current_lane_index]

# Function to display mode selection options
def display_mode_selection(screen):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    circle_text = font.render("Press '1' for Circle Mode", True, BLACK)
    manual_text = font.render("Press '2' for Manual Steering Mode", True, BLACK)
    lane_change_text = font.render("Press '3' for Lane Change Mode", True, BLACK)
    screen.blit(circle_text, (screen_width // 2 - circle_text.get_width() // 2, screen_height / 4))
    screen.blit(manual_text, (screen_width // 2 - manual_text.get_width() // 2, screen_height / 2))
    screen.blit(lane_change_text, (screen_width // 2 - lane_change_text.get_width() // 2, screen_height * 3 / 4))
    pygame.display.flip()


def get_user_mode_selection(screen):
    display_mode_selection(screen)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 'circle'
                elif event.key == pygame.K_2:
                    return 'manual'
                elif event.key is pygame.K_3:
                    return 'lane_change'
            elif event.type is pygame.QUIT:
                pygame.quit()
                exit()

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

# Select car type based on mode
if mode_selection in ['manual', 'input']:
    car = Car_4ws(screen_width // 2, screen_height // 2)
else:
    car = Car(screen_width // 2, screen_height // 2, angle=0, velocity=30)

# For manual input mode, ask for wheel angles before starting the loop
radius = 100  # Define the radius variable
if mode_selection == 'circle':
    current_path = generate_circle(car.x, car.y, radius, points=100)
elif mode_selection == 'random':
    current_path = generate_smooth_random_path((car.x, car.y), num_segments=10, segment_length=50)


if mode_selection == 'manual':
    car = Car_4ws(screen_width // 2, screen_height // 2)
else:
    car = Car(screen_width // 2, screen_height // 2, angle=0, velocity=30)  # Assuming this is for autonomous modes
     

# Main simulation loop
running = True
while running:
    delta_time = pygame.time.Clock().tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if mode_selection == 'manual' or mode_selection == 'lane_change':
                handle_manual_control(car, event)
                if mode_selection == 'lane_change':
                    handle_lane_change(car, event)

    screen.fill(WHITE)
    if mode_selection == 'lane_change':
        draw_lanes(screen)

    lookahead_distance = 50  # Adjust based on your simulation needs



    if mode_selection == 'manual':
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # Accelerate
            car.velocity += 0.05  # Adjust for realism
        if keys[pygame.K_s]:  # Decelerate
            car.velocity -= 0.05
        
        
        if keys[pygame.K_d]:  # Steer left
            car.front_right_wheel_angle += math.radians(1)
            car.rear_right_wheel_angle += math.radians(1)
        if keys[pygame.K_a]:  # Steer right
            car.front_right_wheel_angle -= math.radians(1)
            car.rear_right_wheel_angle -= math.radians(1)

        print(f"Front Left: {math.degrees(car.front_right_wheel_angle)}, Front Right: {math.degrees(car.rear_right_wheel_angle)}")
        print(f"Rear Left: {math.degrees(car.front_left_wheel_angle)}, Rear Right: {math.degrees(car.rear_left_wheel_angle)}")

        
        
        # Ensure angles are within limits
        car.front_left_wheel_angle = max(min(car.front_left_wheel_angle, car.max_steering_angle), -car.max_steering_angle)
        car.front_right_wheel_angle = max(min(car.front_right_wheel_angle, car.max_steering_angle), -car.max_steering_angle)

        car.update(delta_time)  # Update car's state with the new velocity and angles

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
