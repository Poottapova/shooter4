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


class Snake(GameSprite):
    def __init__(self, pl_image, pl_x, pl_y):
        super().__init__(pl_image, pl_x, pl_y)
        self.dx = SQUARE_SIZE
        self.dy = 0

    def update(self):
        # Двигаем голову
        self.rect.x += self.dx
        self.rect.y += self.dy
    
    def get_direction(self):
        keys = key.get_pressed()
        if keys[K_UP] and self.dy == 0:
            self.dx = 0
            self.dy = -SQUARE_SIZE
        elif keys[K_DOWN] and self.dy == 0:
            self.dx = 0
            self.dy = SQUARE_SIZE
        elif keys[K_LEFT] and self.dx == 0:
            self.dx = -SQUARE_SIZE
            self.dy = 0
        elif keys[K_RIGHT] and self.dx == 0:
            self.dx = SQUARE_SIZE
            self.dy = 0


# Создание объектов
head = Snake('head.png', 200, 250)

clock = time.Clock()

step_time = timer()

running = True 

finish = False
while running:
    
    for e in event.get():
        if e.type == QUIT:
            running = False

    if not finish:
        cur_time = timer()
        w.blit(bg, (0, 0))
        head.get_direction()

        # Перемещение змейки раз в 0.5 секунды
        if cur_time - step_time >= 0.5:
            head.update()        
            step_time = timer()

        head.draw_sprite()
        

    display.update()
    clock.tick(FPS)