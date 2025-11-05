from numpy import random

class Map:
    def __init__(self, rows=15, cols=40):
        self.rows = rows
        self.cols = cols
        self.grid = self.gen_map()
        self.render_map()

    def gen_map(self):
        matrix = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(1 if random.randint(0, 10) < 3 else 0)
            matrix.append(row)
        return matrix

    def render_map(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.grid[i][j] = "X" if self.grid[i][j] == 1 else "-"

    def dim(self):
        return (self.rows, self.cols)

    def show(self):
        for i in range(self.rows):
            print("".join(self.grid[i]))

m = Map()
m.show()
