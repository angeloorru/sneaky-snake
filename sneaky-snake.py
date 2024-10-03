import pygame
import random

# Initialize pygame
pygame.init()

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# Set display dimensions
WIDTH = 600
HEIGHT = 400

# Define block size and speed
BLOCK_SIZE = 20
SNAKE_SPEED = 10

# Create display
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define clock for controlling speed
clock = pygame.time.Clock()

# Font settings
font_style = pygame.font.SysFont(None, 35)


def initialize_game():
    x, y = WIDTH / 2, HEIGHT / 2
    x_change, y_change = 0, 0
    snake_list = []
    snake_length = 1
    food_x, food_y = generate_food_position()
    return x, y, x_change, y_change, snake_list, snake_length, food_x, food_y


def generate_food_position():
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    return food_x, food_y


def display_score(score):
    score_text = font_style.render("Score: " + str(score), True, GREEN)
    display.blit(score_text, [0, 0])


def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(display, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])


def game_over_message():
    msg = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
    display.blit(msg, [WIDTH / 6, HEIGHT / 3])


def handle_game_over():
    game_over_message()
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True  # Quit the game when window is closed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return True  # Quit the game
                elif event.key == pygame.K_c:
                    return False  # Restart the game


def handle_input(x_change, y_change):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return None, None  # Quit the game when window is closed
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                return -BLOCK_SIZE, 0
            elif event.key == pygame.K_RIGHT:
                return BLOCK_SIZE, 0
            elif event.key == pygame.K_UP:
                return 0, -BLOCK_SIZE
            elif event.key == pygame.K_DOWN:
                return 0, BLOCK_SIZE
    return x_change, y_change


def update_snake(snake_list, snake_length, x, y):
    snake_head = [x, y]
    snake_list.append(snake_head)

    if len(snake_list) > snake_length:
        del snake_list[0]

    # Check for snake collision with itself
    for block in snake_list[:-1]:
        if block == snake_head:
            return True  # Game close due to collision

    return False  # No collision


def snake_game():
    game_over = False

    # Initialize game state
    x, y, x_change, y_change, snake_list, snake_length, food_x, food_y = initialize_game()

    while not game_over:

        # Handle player input
        x_change, y_change = handle_input(x_change, y_change)
        if x_change is None:
            game_over = True
            continue  # Quit the game

        # Update snake's position
        x += x_change
        y += y_change

        # Check for boundary collisions
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            if handle_game_over():
                game_over = True
            else:
                x, y, x_change, y_change, snake_list, snake_length, food_x, food_y = initialize_game()
            continue

        # Update the screen
        display.fill(BLACK)
        pygame.draw.rect(display, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Check if the snake collides with itself
        if update_snake(snake_list, snake_length, x, y):
            if handle_game_over():
                game_over = True
            else:
                x, y, x_change, y_change, snake_list, snake_length, food_x, food_y = initialize_game()
            continue

        draw_snake(snake_list)
        display_score(snake_length - 1)
        pygame.display.update()

        # Check if snake eats food
        if x == food_x and y == food_y:
            food_x, food_y = generate_food_position()
            snake_length += 1

        clock.tick(SNAKE_SPEED)

    pygame.quit()


# Handle KeyboardInterrupt
try:
    snake_game()
except KeyboardInterrupt:
    pygame.quit()
    print("Game interrupted and exited cleanly.")
