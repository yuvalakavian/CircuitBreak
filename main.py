import pygame
import random
import time  # Import the time module

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 15  # 17x17 grid
CELL_SIZE = WIDTH // GRID_SIZE
ROAD_INTERVAL = 3  # Roads occur every 3 cells
TRAFFIC_LIGHT_SIZE = 15  # Traffic light marker radius
CAR_SIZE = 20  # Car size in pixels
CYCLE_PERIOD = 30  # Total ticks for a full traffic light cycle
GREEN_DURATION = 15  # Ticks for green in a given direction
CYBERATTACK_DURATION = 100  # Duration of the cyberattack in frames
CYBERATTACK_CHANCE = 0.01  # Probability of a cyberattack occurring each frame
ACCIDENT_CHANCE = 0.0 # Probability of a non-cyberattack related accident per frame
RESET_DELAY = 5  # Time in seconds before automatic reset after an accident
CYBERATTACK_PAUSE = 3 # Time in seconds to pause the game during cyberattack

# Colors
WHITE = (255, 255, 255)
RED = (220, 20, 60)
GREEN = (50, 205, 50)
BLACK = (0, 0, 0)
BLUE = (65, 105, 225)
YELLOW = (255, 215, 0)
GRAY = (100, 100, 100)  # Road color
DARK_GRAY = (40, 40, 40)  # Non-road background
ORANGE = (255, 165, 0)  # Color to indicate cyberattack

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Smart City Traffic Simulation")
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 74)

# Data structures
traffic_lights = {}  # Key: (row, col) coordinate of intersection
cars = []
cyberattack_active = False
cyberattack_timer = 0
accident = False
accident_location = None
accident_time = None  # Store the time when the accident occurred
affected_lights = set() # Store coordinates of affected traffic lights during cyberattack
cyberattack_pause_end = 0 # Store the time when the cyberattack pause ends
game_paused = False

def is_intersection(i, j):
    return (i % ROAD_INTERVAL == 0) and (j % ROAD_INTERVAL == 0)

def is_on_road(i, j):
    return (i % ROAD_INTERVAL == 0) or (j % ROAD_INTERVAL == 0)

def within_bounds(x, y):
    return 0 <= x < GRID_SIZE and 0 <= y < GRID_SIZE and is_on_road(x, y)

def spawn_car():
    while True:
        x, y = random.choice(range(GRID_SIZE)), random.choice(range(GRID_SIZE))
        if is_on_road(x, y) and not is_intersection(x, y):
            direction = random.choice(['N', 'S', 'E', 'W'])
            return Car(x, y, direction)

# Create traffic lights only at every other road intersection
for i in range(0, GRID_SIZE, ROAD_INTERVAL * 2):
    for j in range(0, GRID_SIZE, ROAD_INTERVAL * 2):
        if is_intersection(i, j):
            traffic_lights[(i, j)] = {
                'timer': random.randint(0, CYCLE_PERIOD - 1)
            }

def get_light_state(pos):
    """Return the light state at an intersection."""
    if pos in traffic_lights:
        t = traffic_lights[pos]['timer']
        return 'NS' if (t % CYCLE_PERIOD) < GREEN_DURATION else 'EW'
    return None

def get_next_pos(x, y, direction):
    """Get the next position based on direction."""
    if direction == 'N':
        return x, y - 1
    elif direction == 'S':
        return x, y + 1
    elif direction == 'E':
        return x + 1, y
    elif direction == 'W':
        return x - 1, y

class Car:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # 'N', 'S', 'E', 'W'

    def move(self, all_cars):
        global cyberattack_active
        global accident
        global accident_location
        global accident_time
        global game_paused

        if accident or game_paused:
            return # Don't move if there's an accident or game is paused

        # Chance of a random accident (independent of cyberattack)
        if not cyberattack_active and random.random() < ACCIDENT_CHANCE:
            # Choose two random cars
            if len(all_cars) >= 2:
                car1, car2 = random.sample(all_cars, 2)
                if (car1.x, car1.y) == (car2.x, car2.y):
                    accident = True
                    accident_location = (car1.x, car1.y)
                    accident_time = time.time()  # Record the time of the accident
                    print(f"Random accident detected at: ({car1.x}, {car1.y})")
                    return

        # During a cyberattack, cars might behave erratically
        if cyberattack_active:
            if random.random() < 0.2:  # 20% chance of erratic behavior
                self.direction = random.choice(['N', 'S', 'E', 'W']) # Sudden direction change
            if random.random() < 0.1: # 10% chance of stopping unexpectedly
                return

        # Calculate next position
        next_x, next_y = get_next_pos(self.x, self.y, self.direction)

        # Check if next position is within bounds
        if within_bounds(next_x, next_y):
            # Check for collision before moving
            for other_car in all_cars:
                if other_car != self and other_car.x == next_x and other_car.y == next_y:
                    accident = True
                    accident_location = (next_x, next_y)
                    accident_time = time.time()  # Record the time of the accident
                    print(f"Accident detected at: ({next_x}, {next_y})")
                    return

            # Check if next position is an intersection
            if is_intersection(next_x, next_y):
                light_state = get_light_state((next_x, next_y))

                # During a cyberattack, traffic lights might malfunction
                if cyberattack_active:
                    # Lights might randomly switch or stay red
                    if random.random() < 0.3: # 30% chance of ignoring the light
                        self.x, self.y = next_x, next_y
                    else:
                        pass # Treat as red
                elif light_state is not None:
                    # Check if car can pass based on its direction and light state
                    if (self.direction in ['N', 'S'] and light_state == 'NS') or \
                       (self.direction in ['E', 'W'] and light_state == 'EW'):
                        # Green light or allowed direction - move
                        self.x, self.y = next_x, next_y
                    else:
                        # Red light - do not move
                        pass
                else:
                    # Intersection without traffic light - move freely
                    self.x, self.y = next_x, next_y
            else:
                # Not at an intersection - move freely
                self.x, self.y = next_x, next_y
        else:
            # Out of bounds - respawn
            cars.remove(self)
            cars.append(spawn_car())

