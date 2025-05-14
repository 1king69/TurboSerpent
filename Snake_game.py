
# importing libraries
import pygame
import time
import random

# Window size
window_x = 720
window_y = 480

# defining colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)
yellow = pygame.Color(255, 255, 0)

# Initialising pygame
pygame.init()

# Initialise game window
pygame.display.set_caption('TurboSerpent - Select Level')
game_window = pygame.display.set_mode((window_x, window_y))

# FPS (frames per second) controller
fps = pygame.time.Clock()

# Game levels with corresponding speeds
levels = {
    1: 5,
    2: 8,
    3: 12,
    4: 16,
    5: 20,
}


# Selecting level
def select_level():
    selecting = True
    font = pygame.font.SysFont('times new roman', 30)
    title_font = pygame.font.SysFont('times new roman', 50)

    while selecting:
        game_window.fill(black)
        title_surface = title_font.render('Select Level (1-5)', True, yellow)
        title_rect = title_surface.get_rect(center=(window_x / 2, window_y / 6))
        game_window.blit(title_surface, title_rect)

        info_surface = font.render('Press number keys 1 to 5 to select difficulty', True, white)
        info_rect = info_surface.get_rect(center=(window_x / 2, window_y / 3))
        game_window.blit(info_surface, info_rect)

        for level in range(1, 6):
            level_text = f'Level {level}: Speed {levels[level]}'
            level_surface = font.render(level_text, True, white)
            level_rect = level_surface.get_rect(center=(window_x / 2, window_y / 3 + 40 + level * 30))
            game_window.blit(level_surface, level_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_1, pygame.K_KP1]:
                    return 1
                if event.key in [pygame.K_2, pygame.K_KP2]:
                    return 2
                if event.key in [pygame.K_3, pygame.K_KP3]:
                    return 3
                if event.key in [pygame.K_4, pygame.K_KP4]:
                    return 4
                if event.key in [pygame.K_5, pygame.K_KP5]:
                    return 5
        fps.tick(30)


# displaying Score function
def show_score(choice, color, font, size, score):
    # creating font object score_font
    score_font = pygame.font.SysFont(font, size)

    # create the display surface object score_surface
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # create a rectangular object for the text surface object
    score_rect = score_surface.get_rect()

    # displaying text
    game_window.blit(score_surface, score_rect)


# game over function
def game_over(score):
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 50)

    # creating a text surface on which text will be drawn
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)

    # create a rectangular object for the text surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (window_x / 2, window_y / 4)

    # blit will draw the text on screen
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # after 2 seconds we will quit the program
    time.sleep(2)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


def game(level):
    snake_speed = levels[level]

    # defining snake default position
    snake_position = [100, 50]

    # defining first 4 blocks of snake body
    snake_body = [[100, 50],
                  [90, 50],
                  [80, 50],
                  [70, 50]
                  ]
    # fruit position
    fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                      random.randrange(1, (window_y // 10)) * 10]

    fruit_spawn = True

    # setting default snake direction towards right
    direction = 'RIGHT'
    change_to = direction

    # initial score
    score = 0

    while True:
        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # If two keys pressed simultaneously we don't want snake to move into two directions simultaneously
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

        # Snake body growing mechanism
        # if fruits and snakes collide then scores will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            score += 10
            fruit_spawn = False
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x // 10)) * 10,
                              random.randrange(1, (window_y // 10)) * 10]

        fruit_spawn = True
        game_window.fill(black)

        for pos in snake_body:
            pygame.draw.rect(game_window, green,
                             pygame.Rect(pos[0], pos[1], 10, 10))
        pygame.draw.rect(game_window, white, pygame.Rect(
            fruit_position[0], fruit_position[1], 10, 10))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x - 10:
            break
        if snake_position[1] < 0 or snake_position[1] > window_y - 10:
            break

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                break

        else:
            # displaying score continuously
            show_score(1, white, 'times new roman', 20, score)

            # Updating window title with level info
            pygame.display.set_caption('TurboSerpent - Level {level} - Score {score}')
            # Refresh game screen
            pygame.display.update()

            # Frame Per Second /Refresh Rate
            fps.tick(snake_speed)
            continue
        break  # break if snake touched its own body or out of bounds

    game_over(score)


def main():
    level = select_level()
    game(level)


if __name__ == '__main__':
    main()

