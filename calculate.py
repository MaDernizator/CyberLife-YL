from frame import Universe
from frame import Application
from PyQt5.QtWidgets import QApplication
import sys
import sqlite3

app = QApplication(sys.argv)
ex = Application()
ex.show()

FILE_NAME = ex.get_name()
BLOCK_SIZE = 50
data = []


def step():
    block = ''
    for _ in range(BLOCK_SIZE):
        block += str(world.get_age()) + ' ' + str(world.get_count_of_organisms()) + '\t'
        block += str(world.step(data=True))[1:-1] + '\n'
    file.write(block)


world = Universe()
with open(FILE_NAME, 'a') as file:  # TODO дописать создание файла, если он не существует (для объёма)
    while True:
        step()
        if world.get_count_of_organisms() <= 0:
            break

con = sqlite3.connect('reports.db')
cur = con.cursor()
cur.execute(f"""INSERT INTO launches(duration) VALUES('{world.get_age()}')""")
con.commit()
