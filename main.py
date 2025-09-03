import pygame
from pygame import sprite, transform, image, time, key, event, QUIT, K_UP, K_DOWN, K_LEFT, K_RIGHT
import random

pygame.init()

# Константы
WIDTH, HEIGHT = 750, 500
SQUARE_SIZE = 50
FPS = 2 # Уменьшена скорость змейки

# Окно игры
w = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Змейка")

# Загрузка изображений
bg = transform.scale(image.load("background.jpg"), (WIDTH, HEIGHT))
apple_img = transform.scale(image.load("apple.png"), (SQUARE_SIZE, SQUARE_SIZE))

class GameSprite(sprite.Sprite):
    def __init__(self, pl_image, pl_x, pl_y, w, h):
        super().__init__()
        self.image = transform.scale(image.load(pl_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y

    def draw_sprite(self):
        w.blit(self.image, (self.rect.x, self.rect.y))

class SnakeHead(GameSprite):
    def __init__(self, pl_x, pl_y):
        super().__init__("head.png", pl_x, pl_y, SQUARE_SIZE=50, SQUARE_SIZE=50)
        self.dx, self.dy = SQUARE_SIZE, 0

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def change_direction(self, key):
        if key == K_UP and self.dy == 0:
            self.dx, self.dy = 0, -SQUARE_SIZE
        elif key == K_DOWN and self.dy == 0:
            self.dx, self.dy = 0, SQUARE_SIZE
        elif key == K_LEFT and self.dx == 0:
            self.dx, self.dy = -SQUARE_SIZE, 0
        elif key == K_RIGHT and self.dx == 0:
            self.dx, self.dy = SQUARE_SIZE, 0

class SnakeBody(GameSprite):
    def __init__(self, pl_x, pl_y):
        super().__init__("square.png", pl_x, pl_y, SQUARE_SIZE, SQUARE_SIZE)

class Apple(GameSprite):
    def __init__(self):
        self.respawn()

    def respawn(self):
        self.rect = pygame.Rect(random.randint(0, (WIDTH // SQUARE_SIZE) - 1) * SQUARE_SIZE,
                                random.randint(0, (HEIGHT // SQUARE_SIZE) - 1) * SQUARE_SIZE,
                                SQUARE_SIZE, SQUARE_SIZE)
    
    def draw_sprite(self):
        w.blit(apple_img, (self.rect.x, self.rect.y))

# Основной игровой цикл
snake = [SnakeHead(250, 100)]
apple = Apple()
clock = pygame.time.Clock()
running = True

while running:
    w.blit(bg, (0, 0))
    for e in event.get():
        if e.type == QUIT:
            running = False
        elif e.type == pygame.KEYDOWN:
            snake[0].change_direction(e.key)
    
    # Движение змейки
    for i in range(len(snake) - 1, 0, -1):
        snake[i].rect.x = snake[i - 1].rect.x
        snake[i].rect.y = snake[i - 1].rect.y
    
    snake[0].update()
    
    # Проверка столкновения с яблоком
    if snake[0].rect.colliderect(apple.rect):
        apple.respawn()
        last_part = snake[-1]
        snake.append(SnakeBody(last_part.rect.x, last_part.rect.y))
    
    # Отрисовка яблока
    apple.draw_sprite()
    
    # Отрисовка змейки
    for part in snake:
        part.draw_sprite()
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()