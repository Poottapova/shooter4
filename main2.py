from pygame import *
from time import time as timer
from random import *


Main_Window = display.set_mode((750, 500))
display.set_caption("Змейка")
Background = transform.scale(image.load("background.jpg"), (750, 500))



gamecycle = True


FPS = 55
clock = time.Clock()


font.init()
game_font = font.Font(None, 50)
game_over = game_font.render("Игра окончена", 1, (0, 0, 0))


class GameSprite(sprite.Sprite):
    def __init__(self, image_pic, x, y):
        super().__init__()
        self.image_pic = transform.scale(image.load(image_pic), (50, 50))
        self.rect = self.image_pic.get_rect()
        self.rect.x = x
        self.rect.y = y
   
    def draw(self):
        Main_Window.blit(self.image_pic, (self.rect.x, self.rect.y))


class Snake(GameSprite):
    def __init__(self, snake_image, x, y):
        super().__init__(snake_image, x, y)
        self.velo_x = 50
        self.velo_y = 0


    def update(self):
        for i in range(len(body) - 1, 0, -1):
            body[i].rect.x = body[i - 1].rect.x
            body[i].rect.y = body[i - 1].rect.y




        self.rect.x += self.velo_x
        self.rect.y += self.velo_y


    def get_direction(self):
        keys = key.get_pressed()
        if keys[K_UP]:
            self.velo_x = 0
            self.velo_y = -50
        if keys[K_DOWN]:
            self.velo_x = 0
            self.velo_y = 50
        if keys[K_LEFT]:
            self.velo_x = -50
            self.velo_y = 0
        if keys[K_RIGHT]:
            self.velo_x = 50
            self.velo_y = 0


Zmeya = Snake("head.png", 200, 300)


class Apple(GameSprite):
    def __init__(self, image_pic):
        super().__init__(image_pic, 0, 0)
        self.respawn()
   
    def respawn(self):
        self.rect.x = randrange(50, 700, 50)
        self.rect.y = randrange(50, 450, 50)


Yabloko = Apple("apple.png")


snake_time = timer()


body = [Zmeya]


finish = False
while gamecycle:


    for e in event.get():
        if e.type == QUIT:
            gamecycle = False


    if finish == False:


        current_time = timer()




        if current_time - snake_time >= 0.3:
            Zmeya.update()
            snake_time = timer()


        if Zmeya.rect.colliderect(Yabloko.rect):
            Yabloko.respawn()


            last_body = body[-1]
            new_x = last_body.rect.x
            new_y = last_body.rect.y


            if Zmeya.velo_x > 0:
                new_x -= 50
            elif Zmeya.velo_x < 0:
                new_x += 50
            elif Zmeya.velo_y < 0:
                new_y += 50
            elif Zmeya.velo_y > 0:
                new_y -= 50


            new_body = Snake("head.png", new_x, new_y)
            body.append(new_body)

        Main_Window.blit(Background, (0, 0))
        for i in range(1, len(body)):
            if Zmeya.rect.colliderect(body[i].rect):
                finish = True
                Main_Window.blit(game_over, (350, 250))
        
               


        if Zmeya.rect.x > 700:
            Zmeya.rect.x = 0
        elif Zmeya.rect.x < 0:
            Zmeya.rect.x = 700
        elif Zmeya.rect.y < 0:
            Zmeya.rect.y = 450
        elif Zmeya.rect.y > 450:
            Zmeya.rect.y = 0






        
        Zmeya.draw()
        Yabloko.draw()


        for i in range(len(body)):
            body[i].draw()


        Zmeya.get_direction()


       
    display.update()
    clock.tick(FPS)
   
   
   

