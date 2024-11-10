import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 800
CELL_SIZE = 50
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
SHAPES = [
    [[1, 1, 1, 1]],  # I-shape
    [[1, 1, 1], [0, 1, 0]],  # T-shape
    [[1, 1, 0], [0, 1, 1]],  # S-shape
    [[0, 1, 1], [1, 1, 0]],  # Z-shape
    [[1, 1, 1], [1, 0, 0]],  # L-shape
    [[1, 1, 1], [0, 0, 1]],  # J-shape
    [[1, 1], [1, 1]],  # O-shape
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tetris')
def create_grid():
    return [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[y][x], (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_shape(shape, offset, color):
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, color, ((offset[0] + x) * CELL_SIZE, (offset[1] + y) * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def valid_position(shape, offset, grid):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= GRID_WIDTH or y + off_y >= GRID_HEIGHT:
                    return False
                if grid[y + off_y][x + off_x] != BLACK:
                    return False
    return True

def clear_rows(grid):
    cleared = 0
    new_grid = [row for row in grid if any(cell == BLACK for cell in row)]
    cleared = GRID_HEIGHT - len(new_grid)
    return [[BLACK] * GRID_WIDTH] * cleared + new_grid
def game():
    clock = pygame.time.Clock()
    grid = create_grid()
    shape = random.choice(SHAPES)
    shape_position = [GRID_WIDTH // 2 - len(shape[0]) // 2, 0]
    fall_time = 0

    running = True
    while running:
        screen.fill(WHITE)
        fall_time += clock.get_rawtime()
        clock.tick(60)

        if fall_time / 1000 >= 0.5:
            fall_time = 0
            shape_position[1] += 1
            if not valid_position(shape, shape_position, grid):
                shape_position[1] -= 1
                for y, row in enumerate(shape):
                    for x, cell in enumerate(row):
                        if cell:
                            grid[shape_position[1] + y][shape_position[0] + x] = BLUE
                grid = clear_rows(grid)
                shape = random.choice(SHAPES)
                shape_position = [GRID_WIDTH // 2 - len(shape[0]) // 2, 0]
                if not valid_position(shape, shape_position, grid):
                    running = False  

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    shape_position[0] -= 1
                    if not valid_position(shape, shape_position, grid):
                        shape_position[0] += 1
                elif event.key == pygame.K_RIGHT:
                    shape_position[0] += 1
                    if not valid_position(shape, shape_position, grid):
                        shape_position[0] -= 1
                elif event.key == pygame.K_DOWN:
                    shape_position[1] += 1
                    if not valid_position(shape, shape_position, grid):
                        shape_position[1] -= 1
                elif event.key == pygame.K_UP:
                    shape = list(zip(*shape[::-1]))
                    if not valid_position(shape, shape_position, grid):
                        shape = list(zip(*shape))[::-1]

        draw_grid(grid)
        draw_shape(shape, shape_position, RED)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    game()
