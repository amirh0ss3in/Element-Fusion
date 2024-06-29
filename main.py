import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 700
GRID_SIZE = 5
CELL_SIZE = WIDTH // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ELEMENTS = [
    ('H', 'Hydrogen', 1, 1.008, (141, 182, 205)),
    ('He', 'Helium', 2, 4.003, (155, 205, 155)),
    ('Li', 'Lithium', 3, 6.941, (205, 155, 155)),
    ('Be', 'Beryllium', 4, 9.012, (205, 173, 0)),
    ('B', 'Boron', 5, 10.811, (238, 180, 34)),
    ('C', 'Carbon', 6, 12.011, (139, 69, 19)),
    ('N', 'Nitrogen', 7, 14.007, (144, 238, 144)),
    ('O', 'Oxygen', 8, 15.999, (70, 130, 180)),
    ('F', 'Fluorine', 9, 18.998, (238, 130, 238)),
    ('Ne', 'Neon', 10, 20.180, (255, 62, 150)),
    ('Na', 'Sodium', 11, 22.990, (171, 130, 255)),
    ('Mg', 'Magnesium', 12, 24.305, (50, 205, 50)),
    ('Al', 'Aluminum', 13, 26.982, (165, 42, 42)),
    ('Si', 'Silicon', 14, 28.086, (85, 107, 47)),
    ('P', 'Phosphorus', 15, 30.974, (255, 140, 0)),
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Element Fusion")

grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
score = 0

def move(direction):
    global score
    moved = False
    if direction in ('LEFT', 'RIGHT'):
        for y in range(GRID_SIZE):
            line = [grid[y][x] for x in range(GRID_SIZE) if grid[y][x]]
            if direction == 'RIGHT':
                line.reverse()
            new_line = []
            i = 0
            while i < len(line):
                if i + 1 < len(line) and line[i] == line[i+1]:
                    current_index = next((index for index, e in enumerate(ELEMENTS) if e[0] == line[i]), None)
                    if current_index is not None and current_index < len(ELEMENTS) - 1:
                        new_line.append(ELEMENTS[current_index + 1][0])
                        score += ELEMENTS[current_index + 1][2]
                    else:
                        new_line.append(line[i])
                    i += 2
                    moved = True
                else:
                    new_line.append(line[i])
                    i += 1
            new_line += [None] * (GRID_SIZE - len(new_line))
            if direction == 'RIGHT':
                new_line.reverse()
            for x in range(GRID_SIZE):
                if grid[y][x] != new_line[x]:
                    moved = True
                grid[y][x] = new_line[x]
    else:  # UP or DOWN
        for x in range(GRID_SIZE):
            line = [grid[y][x] for y in range(GRID_SIZE) if grid[y][x]]
            if direction == 'DOWN':
                line.reverse()
            new_line = []
            i = 0
            while i < len(line):
                if i + 1 < len(line) and line[i] == line[i+1]:
                    current_index = next((index for index, e in enumerate(ELEMENTS) if e[0] == line[i]), None)
                    if current_index is not None and current_index < len(ELEMENTS) - 1:
                        new_line.append(ELEMENTS[current_index + 1][0])
                        score += ELEMENTS[current_index + 1][2]
                    else:
                        new_line.append(line[i])
                    i += 2
                    moved = True
                else:
                    new_line.append(line[i])
                    i += 1
            new_line += [None] * (GRID_SIZE - len(new_line))
            if direction == 'DOWN':
                new_line.reverse()
            for y in range(GRID_SIZE):
                if grid[y][x] != new_line[y]:
                    moved = True
                grid[y][x] = new_line[y]
    return moved

def is_game_over():
    return all(all(cell is not None for cell in row) for row in grid)

def add_new_element():
    empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[y][x] is None]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[y][x] = random.choice(['H', 'He'])

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            cell_rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (100, 100, 100), cell_rect, 1)
            
            if grid[y][x]:
                element = next((e for e in ELEMENTS if e[0] == grid[y][x]), None)
                if element:
                    # Draw element background
                    inner_rect = cell_rect.inflate(-10, -10)
                    pygame.draw.rect(screen, element[4], inner_rect, border_radius=int(CELL_SIZE * 0.15))
                    pygame.draw.rect(screen, WHITE, inner_rect, 2, border_radius=int(CELL_SIZE * 0.15))
                    
                    # Draw element symbol
                    font_size = int(CELL_SIZE * 0.4)
                    font = pygame.font.Font(pygame.font.match_font('arial'), font_size)
                    text = font.render(element[0], True, WHITE)
                    text_rect = text.get_rect(center=cell_rect.center)
                    screen.blit(text, text_rect)
                    
                    # Draw atomic number
                    font_size = int(CELL_SIZE * 0.2)
                    font = pygame.font.Font(pygame.font.match_font('arial'), font_size)
                    text = font.render(str(element[2]), True, WHITE)
                    text_rect = text.get_rect(topleft=(cell_rect.left + int(CELL_SIZE * 0.1), cell_rect.top + int(CELL_SIZE * 0.1)))
                    screen.blit(text, text_rect)
                    
                    # Draw atomic mass
                    text = font.render(f"{element[3]:.2f}", True, WHITE)
                    text_rect = text.get_rect(bottomright=(cell_rect.right - int(CELL_SIZE * 0.1), cell_rect.bottom - int(CELL_SIZE * 0.1)))
                    screen.blit(text, text_rect)

def draw_background():
    for y in range(HEIGHT):
        r = int(44 + (y / HEIGHT) * 26)
        g = int(62 + (y / HEIGHT) * 18)
        b = int(80 + (y / HEIGHT) * 20)
        pygame.draw.line(screen, (r, g, b), (0, y), (WIDTH, y))

def main():
    global score
    clock = pygame.time.Clock()
    add_new_element()
    add_new_element()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                moved = False
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    moved = move('LEFT')
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    moved = move('RIGHT')
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    moved = move('UP')
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    moved = move('DOWN')
                
                if moved:
                    add_new_element()
                
                if is_game_over():
                    print(f"Game Over! Final Score: {score}")
                    pygame.quit()
                    sys.exit()

        draw_background()
        draw_grid()
        font = pygame.font.Font(pygame.font.match_font('arial'), 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 40))
        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()