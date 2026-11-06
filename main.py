import pygame
import random

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
STONE_COLOR = (128, 128, 128)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

SPEED = 12

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pygame.display.set_caption("Змейка")

clock = pygame.time.Clock()


class GameObject:
    def __init__(self, body_color):
        self.body_color = body_color
        self.position = None

    def set_position(self, snake_position):
        all_positions = [
            [x * GRID_SIZE, y * GRID_SIZE]
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        ]

        clean_position = [pos for pos in all_positions if pos not in snake_position]
        self.position = random.choice(clean_position)

    def draw(self):
        pygame.draw.rect(
            screen, self.body_color, (*self.position, GRID_SIZE, GRID_SIZE)
        )


class Snake:
    def __init__(self):
        self.body_color = (0, 255, 0)
        self.lenght = 1
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.positions = [[center_x, center_y]]
        self.direction = LEFT
        self.last = []

    def draw(self):
        for pos in self.positions:
            pygame.draw.rect(screen, self.body_color, (*pos, GRID_SIZE, GRID_SIZE))

        if self.last:
            pygame.draw.rect(screen, (0, 0, 0), (*self.last, GRID_SIZE, GRID_SIZE))

    def move(self):
        self.last = self.positions[-1]
        cur_x, cur_y = self.positions[0]
        dir_x, dir_y = self.direction

        new_x = (cur_x + dir_x * GRID_SIZE) % SCREEN_WIDTH
        new_y = (cur_y + dir_y * GRID_SIZE) % SCREEN_HEIGHT

        last_pos = self.positions.copy()
        for i in range(1, len(self.positions)):
            self.positions[i] = last_pos[i - 1]

        self.positions[0] = [new_x, new_y]

    def reset(self):
        center_x = (GRID_WIDTH // 2) * GRID_SIZE
        center_y = (GRID_HEIGHT // 2) * GRID_SIZE
        self.positions = [[center_x, center_y]]
        self.lenght = 1
        self.last = []


class Apple(GameObject):
    def __init__(self, body_color):
        super().__init__(body_color)

    def set_position(self, snake_position, stone_positions=[]):
        all_positions = [
            [x * GRID_SIZE, y * GRID_SIZE]
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        ]

        clean_position = [
            pos
            for pos in all_positions
            if pos not in snake_position and pos not in stone_positions
        ]
        self.position = random.choice(clean_position)


class Stone(GameObject):
    def __init__(self, body_color):
        super().__init__(body_color)

    def set_position(self, snake_position, apple_position, stones_position):
        all_positions = [
            [x * GRID_SIZE, y * GRID_SIZE]
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
        ]

        clean_position = [
            pos
            for pos in all_positions
            if pos not in snake_position
            and pos not in apple_position
            and pos not in stones_position
        ]
        self.position = random.choice(clean_position)


def handle_keys(game_object):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.direction = RIGHT


def main():
    pygame.init()
    snake = Snake()
    apple = Apple(APPLE_COLOR)
    apple.set_position(snake_position=snake.positions)
    stone_count = 0
    stones_positions = []
    stones = []
    running = True

    while running:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if (
            snake.positions[0] in snake.positions[1:]
            or snake.positions[0] in stones_positions
        ):
            screen.fill((0, 0, 0))
            snake.reset()
            apple.set_position(snake.positions)
            stones.clear()
            stones_positions = []
            stone_count = 0

        if snake.positions[0] == apple.position:
            snake.lenght += 1
            snake.positions.append(snake.positions[-1])
            apple.set_position(snake.positions, stones_positions)

            if snake.lenght >= 5:
                stone = Stone(STONE_COLOR)
                stone.set_position(snake.positions, apple.position, stones_positions)
                stones.append(stone)
                stone_count += 1
                stones_positions.append(stone.position)

                if stone_count > 5:
                    pos = stones_positions.pop(0)
                    stones.pop(0)
                    pygame.draw.rect(screen, (0, 0, 0), (*pos, GRID_SIZE, GRID_SIZE))
                    stone_count = 5

        snake.draw()
        apple.draw()
        for s in stones:
            s.draw()
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
