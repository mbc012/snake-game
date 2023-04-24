import pygame
import random


FOOD_TOTAL = 5
GRID_SIZE = 20
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class SnakeRect(pygame.Rect):
    def __init__(self, x, y, width, height, head=False):
        super().__init__(x, y, width, height)
        self.head = head


snake_vel = 0
snake_last = [(0, 0)]
snake_head = SnakeRect(0, 0, 20, 20, True)
snake_rects = [snake_head, *[SnakeRect(-20*(i+1), 0, 20, 20) for i in range(1)]]

food_postions = []


def draw_screen_grid():
    for x in range(0, SCREEN_WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (x, 0), (x, SCREEN_HEIGHT))

    for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (255, 255, 255), (0, y), (SCREEN_WIDTH, y))


def get_future_snake_location(new_pos):
    snake_positions = [new_pos]
    for r in snake_rects:
        snake_positions.append((r.x, r.y))
    return snake_positions


def get_current_snake_location():
    snake_positions = []
    for r in snake_rects:
        snake_positions.append((r.x, r.y))
    return snake_positions


def add_snake():
    snake_rects.append(SnakeRect(snake_last[0][0], snake_last[0][1], 20, 20))


def draw_snake():
    head_x, head_y = snake_head.x, snake_head.y
    if snake_vel == 0:
        head_x += GRID_SIZE
    elif snake_vel == 1:
        head_y -= GRID_SIZE
    elif snake_vel == 2:
        head_x -= GRID_SIZE
    elif snake_vel == 3:
        head_y += GRID_SIZE

    snake_pos = get_future_snake_location(new_pos=(head_x, head_y))
    snake_last[0] = snake_pos[-1]

    for i, r in enumerate(snake_rects):
        # update pos
        r.x, r.y = snake_pos[i]

        # draw
        if r.head:
            pygame.draw.rect(screen, (255, 0, 0), r)
        else:
            pygame.draw.rect(screen, (255, 255, 255), r)


def add_food():
    snake_location = get_current_snake_location()

    while True:
        x = random.randrange(0, SCREEN_WIDTH, GRID_SIZE)
        y = random.randrange(0, SCREEN_HEIGHT, GRID_SIZE)
        if (x, y) not in snake_location:
            food_postions.append((x, y))
            break


def draw_food():
    for x, y in food_postions:
        pygame.draw.rect(screen, (0, 0, 255), (x, y, GRID_SIZE, GRID_SIZE))


def check_food():
    if food_postions.__len__() < FOOD_TOTAL:
        add_food()
    check_food_collision()


def check_food_collision():
    snake_pos = get_current_snake_location()
    for x, y in food_postions:
        if (x, y) in snake_pos:
            food_postions.remove((x, y))
            add_snake()


def check_snake_collision():
    snake_pos = get_current_snake_location()
    # Check snake outside of screen
    for x, y in snake_pos:
        if x < 0 or x > (SCREEN_WIDTH) or y < 0 or y > (SCREEN_HEIGHT):
            print("Game Over")
            exit()

    # Check snake collision on self
    for x, y in snake_pos:
        if snake_pos.count((x, y)) > 1:
            print("Game Over")
            exit()


def start_screen():
    # TODO: Finish start screen

    start_button = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 50, 100, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 + 50, 100, 50)

    pygame.draw.rect(screen, (255, 0, 0), start_button)
    pygame.draw.rect(screen, (255, 0, 0), quit_button)


if __name__ == "__main__":
    while True:
        #start_screen()

        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # check key inputs
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                snake_vel = 2
            elif keys[pygame.K_RIGHT]:
                snake_vel = 0
            elif keys[pygame.K_UP]:
                snake_vel = 1
            elif keys[pygame.K_DOWN]:
                snake_vel = 3

            screen.fill((0, 0, 0))
            draw_screen_grid()

            draw_snake()
            check_snake_collision()
            check_food()
            draw_food()

            pygame.display.flip()
            clock.tick(5)