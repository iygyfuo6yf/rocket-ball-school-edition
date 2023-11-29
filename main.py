import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BALL_RADIUS = 20
GRAVITY = 0.5
FLAP_FORCE = 8
PIPE_WIDTH = 50
PIPE_VELOCITY = 3
GAP = 200
GAP_CHANGE = 1
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (135, 206, 235)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Ball')

# Fonts
font = pygame.font.Font(None, 36)

# Ball variables
ball_x = SCREEN_WIDTH // 4
ball_y = SCREEN_HEIGHT // 2
ball_velocity = 0

# Pipes
pipes = []

def create_pipe():
    random_pos = random.randint(50, SCREEN_HEIGHT - 250)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH + 20, random_pos, PIPE_WIDTH, SCREEN_HEIGHT - random_pos)
    top_pipe = pygame.Rect(SCREEN_WIDTH + 20, 0, PIPE_WIDTH, random_pos - GAP)
    return bottom_pipe, top_pipe

pipes.append(create_pipe())

# Game variables
score = 0
high_score = 0
game_over = False
mouse_clicked = False
time_since_last_click = pygame.time.get_ticks()

clock = pygame.time.Clock()

def display_high_score():
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, SCREEN_HEIGHT - 40))

running = True
while running:
    screen.fill(BLUE)

    if not game_over:
        if score == 0:
            display_high_score()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    ball_velocity = -FLAP_FORCE
                    time_since_last_click = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                ball_velocity = -FLAP_FORCE * 2
                mouse_clicked = True
                time_since_last_click = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_clicked = False
                time_since_last_click = pygame.time.get_ticks()
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pipes.clear()
                    pipes.append(create_pipe())
                    ball_y = SCREEN_HEIGHT // 2
                    ball_velocity = 0
                    score = 0
                    game_over = False
                    time_since_last_click = pygame.time.get_ticks()

        ball_velocity += GRAVITY
        ball_y += ball_velocity

        if mouse_clicked:
            ball_velocity = -FLAP_FORCE * 2

        if BALL_RADIUS < ball_y < SCREEN_HEIGHT - BALL_RADIUS:
            pygame.draw.circle(screen, RED, (ball_x, int(ball_y)), BALL_RADIUS)

        for pipe_pair in pipes[:]:
            pygame.draw.rect(screen, GREEN, pipe_pair[0])
            pygame.draw.rect(screen, GREEN, pipe_pair[1])

            pipe_pair[0].x -= PIPE_VELOCITY
            pipe_pair[1].x -= PIPE_VELOCITY

            if pipe_pair[0].right < 0:
                pipes.remove(pipe_pair)
                new_pipe_pair = create_pipe()
                pipes.append(new_pipe_pair)
                score += 1

            if (pipe_pair[0].colliderect(
                    pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2))
                    or pipe_pair[1].colliderect(
                        pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_RADIUS * 2, BALL_RADIUS * 2))):
                game_over = True

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if score > high_score:
            high_score = score

        current_time = pygame.time.get_ticks()
        if ball_y - BALL_RADIUS > SCREEN_HEIGHT or (current_time - time_since_last_click > 1000 and current_time != 0):
            game_over = True

    else:
        game_over_text = font.render("Game Over", True, WHITE)
        instruction_text = font.render("Press SPACE to restart", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
        screen.blit(instruction_text, (SCREEN_WIDTH // 2 - 140, SCREEN_HEIGHT // 2 + 20))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                pipes.clear()
                pipes.append(create_pipe())
                ball_y = SCREEN_HEIGHT // 2
                ball_velocity = 0
                score = 0
                game_over = False
                time_since_last_click = pygame.time.get_ticks()

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
