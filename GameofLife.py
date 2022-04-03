import pygame
from pygame.locals import *
import random
from pprint import pprint as pp
import time
import pygame
from pygame.locals import *
import random
from pprint import pprint as pp
import time


class Cell:
    def __init__(self, x, y):
        self.state = 0
        self.x = x
        self.y = y

    def is_alive(self):
        return self.state


class CellList:
    def __init__(self, nrow=1, ncol=1, filename=''):
        self.nrow = nrow
        self.ncol = ncol
        self.filename = filename
        self.i = 0
        self.state = 0
        if filename == '':
            self.field = [[Cell(i, j) for i in range(self.ncol)] for j in range(self.nrow)]
        else:
            self.read_file()

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < self.ncol * self.nrow:
            res = self.field[(self.i) // self.ncol][(self.i) % self.ncol]
            self.i += 1
            return res
        raise StopIteration()
        pass

    def __str__(self):
        res = [[cell.state for cell in row] for row in self.field]
        return str(res)

    def read_file(self):
        f = open(self.filename)
        s = f.read()
        f.close()
        col = 0
        self.nrow = 1
        self.ncol = len(s[0:s.find('\n')])
        while s.find('\n') != -1:
            num = s.find('\n')
            s = s[0:num] + s[num + 1:]
            self.nrow += 1
        self.field = [[Cell(i, j) for i in range(self.ncol)] for j in range(self.nrow)]
        j = 0
        for i in s:
            self.field[j // self.ncol][j % self.ncol].state = int(i)
            j += 1


class GameOfLife:
    def __init__(self, width=640, height=480, cell_size=10, speed=0.1):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        # http://www.pygame.org/docs/ref/draw.html#pygame.draw.line
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self):
        pygame.init()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        self.field = self.cell_list(randomize=True)
        running = True
        count = 0
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_cell_list(self.field)
            pygame.display.flip()
            self.field = self.update_cell_list(self.field)
            time.sleep(self.speed)
        pygame.quit()

    def cell_list(self, randomize=False):
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1.
        В противном случае клетка считается мертвой, то
        есть ее значение равно 0.
        Если параметр randomize = True, то создается список, где
        каждая клетка может быть равновероятно живой или мертвой.
        """
        if randomize:
            cell_list = CellList(nrow=self.cell_height, ncol=self.cell_width)
            for cell in cell_list:
                cell.state = random.randint(0, 1)
            return cell_list.field

    def draw_cell_list(self, rects):
        """
        Отображение списка клеток 'rects' с закрашиванием их в
        соответствующе цвета
        Rect - координаты прямоугольника в формате (x, y, длина стороны a, длина стороны b)
        """
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if rects[i][j].state:
                    pygame.draw.rect(self.screen, pygame.Color('green'), (
                    j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), (
                    j * self.cell_size + 1, i * self.cell_size + 1, self.cell_size - 1, self.cell_size - 1))

    def get_neighbours(self, cell):
        """
        Вернуть список соседних клеток для клетки cell.
        Соседними считаются клетки по горизонтали,
        вертикали и диагоналям, то есть во всех
        направлениях.
        """
        x, y = cell
        newX = x - 1
        newY = y - 1
        neigh = []
        for i in range(3):
            for j in range(3):
                if (x == i + newX) and (y == j + newY):
                    continue
                if (newX + i < 0) or (newY + j < 0):
                    continue
                if (newX + i >= self.cell_height) or (newY + j >= self.cell_width):
                    continue
                neigh.append(Cell(i + newX, j + newY))
        return neigh

    def nAlive(self, i, j, cell_list):
        numAlive = 0
        for k in self.get_neighbours((i, j)):
            x, y = k.x, k.y
            if cell_list[x][y].state == 1:
                numAlive += 1
        return numAlive

    def update_cell_list(self, cell_list):
        """
        Обновление состояния клеток
        """
        newField = [[Cell(i, j) for j in range(self.cell_width)] for i in range(self.cell_height)]
        numAlive = 0

        for i in range(self.cell_height):
            for j in range(self.cell_width):
                if (cell_list[i][j].state == 0) and (self.nAlive(i, j, cell_list) == 3):
                    newField[i][j].state = 1
                elif (cell_list[i][j].state == 1) and (self.nAlive(i, j, cell_list) in [2, 3]):
                    newField[i][j].state = 1
        return newField


if __name__ == '__main__':
    game = GameOfLife(700, 500, 50)
    game.run()
