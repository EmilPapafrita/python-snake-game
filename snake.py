import pygame
import time
import random

snake_speed = 15

# Window size
window_x = 720
window_y = 480

# colors
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
redOrange = pygame.Color(100, 33, 29)
yellow = pygame.Color(255, 255, 191)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('Snake Game 🐍')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# defining snake default position
snake_position = [250, 250]
# defining first 4 blocks of snake body
snake_body = [ [250, 250],[240, 250],[230, 250],[220, 250] ]

# fruit position
fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                  random.randrange(1, (window_y // 10)) * 10]

fruit_spawn = True

# setting default snake direction towards
# right
direction = 'RIGHT'
change_to = direction

# initial score
score = 0


# displaying Score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)  # creating font object
    score_surface = score_font.render('Score : ' + str(score), True, color)  # creating display surface object
    score_rect = score_surface.get_rect()  # creating rectangular object for text
    game_window.blit(score_surface, score_rect)  # displaying text


# game over function
def game_over():
    my_font = pygame.font.SysFont('times new roman', 50)  # creating font object

    game_over_surface = my_font.render(                      # creating a text surface
        'Your Score is : ' + str(score), True, red)  # where text will be drawn

    game_over_rect = game_over_surface.get_rect() # rectangular object text surface object

    game_over_rect.midtop = (window_x / 2, window_y / 4)  # setting position of the text

    game_window.blit(game_over_surface, game_over_rect)  # blit will draw the text on screen
    pygame.display.flip()

    time.sleep(2)  # after 2 seconds we will quit the program
    pygame.quit()  # deactivating pygame library
    quit()  # quit program

# Load array of multiple fruit images
fruit_images = [
    pygame.transform.scale(pygame.image.load("apple.png"), (20, 20)),
    pygame.transform.scale(pygame.image.load("mango.png"), (20, 20)),
    pygame.transform.scale(pygame.image.load("orange.png"), (20, 20)),
]

# Load the grass image
grass_img = pygame.image.load("grass.png")
grass_img = pygame.transform.scale(grass_img, (window_x, window_y))

# Initialize the fruit image
fruit_image = pygame.transform.scale(pygame.image.load("apple.png"), (20, 20))

# Main Function
while True:

    # handling key events
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # If two keys pressed simultaneously
    # we don't want snake to move into two
    # directions simultaneously
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    # Moving the snake
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Snake body growing mechanism if fruits and snakes collide then scores will be incremented by 1.
    # Since image of fruit takes up 4 blocks instead of 1 each conditional is needed to cover all 4
    snake_body.insert(0, list(snake_position))
    if (
            snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]
    ) or (
            snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1] + 10
    ) or (
            snake_position[0] == fruit_position[0] + 10 and snake_position[1] == fruit_position[1]
    ) or (
            snake_position[0] == fruit_position[0] + 10 and snake_position[1] == fruit_position[1] + 10
    ):
        score += 1
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_image = random.choice(fruit_images)  # Select a random fruit image
        fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                          random.randrange(1, (window_y // 10)) * 10]
        fruit_spawn = True

    game_window.blit(grass_img, (0, 0))  # Using grass image as background

    for i, pos in enumerate(snake_body):  # To get the stripes on snake body
        if i % 2 == 0:
            pygame.draw.rect(game_window, redOrange, pygame.Rect(pos[0], pos[1], 10, 10))
        else:
            pygame.draw.rect(game_window, yellow, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the fruit image
    game_window.blit(fruit_image, (fruit_position[0], fruit_position[1]))

    # Game Over conditions
    if snake_position[0] < 0 or snake_position[0] > window_x - 10:
        game_over()
    if snake_position[1] < 0 or snake_position[1] > window_y - 10:
        game_over()

    # Touching the snake body
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # displaying score continuously
    show_score(1, white, 'times new roman', 20)
    # Refresh game screen
    pygame.display.update()
    # Frame Per Second /Refresh Rate
    fps.tick(snake_speed)