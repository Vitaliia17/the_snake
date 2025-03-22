import sys
from random import choice

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
START_SPEED, MAX_LENGTH = 10, 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Базовый класс игрового объекта."""

    def __init__(self, body_color=None):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw_rect(self, position, color):
        """Рисует квадрат на экране."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):
        """Абстрактный метод для отрисовки объектов."""


class Apple(GameObject):
    """Класс для яблока."""

    def __init__(self, occupied_positions=None):
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(occupied_positions or [])

    def randomize_position(self, occupied_positions):
        """Генерирует случайную позицию, избегая занятых мест."""
        available_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied_positions
        ]
        if available_positions:
            self.position = choice(available_positions)

    def draw(self):
        """Рисует яблоко на экране."""
        self.draw_rect(self.position, self.body_color)


class Snake(GameObject):
    """Класс для змейки."""

    def __init__(self):
        """Инициализирует объект змейки и вызывает метод сброса состояния."""
        super().__init__(SNAKE_COLOR)
        self.reset()
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None

    def reset(self):
        """Сбрасывает состояние змейки до начального."""
        self.length = 1
        self.positions = [
            (SCREEN_WIDTH // 2 // GRID_SIZE * GRID_SIZE,
             SCREEN_HEIGHT // 2 // GRID_SIZE * GRID_SIZE)
        ]
        self.direction = choice([UP, DOWN, LEFT, RIGHT])
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Перемещает змейку в текущем направлении."""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.positions.insert(
            0,
            (
                (head_x + direction_x * GRID_SIZE) % SCREEN_WIDTH,
                (head_y + direction_y * GRID_SIZE) % SCREEN_HEIGHT
            )
        )
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Рисует змейку на экране."""
        if self.last:
            pg.draw.rect(
                screen, BOARD_BACKGROUND_COLOR,
                (*self.last, GRID_SIZE, GRID_SIZE)
            )
        for position in self.positions:
            self.draw_rect(position, self.body_color)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш."""
    global speed
    for event in pg.event.get():
        if (event.type == pg.QUIT
                or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE)):
            pg.quit()
            sys.exit()

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and snake.direction != DOWN:
                snake.next_direction = UP
            elif event.key == pg.K_DOWN and snake.direction != UP:
                snake.next_direction = DOWN
            elif event.key == pg.K_LEFT and snake.direction != RIGHT:
                snake.next_direction = LEFT
            elif event.key == pg.K_RIGHT and snake.direction != LEFT:
                snake.next_direction = RIGHT


def main():
    """Основная функция запуска игры."""
    speed = START_SPEED
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка: съела яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        # Проверка: столкнулась с собой
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()

        pg.display.update()
        clock.tick(speed)


if __name__ == '__main__':
    pg.init()
    main()
