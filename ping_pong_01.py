from pathlib import Path
from random import randint,choice
from pygame import *
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,width,height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def colliderect(self, rect):
        return self.rect.colliderect(rect)
class Paddle(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed,side):
        super().__init__(player_image, player_x, player_y, width, height, player_speed)
        self.side = side
    def movement(self):
        if self.side == 0:
            if key_pressed[K_KP_7] and self.rect.y >= 0:
                self.rect.y -= self.speed
            if key_pressed[K_KP_4] and self.rect.y <= 400:
                self.rect.y += self.speed
        if self.side == 1:
            if key_pressed[K_KP_9] and self.rect.y >= 0:
                self.rect.y -= self.speed
            if key_pressed[K_KP_6] and self.rect.y <= 400:
                self.rect.y += self.speed
class Ball(GameSprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed,vertical_speed,heading):
        super().__init__(player_image, player_x, player_y, width, height, player_speed)
        self.vert_speed = vertical_speed
        self.heading = heading
    def movement(self):
        global score_r,score_l
        if self.heading == 1:
            self.rect.x += self.speed
        if self.heading == 0:
            self.rect.x -= self.speed
        self.rect.y += self.vert_speed
        if self.colliderect(paddle_sprite1):
            self.heading = 1
            self.vert_speed += choice(vert)
            self.speed = choice(rand_collide)
        if self.colliderect(paddle_sprite2):
            self.heading = 0
            self.vert_speed += choice(vert)
            self.speed = choice(rand_collide)
        if self.rect.y <= 0 or self.rect.y >= 450:
            self.vert_speed = self.vert_speed* -1
        if self.rect.x > 700:
            self.rect.x = 325
            self.rect.y = 225
            self.speed = choice(default_speed)
            self.vert_speed = choice(vert)
            score_l += 1
        if self.rect.x < -50:
            self.rect.x = 325
            self.rect.y = 225
            self.speed = choice(default_speed)
            self.vert_speed = choice(vert)
            score_r += 1
        
fps = 60
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
background = ('white')
clock = time.Clock()
vert = [2,-2]
rand_collide = [1,2,3,4,5,6]
default_speed = [2,-2]
randspeed = [1,2,3,-1,-2,-3]
paddle_sprite1 = Paddle(Path(__file__).parent / 'Paddle.png',5,150,25,100,5,0)
paddle_sprite2 = Paddle(Path(__file__).parent / 'Paddle.png',670,150,25,100,5,1)
ball1 = Ball(Path(__file__).parent / 'Ball.png',325,225,50,50,2,choice(vert),randint(0,1))
lose_x = 300
lose_y = 240
win_x = 300
win_y = 240
finish = False
score_r = 0
score_l = 0
font.init()
game = False
font = font.SysFont('Arial',30)
win = font.render('YOU WIN!',True,(0,215,0))
lose = font.render('YOU LOSE!',True,(255,0,0))
while game == False:
    window.fill(background)
    score_r_font = font.render(str(score_r),True,(255,0,0))
    score_l_font = font.render(str(score_l),True,(255,0,0))
    ball1.reset()
    paddle_sprite1.reset()
    paddle_sprite2.reset()
    window.blit(score_r_font,(550,0))
    window.blit(score_l_font,(100,0))
    if score_l >= 3: 
        window.blit(win,(450,220))
        window.blit(lose,(130,220))
        finish = True
    if score_r >= 3:
        window.blit(win,(130,220))
        window.blit(lose,(450,220))
        finish = True
    if finish != True:
        key_pressed = key.get_pressed()
        paddle_sprite1.movement()
        paddle_sprite2.movement()
        ball1.movement()
        clock.tick(fps)
    for e in event.get():
        if e.type == QUIT:
            game = True
    display.update()