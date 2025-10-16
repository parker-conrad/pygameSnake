import pygame
import random

pygame.init()

BLACK = (0, 0, 0)
GREY = (30, 30, 30)
YELLOW = (255, 255, 0)
GREEN = (67, 82, 61)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
RED = (125, 25, 25)
BORDERS = True


COLOR1 = BLACK
COLOR2 = GREEN
COLOR3 = GREEN
COLOR4 = RED

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 20
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()



def gen(num):
    return set([(random.randrange(0, GRID_HEIGHT), random.randrange(0, GRID_WIDTH)) for i in range(num)])

def draw_grid(positions):
    screen.fill(COLOR3)
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, COLOR1, (*top_left, TILE_SIZE, TILE_SIZE))
    if BORDERS == True:
        for row in range(GRID_HEIGHT):
            pygame.draw.line(screen, COLOR2, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

        for col in range(GRID_WIDTH):
            pygame.draw.line(screen, COLOR2, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def draw_grid_apple(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, COLOR4, (*top_left, TILE_SIZE, TILE_SIZE))
    if BORDERS == True:
        for row in range(GRID_HEIGHT):
            pygame.draw.line(screen, COLOR2, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

        for col in range(GRID_WIDTH):
            pygame.draw.line(screen, COLOR2, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))

def get_snake(snake, mome, apple):
    newSnake = snake
    x, y = snake[len(snake) - 1]
    app = apple[0]
    if mome == 0:
        y = y - 1
        coord = (x, y)
    elif mome == 1:
        x = x - 1
        coord = (x, y)
    elif mome == 2:
        y = y + 1
        coord = (x, y)
    elif mome == 3:
        x = x + 1
        coord = (x, y)
    newSnake.append(coord)
    if app not in newSnake:
        del newSnake[0]
    return newSnake

def apple_pos(snake):
    coord = (random.randrange(0, GRID_WIDTH-1), random.randrange(0, GRID_HEIGHT-1))
    def inside(coord):
        if coord in snake:
            coord = (random.randrange(0, GRID_WIDTH-1), random.randrange(0, GRID_HEIGHT-1))
            inside(coord)
        else:
            return coord
    coord = inside(coord)
    return coord

def snake_in_apple(snake, apple):
    coord = apple[0]
    if coord in snake:
        coord = apple_pos(snake)
    return coord

def snake_die (snake):
    newSnake = snake
    x, y = snake[len(snake) - 1]
    coord = (x, y)
    if x<0 or y<0 or x>GRID_WIDTH-1 or y>GRID_HEIGHT-1:
        newSnake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    if len(snake) != len(set(snake)):
        newSnake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    return newSnake

def mome_die (snake, mome):
    x, y = snake[len(snake) - 1]
    newMome = mome
    if x<0 or y<0 or x>GRID_WIDTH-1 or y>GRID_HEIGHT-1:
        newMome = 0
    if len(snake) != len(set(snake)):
        newMome = 0
    return newMome

def apple_die (snake, apple):
    x, y = snake[len(snake) - 1]
    coord = apple[0]
    if x<0 or y<0 or x>GRID_WIDTH-1 or y>GRID_HEIGHT-1:
        coord = apple_pos(snake)
    if len(snake) != len(set(snake)):
        coord = apple_pos(snake)
    return [coord]

def update_die (snake, update_frequency):
    x, y = snake[len(snake) - 1]
    u_f = update_frequency
    if x<0 or y<0 or x>GRID_WIDTH-1 or y>GRID_HEIGHT-1:
        u_f = 17
    if len(snake) != len(set(snake)):
        u_f = 17
    return u_f

def main():
    running = True
    playing = True
    count = 0
    stopper = 0
    update_frequency = 17

    positions = set()
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snakePrev = 0
    apple = [apple_pos(snake)]
    mome = 0
    while running:
        clock.tick(FPS)

        if playing:
            count += 1

        if len(snake) > snakePrev and update_frequency > 1:
            update_frequency = update_frequency - .15
            snakePrev = snakePrev + 1

        if count >= update_frequency:
            count = 0
            mome = mome_die(snake, mome)
            apple = apple_die(snake, apple)
            snake = snake_die(snake)
            #snake = apple_in_snake(snake, apple, mome)
            snake = get_snake(snake, mome, apple)
            apple = [snake_in_apple(snake, apple)]
            positions = snake + apple
            update_frequency = update_die(snake, update_frequency)
            if stopper > 0:
                stopper = stopper - 1

        pygame.display.set_caption("Playing" if playing else "Stopped")

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing

                if event.key == pygame.K_w and event.key != pygame.K_d  and event.key != pygame.K_a  and event.key != pygame.K_s:
                    if mome !=2:
                        mome = 0
                    elif len(snake) < 2:
                        mome = 0

                if event.key == pygame.K_a and event.key != pygame.K_d  and event.key != pygame.K_w  and event.key != pygame.K_s:
                    if stopper == 0:
                        stopper = 1
                        if len(snake)>0 and mome != 3:
                            mome = 1
                        elif len(snake) < 2:
                            mome = 1

                if event.key == pygame.K_s and event.key != pygame.K_d  and event.key != pygame.K_a  and event.key != pygame.K_w:
                    if stopper == 0:
                        stopper = 1
                        if len(snake)>0 and mome != 0:
                            mome = 2
                        elif len(snake) < 2:
                            mome = 2

                if event.key == pygame.K_d and event.key != pygame.K_w  and event.key != pygame.K_a  and event.key != pygame.K_s:
                    if stopper == 0:
                        stopper = 1
                        if len(snake)>0 and mome != 1:
                            mome = 3
                        elif len(snake) < 2:
                            mome = 3

                if event.key == pygame.K_3:
                    global COLOR1
                    global COLOR2
                    global COLOR3
                    global COLOR4
                    global BORDERS
                    COLOR1 = BLACK
                    COLOR2 = BLACK
                    COLOR3 = GREEN
                    BORDERS = True

                if event.key == pygame.K_1:
                    COLOR1 = BLACK
                    COLOR2 = GREEN
                    COLOR3 = GREEN
                    BORDERS = True

                if event.key == pygame.K_2:
                    COLOR1 = BLACK
                    COLOR2 = GREEN
                    COLOR3 = GREEN
                    BORDERS = False

                if event.key == pygame.K_4:
                    if COLOR4 == RED:
                        COLOR4 = BLACK
                    else:
                        COLOR4 = RED

        draw_grid(positions)
        draw_grid_apple(apple)
        pygame.display.update()

    pygame.quit()

if __name__ == '__main__':
    main()