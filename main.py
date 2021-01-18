import pygame #
from random import choice

def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls['left'] = False
        next.walls['right'] = False
    elif dx == -1:
        current.walls['right'] = False
        next.walls['left'] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls['top'] = False
        next.walls['bottom'] = False
    elif dy == -1:
        current.walls['bottom'] = False
        next.walls['top'] = False

raz = width, height = 802, 602
size = 20
cols, rows = width // size, height // size

pygame.init()
window = pygame.display.set_mode(raz)
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def fillCell(self):
        x, y = self.x * size, self.y * size
        pygame.draw.rect(window, pygame.Color('red'), (x + 2, y + 2, size - 2, size - 2))

    def draw(self):
        x, y = self.x * size, self.y * size
        if self.visited:
            pygame.draw.rect(window, pygame.Color('white'), (x, y, size, size))

        if self.walls['top']:
            pygame.draw.line(window, pygame.Color('black'), (x, y), (x + size, y), 3)
        if self.walls['bottom']:
            pygame.draw.line(window, pygame.Color('black'), (x + size, y + size), (x , y + size), 3)
        if self.walls['right']:
            pygame.draw.line(window, pygame.Color('black'), (x + size, y), (x + size, y + size), 3)
        if self.walls['left']:
            pygame.draw.line(window, pygame.Color('black'), (x, y + size), (x, y), 3)

    def checkUtil(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.checkUtil(self.x, self.y - 1)
        right = self.checkUtil(self.x + 1, self.y)
        bottom = self.checkUtil(self.x, self.y + 1)
        left = self.checkUtil(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if right and not right.visited:
            neighbors.append(right)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False

grid = [Cell(col, row) for row in range(rows) for col in range(cols)]
currentCell = grid[0]
stack = []


while True:
    window.fill(pygame.Color('yellow'))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    [cell.draw() for cell in grid]
    currentCell.visited = True
    currentCell.fillCell()

    nextCell = currentCell.check_neighbors()
    if nextCell:
        nextCell.visited = True
        stack.append(currentCell)
        remove_walls(currentCell, nextCell)
        currentCell = nextCell
    elif stack:
        currentCell = stack.pop()
    pygame.display.flip()
    clock.tick(100)