def reset_game():
    global accident, accident_location, cyberattack_active, cyberattack_timer, traffic_lights, cars, accident_time, affected_lights, game_paused, cyberattack_pause_end
    accident = False
    accident_location = None
    accident_time = None
    cyberattack_active = False
    cyberattack_timer = 0
    affected_lights.clear()
    traffic_lights.clear()
    cars.clear()
    game_paused = False
    cyberattack_pause_end = 0
    for i in range(0, GRID_SIZE, ROAD_INTERVAL * 2):
        for j in range(0, GRID_SIZE, ROAD_INTERVAL * 2):
            if is_intersection(i, j):
                traffic_lights[(i, j)] = {
                    'timer': random.randint(0, CYCLE_PERIOD - 1)
                }
    for _ in range(5):
        cars.append(spawn_car())
    print("Game reset.")

# Spawn cars on random roads
for _ in range(4):
    cars.append(spawn_car())

running = True
clock = pygame.time.Clock()

while running:
    screen.fill(DARK_GRAY)

    current_time = time.time()

    # Cyberattack trigger
    if not cyberattack_active and not accident and random.random() < CYBERATTACK_CHANCE:
        cyberattack_active = True
        cyberattack_timer = CYBERATTACK_DURATION
        affected_lights.clear() # Clear previous affected lights
        game_paused = True # Pause the game
        cyberattack_pause_end = current_time + CYBERATTACK_PAUSE
        print("CYBER ATTACK initiated!")

    # Cyberattack duration
    if cyberattack_active:
        cyberattack_timer -= 1
        if cyberattack_timer <= 0:
            cyberattack_active = False
            print("Cyberattack ended.")

    # Auto-reset after accident
    if accident and accident_time is not None and current_time - accident_time >= RESET_DELAY:
        reset_game()

    # Continue game after cyberattack pause
    if game_paused and current_time >= cyberattack_pause_end:
        game_paused = False
        print("Cyberattack pause ended. Simulation continues.")

    # Update traffic lights (might malfunction during cyberattack)
    if not game_paused:
        for pos in traffic_lights:
            if cyberattack_active:
                if random.random() < 0.3: # 30% chance lights get stuck or change erratically
                    affected_lights.add(pos)
                    # Simulate erratic behavior by not updating the timer
                else:
                    if pos in affected_lights:
                        affected_lights.discard(pos) # Light might recover
                    traffic_lights[pos]['timer'] = (traffic_lights[pos]['timer'] + 1) % CYCLE_PERIOD
            else:
                traffic_lights[pos]['timer'] = (traffic_lights[pos]['timer'] + 1) % CYCLE_PERIOD

    # Draw roads
    for i in range(GRID_SIZE):
        color = ORANGE if cyberattack_active and (i + i // ROAD_INTERVAL) % 2 == 0 else GRAY # Adjusted visual indicator
        for j in range(GRID_SIZE):
            if is_on_road(i, j):
                pygame.draw.rect(screen, color, (i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw traffic lights
    for pos, data in traffic_lights.items():
        light_state = get_light_state(pos)
        if cyberattack_active and pos in affected_lights:
            color = random.choice([RED, GREEN, YELLOW])
        else:
            color = GREEN if light_state == 'NS' else RED
        pygame.draw.circle(screen, color, (pos[0] * CELL_SIZE + CELL_SIZE // 2, pos[1] * CELL_SIZE + CELL_SIZE // 2), TRAFFIC_LIGHT_SIZE)

    # Move and draw cars
    if not accident and not game_paused:
        for car in cars[:]:
            car.move(cars) # Pass the list of all cars for collision detection

    for car in cars:
        # Draw car
        pygame.draw.rect(screen, BLUE, (car.x * CELL_SIZE + 5, car.y * CELL_SIZE + 5, CAR_SIZE, CAR_SIZE))

    # Display accident alert
    if accident:
        alert_text = large_font.render("ACCIDENT!", True, RED)
        text_rect = alert_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(alert_text, text_rect)
        if accident_location:
            coord_text = font.render(f"Coordinates: ({accident_location[0]}, {accident_location[1]})", True, RED)
            coord_rect = coord_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
            screen.blit(coord_text, coord_rect)

    # Display cyberattack information
    if cyberattack_active:
        cyber_alert_text = large_font.render("CYBER ATTACK!", True, RED)
        cyber_rect = cyber_alert_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
        screen.blit(cyber_alert_text, cyber_rect)
        if affected_lights:
            lights_text = font.render(f"Affected Lights: {sorted(list(affected_lights))}", True, RED)
            lights_rect = lights_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + 40))
            screen.blit(lights_text, lights_rect)
        else:
            lights_text = font.render("Affected Lights: None (yet)", True, RED)
            lights_rect = lights_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + 40))
            screen.blit(lights_text, lights_rect)
        pause_text = font.render(f"Game Paused for {CYBERATTACK_PAUSE} seconds...", True, RED)
        pause_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(pause_text, pause_rect)

    pygame.display.flip()
    clock.tick(5)  # Slow down the simulation

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and accident:
                reset_game() # Still allow manual reset

pygame.quit()