from PyQt5.QtWidgets import QApplication
from frame import X_SIZE, Y_SIZE, CELL_SIZE
import sys
import pygame
from frame import Application

FPS = 10
mode = 0


def next(data):
    def cell_display(cells):
        cells = cells.split(') (')
        new_cells = []
        for cell in cells:
            new_cell = ''
            for symbol in cell:
                if symbol != ' ':
                    new_cell += symbol
            new_cells.append(new_cell)
        cells = new_cells

        for cell in cells:
            pygame.draw.rect(screen, pygame.Color(*(0, 0, 0) if mode == 1 else (128, 128, 128)), (
                int(cell.split(',')[0]) * CELL_SIZE + 5, int(cell.split(',')[1]) * CELL_SIZE + 5, CELL_SIZE, CELL_SIZE),
                             0)

    screen.fill((0, 0, 0) if not mode or mode == 2 else (255, 255, 255))
    pygame.draw.rect(screen, pygame.Color(255, 0, 0), (0, 0, X_SIZE * CELL_SIZE + 10, Y_SIZE * CELL_SIZE + 10), 5)
    font = pygame.font.Font(None, 40)
    text_age = font.render(f"{age}", True, (255, 0, 0))
    text_count = font.render(f"{data.split()[1]}", True, (255, 0, 0))
    screen.blit(text_age, (width // 3, Y_SIZE * CELL_SIZE + 20))
    screen.blit(text_count, (width // 3 * 2, Y_SIZE * CELL_SIZE + 20))
    # width, height = X_SIZE * CELL_SIZE, Y_SIZE * CELL_SIZE
    data = data.split('\t')[1][3:]
    if data[0].isdigit():
        cells = data.split(")', '")[0]
        cell_display(cells)
        data = data.split(")', '")[1]

    organisms = ''.join(data.split(','))
    organisms = organisms.split('(')[2:][::2]
    for organism in organisms:
        color = organism.split('[[')[1].split(']]')[0]
        color = color.split('] [')
        color = [[int(j) for j in i.split()] for i in color]
        color = color[mode]
        pygame.draw.rect(screen, pygame.Color(*color), (
            int(organism.split(') [')[0].split()[0]) * CELL_SIZE + 5,
            int(organism.split(') [')[0].split()[1]) * CELL_SIZE + 5,
            CELL_SIZE, CELL_SIZE), 0)
    pygame.display.flip()


app = QApplication(sys.argv)
ex = Application()
ex.show()

with open(ex.get_name(), 'r', encoding='utf-8') as file:
    data = file.readlines()[1:]
pygame.init()
size = width, height = X_SIZE * CELL_SIZE + 5, Y_SIZE * CELL_SIZE + 50
screen = pygame.display.set_mode(size)
pygame.mixer.music.load('Spore soundtrack.mp3')
pygame.mixer.music.play()
pause = False
clock = pygame.time.Clock()
age = 0
while age < len(data):
    if not pause:
        clock.tick(FPS)
        next(data[age])
        age += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                pause = not pause
            elif event.button == 1:
                mode += 1
                if mode == 3:
                    mode = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                age = age - 10 if age > 10 else age
            elif event.key == pygame.K_RIGHT:
                age += 10
print('END')
pygame.quit()
