from pygame import *
from time import time as timer
from random import *

# Константы
WIDTH, HEIGHT = 750, 500
SQUARE_SIZE = 50
FPS = 60 

# Окно игры
w = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Змейка")

# Загрузка изображений
bg = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (SQUARE_SIZE, SQUARE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def draw_sprite(self):
        w.blit(self.image, (self.rect.x, self.rect.y))



# Создание объектов
head = GameSprite('head.png', 200, 250)

clock = time.Clock()


running = True 

finish = False
while running:
    
    for e in event.get():
        if e.type == QUIT:
            running = False

    if not finish:

        w.blit(bg, (0, 0))
        

        head.draw_sprite()
        

    display.update()
    clock.tick(FPS)