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
        pyxel.init(self.width, self.height)

        self.num_elevators = 5
        self.idx = 0
        self.elevators = Elevators(self.num_elevators, self.width, self.height)
        self.cat = Cat(0, 0)
        self.score_text = "Score {:05d}"

        pyxel.sound(3).set("g1a#1d#2b2", "s", "7654", "s", 9)
        pyxel.sound(4).set("g1c2f2a2c#2f#3", "p", "6", "s", 4)
        pyxel.sound(5).set("a3d#3a#2f#2d2b1g1d#1", "s", "77654321", "s", 10)

        pyxel.image(0).load(0, 0, "assets/cat_16x16.png")

        self.play_bgm()
        pyxel.run(self.update, self.draw)

    def update(self):
        self.check_input()
        self.cat.center(self.elevators.get(self.idx).pos())
        self.elevators.update()

    def draw(self):
        pyxel.cls(0)
        self.elevators.draw(self.idx)
        self.cat.draw()
        score = self.score_text.format(self.idx)
        scorelen = len(score) * 4
        pyxel.text(self.width - scorelen, 0, score, 10)

    def check_input(self):
        if pyxel.btnr(pyxel.KEY_SPACE):
            self.check_collision()

    def play_bgm(self):
        # bgm
        a = "c3e2g2c3 e2g2c3e2"
        b = "c3d2g2c3 d2g2c3d2"
        pyxel.sound(0).set(a * 3 + b * 1, "t", "2", "f", 30)

        a = "g1c2d2e2 e2e2f2f2"
        b = "e2e2e2c2 c2c2c2c2"
        c = "g2g2g2d2 d2d2d2d2"
        pyxel.sound(1).set(a + b + a + c, "s", "4", "nnnn vvnn vvff nvvf", 30)

        pyxel.sound(2).set("c1c1f0f0a0a0g0g0", "p", "4", "nf", 120)

        pyxel.play(0, 0, loop=True)
        pyxel.play(1, 1, loop=True)
        pyxel.play(2, 2, loop=True)

    def check_collision(self):
        enext = self.elevators.get(self.idx + 1)
        if (
            # Add some paddding for easier gameplay
            self.cat.y + 20 >= enext.y
            and self.cat.y + self.cat.height <= enext.y + enext.size
        ):
            pyxel.play(3, 4)
            self.idx += 1
        else:
            pyxel.play(3, 5)
            self.idx = 0


App()
