from random import randrange, random
import time
from copy import deepcopy
import ctypes
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QWidget

INITIAL_HP = 100


class Application(QWidget):
    def __init__(self):
        super().__init__()
        self.name = QFileDialog.getOpenFileName(self, 'Файл с записью', '', 'Файл (*.txt)')[0]

    def get_name(self):
        self.close()
        return self.name


# TODO проверить какой метод условного перхода лучше
class Cell:
    def __init__(self, world, x, y, hp=INITIAL_HP):
        self.world, self.x, self.y, self.hp = world, x, y, hp

    def get_color(self, mode=0):
        if not mode:
            return 128, 128, 128
        elif mode == 1:
            return 0, 0, 0
        elif mode == 2:
            return 128, 128, 128

    def run(self):
        pass

    def get_hp(self):
        return self.hp

    def death(self):
        self.world.destroy(self)

    def get_coords(self):
        return self.x, self.y

    def set_coords(self, x, y):
        self.x, self.y = x, y


class Organism(Cell):

    def __init__(self, world, x, y, hp, legacy=False):
        super().__init__(world, x, y, hp)

        self.nap = randrange(0, 8)
        if not legacy:
            self.genome = [randrange(0, 64) for _ in range(64)]
        else:
            self.genome = legacy
        self.color = [
            [0, 255, 0], [128, 128, 128], [0, 0, 0], [0, 0, 0], [0, 0, 0]]  # TODO добавить деление по типу генома.
        self.current_command, self.age = 0, 0
        self.commands = [self.c0, self.c1, self.c2, self.c3, self.c4, self.c5, self.c6, self.c7]

    def c0(self):
        self.hp += self.world.get_foto(*self.get_coords())
        self.color[1][0] = self.color[1][0] - 1 if self.color[1][0] > 1 else + 0
        self.color[1][1] = self.color[1][1] + 1 if self.color[1][1] < 254 else + 0
        return True

    def c1(self):
        self.hp += self.world.get_minerals(*self.get_coords())
        self.color[1][0] = self.color[1][0] - 1 if self.color[1][0] > 1 else + 0
        self.color[1][2] = self.color[1][2] + 1 if self.color[1][2] < 254 else + 0
        return True

    def c2(self):
        if self.get_hp() <= INITIAL_HP:
            self.current_command = (self.current_command + 1) % 64
        else:
            self.current_command = (self.current_command + 2) % 64

    def get_target(self):
        return self.world.get_cell(*self.get_new_coords())

    def c3(self):
        try:
            offset = TL.index(type(self.get_target())) + 1
        except ValueError:
            print(self.get_target())
            print(type(self.get_target()))
            print(type(self.get_target()) in TL)
            print(TL.index(type(self.get_target())))

        self.current_command = (self.current_command + offset) % 64

    def c4(self):
        self.nap = (self.nap + self.genome[(self.current_command + 1) % 64] % 8) % 8
        self.current_command = (self.current_command + 1) % 64

    def c5(self):
        if type(self.get_target()) == int:
            self.world.move(self)
            self.current_command = (self.current_command + 1) % 64
            self.get_damage(1)
            return True
        else:
            self.current_command = (self.current_command + TL.index(type(self.get_target()))) % 64

    def c6(self):
        eat = False
        target = self.get_target()
        if type(target) == Organism:
            target.get_damage(self.get_hp() // 4)
            self.hp += 100
            if target.get_hp() <= 0:
                target.death()
                self.hp += 500
            self.get_damage(5)
            return True
        elif type(self.get_target()) == Cell:
            self.hp += 500
            self.get_target().death()
            return True
        else:
            self.current_command = (self.current_command + 1) % 64  # TODO  пока простая модель
        if eat:
            self.color[1][0] = self.color[1][0] + 4 if self.color[1][0] < 254 else + 0
            self.color[1][1] = self.color[1][1] - 1 if self.color[1][1] > 1 else + 0
            self.color[1][2] = self.color[1][2] - 1 if self.color[1][1] > 1 else + 0

    def c7(self):
        if type(self.get_target()) == int:
            self.hp //= 2
            self.world.add_organism(*self.get_new_coords(), self.get_hp(), self.genome)
            return True
        else:
            self.current_command = (self.current_command + 1) % 64

    def get_color(self, mode=0):
        return self.color[mode]

    def get_nap(self):
        return self.nap

    def get_new_coords(self):
        x, y = self.get_coords()
        if self.get_nap() in (0, 6, 7):
            x = (X_SIZE + x - 1) % X_SIZE
        elif self.get_nap() in (2, 3, 4):
            x = (X_SIZE + x + 1) % X_SIZE
        if self.get_nap() in (4, 5, 6):
            y = (Y_SIZE + y - 1) % Y_SIZE
        elif self.get_nap() in (0, 1, 2):
            y = (Y_SIZE + y + 1) % Y_SIZE
        return x, y

    def get_damage(self, damage):
        self.hp -= damage

    def death(self):
        self.world.death(self)

    def get_genome(self):
        return self.genome

    def cycle_check(self):
        for command in set(self.past_commands):
            if self.past_commands.count(command) > 15:
                return True

    def run(self):
        self.past_commands = []
        self.current_command = 0
        self.get_damage(1)
        if self.hp <= 0:
            self.death()
            return
        if self.get_hp() > MAX_HP:
            if 7 in self.genome:
                self.current_command = self.genome.index(7)
                self.commands[7]()
            else:
                for i in range(8):
                    if self.get_target() == int:
                        self.commands[7]()
                        return
                    else:
                        self.nap = (self.nap + 1) % 8
                self.world.replacement(self)
        while True:
            self.past_commands.append(self.genome[self.current_command])
            if len(self.past_commands) > 100:
                break
            if self.cycle_check():  # TODO нужно поддерживать количество команд
                break
            if len(self.past_commands) > 20 and min(self.past_commands) >= len(self.commands):
                break
            if self.genome[self.current_command] < len(self.commands):
                if self.commands[self.genome[self.current_command]]():
                    break
            else:
                self.current_command = (self.current_command + self.genome[self.current_command]) % 64
            if self.hp <= 0:
                self.death()
                break


class Universe:
    def __init__(self):
        self.cycles_count = 0
        self.field = [[0 for j in range(Y_SIZE)] for i in range(X_SIZE)]
        self.cells, self.organisms, self.time = [], [], 0
        self.start()

    def start(self):
        for _ in range(INITIAL_COUNT_OF_CELLS):
            x, y = randrange(1, X_SIZE), randrange(1, Y_SIZE)
            if not self.field[x][y]:
                self.add_organism(x, y)

    def add_organism(self, x, y, hp=INITIAL_HP, legacy=False):
        if legacy:
            legacy = deepcopy(legacy)
            if random() <= PROBABILITY_OF_MUTATION:
                legacy[randrange(0, len(legacy) - 1)] = randrange(0, 64)
        organism = Organism(self, x, y, hp, legacy)
        self.field[x][y] = organism
        self.organisms.append((organism, (x, y)))

    def get_count_of_organisms(self):
        return len(self.organisms)

    def get_age(self):
        return self.cycles_count

    def get_time(self):
        return self.time

    def get_data(self):
        # TODO дописать дополнительную информацию
        data = ''
        for cell in self.cells:
            data += str(cell[0].get_coords())
        return data

    def step(self, data=False):  # TODO попробовать многопроцессность
        if data:
            organisms = ''
        t = time.time()
        for organism in self.organisms:
            organism[0].run()
            if organism[0].get_hp() >= MAX_HP:
                organism[0].color[2] = [255, 0, 0]
            else:
                organism[0].color[2] = [int(organism[0].get_hp() * 255 / MAX_HP), 0,
                                        int((MAX_HP - organism[0].get_hp()) * 255 / MAX_HP)]
            if data:
                organisms += f'{organism[0].get_coords(), organism[0].color, organism[0].get_genome()}'

        self.cycles_count += 1
        self.time = time.time() - t
        if __name__ == '__main__':
            print(self.get_age(), self.get_count_of_organisms(), self.get_time())
        if data:
            if self.get_age() % 10 == 0:
                print(self.get_age(), self.get_count_of_organisms(), self.get_time())
            return ' '.join(self.get_data()), str(organisms)

    def get_foto(self, x, y):
        # TODO зональное распределение
        return 20

    def get_minerals(self, x, y):
        # TODO зональное распределение
        return 20

    def get_cell(self, x, y):
        return self.field[x][y]

    def death(self, organism):
        x, y = organism.get_coords()
        try:
            del self.organisms[self.organisms.index((organism, organism.get_coords()))]
        except Exception:
            del self.organisms[-1]
        self.cells.append((Cell(self, x, y), (x, y)))
        self.field[x][y] = self.cells[-1][0]

    def replacement(self, organism):
        self.death(organism)
        self.destroy(self.cells[-1][0])
        x, y = organism.get_coords()
        legacy = deepcopy(organism.get_genome())
        self.add_organism(x, y, legacy=legacy)

    def destroy(self, cell):
        del self.cells[self.cells.index((cell, cell.get_coords()))]
        self.field[cell.get_coords()[0]][cell.get_coords()[1]] = 0

    def move(self, organism):
        x, y = organism.get_coords()
        self.field[x][y] = 0
        try:
            self.organisms[self.organisms.index((organism, (x, y)))] = (organism, organism.get_new_coords())
        except:
            if self.organisms[-1][1] == (x, y):
                self.organisms[-1] = (organism, organism.get_new_coords())
        x, y = organism.get_new_coords()
        self.field[x][y] = organism
        organism.set_coords(x, y)


MAX_HP = 1500
X_SIZE, Y_SIZE = 600, 300
user32 = ctypes.windll.user32
CELL_SIZE = (min((user32.GetSystemMetrics(0), user32.GetSystemMetrics(1))) - 150) // Y_SIZE
print(CELL_SIZE)
INITIAL_COUNT_OF_CELLS = 100
TL = (Organism, Cell, int)
PROBABILITY_OF_MUTATION = 0.3
if __name__ == '__main__':
    world = Universe()
    while True:
        world.step()
