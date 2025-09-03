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

font.init()
game_font = font.Font(None, 50)  # Шрифт для надписи
text = game_font.render("You lose", True, (255, 0, 0))  # Красный текст

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
        
        # Двигаем хвост, начиная с конца
        for i in range(len(snake) - 1, 0, -1):
            snake[i].rect.x = snake[i - 1].rect.x
            snake[i].rect.y = snake[i - 1].rect.y

        # Двигаем голову
        self.rect.x += self.dx
        self.rect.y += self.dy

        if self.rect.x > 700:
            self.rect.x = 0

        if self.rect.x < 0:
            self.rect.x = 700

        if self.rect.y < 0:
            self.rect.y = 450

        if self.rect.y > 450:
            self.rect.y = 0

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

        
class Apple(GameSprite):
    def __init__(self, pl_image):
        super().__init__(pl_image, 0, 0)
        self.respawn()

    def respawn(self):
        self.rect.x = randrange(0, WIDTH - SQUARE_SIZE, SQUARE_SIZE)
        self.rect.y = randrange(0, HEIGHT - SQUARE_SIZE, SQUARE_SIZE)


# Создание объектов
head = Snake('head.png', 200, 250)
apple = Apple('apple.png')

snake = [head]

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

            # Проверка столкновения головы с яблоком
            if head.rect.colliderect(apple.rect):
                apple.respawn()
                # Добавляем новый сегмент в хвост
                last_part = snake[-1]  # Берём последний сегмент хвоста
                new_x, new_y = last_part.rect.x, last_part.rect.y  # Координаты нового сегмента

                # Определяем, куда разместить новый сегмент относительно последнего сегмента
                if head.dx > 0:  # Движение вправо
                    new_x -= 50
                elif head.dx < 0:  # Движение влево
                    new_x += 50
                elif head.dy > 0:  # Движение вниз
                    new_y -= 50
                elif head.dy < 0:  # Движение вверх
                    new_y += 50

                # Создаём новый сегмент с рассчитанными координатами
                new_part = Snake('square.png', new_x, new_y)
                snake.append(new_part)

            step_time = timer()

        for part in snake[1:]:  # Начинаем со второго элемента (индекс 1)
            if head.rect.colliderect(part.rect):
                finish = True
                w.blit(text, (250, 200))  # Игра завершается

        # Отрисовка объектов
        apple.draw_sprite()
        for part in snake:
            part.draw_sprite()

        

    display.update()
    clock.tick(FPS)
