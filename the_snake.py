import sys
from random import randint as rd

import pygame as pg

# Константы.
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = SCREEN_WIDTH // GRID_SIZE, SCREEN_HEIGHT // GRID_SIZE
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)
COLORS = {
    "board": (0, 0, 0), "border": (93, 216, 228),
    "apple": (255, 0, 0), "snake": (0, 255, 0)
}
START_SPEED, MAX_LENGTH = 10, 10

# Инициализация
pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Змейка')
clock = pg.time.Clock()


def draw_rect(position, color):
    rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
    pg.draw.rect(screen, color, rect)
    pg.draw.rect(screen, COLORS["border"], rect, 1)


class GameObject:
    def __init__(self, body_color):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def get_position(self):
        return self.position

    def set_random_position(self, occupied_positions):
        while True:
            self.position = (
                rd(0, GRID_WIDTH - 1) * GRID_SIZE,
                rd(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if self.position not in occupied_positions:
                break


class Apple(GameObject):
    def __init__(self):
        super().__init__(COLORS["apple"])
        self.set_random_position([])

    def draw(self):
        draw_rect(self.position, self.body_color)


class Snake(GameObject):
    def __init__(self):
        super().__init__(COLORS["snake"])
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def get_head_position(self):
        return self.positions[0]

    def update_direction(self):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        head_x, head_y = self.positions[0]
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT
        )

        if new_head in self.positions:
            self.reset()
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT

    def draw(self):
        for position in self.positions:
            draw_rect(position, self.body_color)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    global speed
    for event in pg.event.get():
        is_quit = event.type == pg.QUIT
        is_escape = event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE

        if is_quit or is_escape:
            pg.quit()
            sys.exit()

        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT
            elif event.key == pg.K_EQUALS:  # '+' на большинстве клавиатур
                speed = min(speed + 2, 30)
            elif event.key == pg.K_MINUS:
                speed = max(speed - 2, 5)


def main():
    global speed
    speed = START_SPEED
    snake, apple = Snake(), Apple()

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.get_position():
            snake.length += 1
            apple.set_random_position(snake.positions)

        screen.fill(COLORS["board"])
        snake.draw()
        apple.draw()

        if snake.length >= MAX_LENGTH:
            print("Победа! Достигнута максимальная длина змейки.")
            pg.quit()
            sys.exit()

        pg.display.update()
        clock.tick(speed)


if __name__ == '__main__':
    main()
