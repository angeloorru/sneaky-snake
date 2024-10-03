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
SNAKE_SPEED = 15

# Create display
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Define clock for controlling speed
clock = pygame.time.Clock()

# Font settings
font_style = pygame.font.SysFont(None, 35)

def display_score(score):
    score_text = font_style.render("Score: " + str(score), True, GREEN)
    display.blit(score_text, [0, 0])

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(display, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def game_over_message():
    msg = font_style.render("Game Over! Press Q-Quit or C-Play Again", True, RED)
    display.blit(msg, [WIDTH / 6, HEIGHT / 3])

def snake_game():
    game_over = False
    game_close = False

    # Initial position of the snake
    x = WIDTH / 2
    y = HEIGHT / 2

    # Initial movement of the snake
    x_change = 0
    y_change = 0

    # Snake initial settings
    snake_list = []
    snake_length = 1

    # Random position for food
    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE

    while not game_over:

        while game_close:
            display.fill(BLACK)
            game_over_message()
            display_score(snake_length - 1)
            pygame.display.update()

            # Handle game over events
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        snake_game()

        # Handle game events (keyboard input)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP:
                    y_change = -BLOCK_SIZE
                    x_change = 0
                elif event.key == pygame.K_DOWN:
                    y_change = BLOCK_SIZE
                    x_change = 0

        # Update the position of the snake
        x += x_change
        y += y_change

        # Check for boundary collisions
        if x >= WIDTH or x < 0 or y >= HEIGHT or y < 0:
            game_close = True

        display.fill(BLACK)

        # Draw food
        pygame.draw.rect(display, RED, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        # Update snake position
        snake_head = []
        snake_head.append(x)
        snake_head.append(y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for snake collision with itself
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)
        display_score(snake_length - 1)

        # Update display
        pygame.display.update()

        # Check if snake eats the food
        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / BLOCK_SIZE) * BLOCK_SIZE
            snake_length += 1

        # Set the game speed
        clock.tick(SNAKE_SPEED)

    pygame.quit()

# Handle KeyboardInterrupt
try:
    snake_game()
except KeyboardInterrupt:
    pygame.quit()
    print("Game interrupted and exited cleanly.")
