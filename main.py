import pygame as p
from random import choice

LEFT = 1
UP = 2
RIGHT = -1
DOWN = -2

FPS = 120
SEGMENT_COLOR = (255, 255, 255)
FOOD_COLOR = (255, 0, 0)

SEGMENT_WIDTH, SEGMENT_HEIGHT, SPACE_BET_SEGMENTS = 30, 30, 2
ROWS, COLUMNS = 20, 20

SCREEN_WIDTH = (COLUMNS * SEGMENT_WIDTH + COLUMNS * SPACE_BET_SEGMENTS) + SPACE_BET_SEGMENTS
SCREEN_HEIGHT = (ROWS * SEGMENT_HEIGHT + ROWS * SPACE_BET_SEGMENTS) + SPACE_BET_SEGMENTS

p.init()
window = p.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
timer = p.time.Clock()

all_sprites = p.sprite.Group()
foods = p.sprite.Group()
segments = []

game_over = False
direction_changed = False

possible_positions = [(SPACE_BET_SEGMENTS + SEGMENT_WIDTH * c + SPACE_BET_SEGMENTS * c,
          SPACE_BET_SEGMENTS + SEGMENT_HEIGHT * r + SPACE_BET_SEGMENTS * r)
         for c in range(COLUMNS) for r in range(ROWS)]


class Segment(p.sprite.Sprite):
    def __init__(self, x, y, width, height, color, direction):
        super().__init__()

        self.image = p.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y

        self.direction = direction


class Food(p.sprite.Sprite):
    def __init__(self, x, y, width, height, color):
        super().__init__()

        self.image = p.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.color = color

        self.rect.x = x
        self.rect.y = y


def add_segment():

    tail = segments[-1]
    segment_x = segment_y = 0

    if tail.direction == LEFT:
        segment_x = tail.rect.x + SEGMENT_WIDTH + SPACE_BET_SEGMENTS
        segment_y = tail.rect.y
    elif tail.direction == UP:
        segment_x = tail.rect.x
        segment_y = tail.rect.y + SEGMENT_HEIGHT + SPACE_BET_SEGMENTS
    elif tail.direction == RIGHT:
        segment_x = tail.rect.x - SEGMENT_WIDTH - SPACE_BET_SEGMENTS
        segment_y = tail.rect.y
    elif tail.direction == DOWN:
        segment_x = tail.rect.x
        segment_y = tail.rect.y - SEGMENT_HEIGHT - SPACE_BET_SEGMENTS

    new_segment = Segment(segment_x, segment_y, SEGMENT_WIDTH, SEGMENT_HEIGHT, SEGMENT_COLOR, tail.direction)

    segments.append(new_segment)
    all_sprites.add(new_segment)


def spawn_food():
    fit_positions = [pos for pos in possible_positions for seg in segments
                     if pos[0] != seg.rect.x and pos[1] != seg.rect.y]
    food_pos = choice(fit_positions)
    new_food = Food(food_pos[0], food_pos[1], SEGMENT_WIDTH, SEGMENT_HEIGHT, FOOD_COLOR)

    foods.add(new_food)
    # all_sprites.add(new_food)


def food_collision():
    food_ = [f for f in foods][0]
    if segments[0].rect.x == food_.rect.x and segments[0].rect.y == food_.rect.y:
        add_segment()
        food_.kill()
        spawn_food()


def move_head():
    global direction_changed

    head = segments[0]

    if head.direction == LEFT:
        head.rect.x -= SEGMENT_WIDTH + SPACE_BET_SEGMENTS
    elif head.direction == UP:
        head.rect.y -= SEGMENT_HEIGHT + SPACE_BET_SEGMENTS
    elif head.direction == RIGHT:
        head.rect.x += SEGMENT_WIDTH + SPACE_BET_SEGMENTS
    elif head.direction == DOWN:
        head.rect.y += SEGMENT_HEIGHT + SPACE_BET_SEGMENTS
    direction_changed = False


def move_segments():

    i = len(segments) - 1
    while i > 0:
        segments[i].rect.x = segments[i - 1].rect.x
        segments[i].rect.y = segments[i - 1].rect.y
        segments[i].direction = segments[i - 1].direction

        i -= 1


def collapse():

    for seg in segments[3:]:
        if seg.rect.x == segments[0].rect.x and seg.rect.y == segments[0].rect.y: return True
    if segments[0].rect.x > SCREEN_WIDTH or segments[0].rect.x < 0\
            or segments[0].rect.y > SCREEN_HEIGHT or segments[0].rect.y < 0: return True
    return False


def update():
    global game_over

    move_segments()
    move_head()

    if collapse():
        game_over = True


def show_game_over_window():
    font = p.font.SysFont("comicsansms", 30)
    text = font.render("Game Over", False, (255, 255, 0))

    dark_effect = p.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_effect.set_alpha(128)
    dark_effect.fill((0, 0, 0))

    window.blit(dark_effect, (0, 0))
    window.blit(text, (SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT / 2 - 10))


def main():
    global direction_changed

    head = Segment(SPACE_BET_SEGMENTS, SPACE_BET_SEGMENTS, SEGMENT_WIDTH, SEGMENT_HEIGHT, SEGMENT_COLOR, RIGHT)

    segments.append(head)
    all_sprites.add(head)

    spawn_food()

    # for r in range(ROWS):
    #     for c in range(COLUMNS):
    #         all_sprites.add(Segment(
    #             SPACE_BET_SEGMENTS + SEGMENT_WIDTH * c + SPACE_BET_SEGMENTS * c,
    #             SPACE_BET_SEGMENTS + SEGMENT_HEIGHT * r + SPACE_BET_SEGMENTS * r,
    #             SEGMENT_WIDTH, SEGMENT_HEIGHT,
    #             SEGMENT_COLOR
    #         ))

    run = True
    counter = 0

    while run:

        for i in p.event.get():
            if i.type == p.QUIT: run = False

        keys = p.key.get_pressed()
        if keys[p.K_LEFT] and segments[0].direction != RIGHT and not direction_changed:
            segments[0].direction = LEFT
            direction_changed = True
        elif keys[p.K_UP] and segments[0].direction != DOWN and not direction_changed:
            segments[0].direction = UP
            direction_changed = True
        elif keys[p.K_RIGHT] and segments[0].direction != LEFT and not direction_changed:
            segments[0].direction = RIGHT
            direction_changed = True
        elif keys[p.K_DOWN] and segments[0].direction != UP and not direction_changed:
            segments[0].direction = DOWN
            direction_changed = True

        if counter == 13 and not game_over:

            update()
            food_collision()
            counter = 0

        window.fill((0, 0, 0))
        for food in foods:
            p.draw.circle(window, food.color, (food.rect.x + SEGMENT_WIDTH / 2, food.rect.y + SEGMENT_HEIGHT / 2), SEGMENT_WIDTH / 2)
        all_sprites.draw(window)

        if game_over:
            show_game_over_window()

        p.display.flip()

        timer.tick(FPS)
        counter += 1


if __name__ == "__main__":
    main()
