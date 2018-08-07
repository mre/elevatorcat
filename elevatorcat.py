import pyxel
from enum import Enum
import random


class Elevator:
    def __init__(self, pos, size, speed, ymin, ymax):
        self.size = size
        self.x = pos * self.size
        self.y = random.randrange(ymin, ymax)
        self.speed = speed
        self.ymax = ymax
        self.ymin = ymin

    def draw(self, hightlight):
        if hightlight:
            pyxel.rect(self.x, self.y, self.x + self.size, self.y + self.size, 8)
        else:
            pyxel.rectb(self.x, self.y, self.x + self.size, self.y + self.size, 9)

    def update(self):
        self.y += self.speed
        if self.y > self.ymax:
            self.y = -self.size
        if self.y + self.size < self.ymin:
            self.y += self.ymax

    def pos(self):
        return (self.x, self.y)


class Elevators:
    def __init__(self, num, width, height):
        self.num = num
        self.width = width
        self.height = height
        self.elevators = self._create_elevators()

    def _create_elevators(self):
        width = int(self.width / self.num)
        elevators = []
        direction = 1
        for i in range(0, self.width):
            speed = random.uniform(1.0, 2.0)
            elevators.append(Elevator(i, 20, direction * speed, 0, self.width))
            direction = -direction
        return elevators

    def get(self, idx):
        return self.elevators[idx]

    def update(self):
        for elevator in self.elevators:
            elevator.update()

    def draw(self, idx):
        for i, elevator in enumerate(self.elevators):
            elevator.draw(i == idx)


class Cat:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16

    def draw(self):
        pyxel.blt(self.x, self.y, 0, 0, 0, self.width, self.height, 5)

    def center(self, pos):
        (self.x, self.y) = pos


class App:
    def __init__(self):
        self.width = 160
        self.height = 120
        self.num_elevators = 5
        self.idx = 0
        self.elevators = Elevators(self.num_elevators, self.width, self.height)
        self.cat = Cat(0, 0)
        pyxel.init(self.width, self.height)
        pyxel.image(0).load(0, 0, "assets/cat_16x16.png")
        pyxel.run(self.update, self.draw)

    def update(self):
        self.check_input()
        self.cat.center(self.elevators.get(self.idx).pos())
        # self.cat.update()
        self.elevators.update()

    def draw(self):
        pyxel.cls(0)
        self.elevators.draw(self.idx)
        self.cat.draw()
        # pyxel.text(80, 60, "Hallo Anna", 1)

    def check_input(self):
        if pyxel.btnr(pyxel.KEY_RIGHT):
            self.idx += 1
        if pyxel.btnr(pyxel.KEY_LEFT):
            self.idx -= 1
        # if pyxel.btn(pyxel.KEY_SPACE):
        #     self.y = (self.y + 10) % self.height


App()
