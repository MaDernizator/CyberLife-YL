from frame import Universe, X_SIZE, Y_SIZE, CELL_SIZE
import pygame

mode = 0
size = width, height = X_SIZE * CELL_SIZE + 10, Y_SIZE * CELL_SIZE + 50


def next():
    if world.get_count_of_organisms() <= 0:
        exit()
    screen.fill((0, 0, 0) if not mode or mode == 2 else (255, 255, 255))
    pygame.draw.rect(screen, pygame.Color(255, 0, 0), (0, 0, X_SIZE * CELL_SIZE + 10, Y_SIZE * CELL_SIZE + 10), 5)
    font = pygame.font.Font(None, 40)
    text_age = font.render(f"{world.get_age()}", True, (255, 0, 0))
    text_count = font.render(f"{world.get_count_of_organisms()}", True, (255, 0, 0))
    text_time = font.render(f"{world.get_time()}", True, (255, 0, 0))
    screen.blit(text_age, (width // 3, height - 40))
    screen.blit(text_count, (width // 2, height - 40))
    screen.blit(text_time, (width // 3 * 2, height - 40))
    for i in world.organisms:
        x, y, = i[1][0], i[1][1]
        try:
            pygame.draw.rect(screen, pygame.Color(*i[0].get_color(mode=mode)),
                             (x * CELL_SIZE + 5, y * CELL_SIZE + 5, CELL_SIZE, CELL_SIZE),
                             0)
        except:
            print(i[0].get_color(mode))
            print(i[0].get_hp())
    for i in world.cells:
        x, y, = i[1][0], i[1][1]
        pygame.draw.rect(screen, pygame.Color(*i[0].get_color(mode)),
                         (x * CELL_SIZE + 5, y * CELL_SIZE + 5, CELL_SIZE, CELL_SIZE), 0)
    pygame.display.flip()
    world.step()


pygame.init()
screen = pygame.display.set_mode(size)
pygame.mixer.music.load('Spore (2008) - Original soundtrack.mp3')
pygame.mixer.music.play()
world = Universe()
running, pause = True, False
clock = pygame.time.Clock()
while running:
    if not pause:
        next()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                pause = not pause
            elif event.button == 1:
                mode += 1
                if mode == 3:
                    mode = 0

pygame.quit()
