#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer
mixer.init()
font.init()

missed = 0
score = 0 
num_fire = 0
rel_time = False
font = font.SysFont("Arial", 40)

score_text = font.render('Счет: '+ str(score), True, (255, 255, 255))
missed_text = font.render('Пропущено: '+ str(missed), True, (255, 255, 255))
lose = font.render('You lose', True, (255, 0, 0))
win = font.render('You won', True, (255, 0, 0))
reload_time = font.render('Waid, reload...', True, (255, 255, 255))

fire = mixer.Sound("fire.ogg")
mixer.music.load("space.ogg")
mixer.music.play()
w, h = 700, 500
window = display.set_mode((w, h))
display.set_caption("pygame window")
background = transform.scale(image.load("galaxy.jpg"), (w,h))
clock = time.Clock()

finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, player_speed, player_x, player_y, player_image, w=65, h=65):
        super().__init__() 
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += 10
        elif key_pressed[K_LEFT] and self.rect.x > 10:
            self.rect.x -= 10
    def fire(self):
        bullet = Bullet(5, self.rect.centerx, self.rect.top,"bullet.png", 15,20)
        bullets.add(bullet)
        

class Enemy(GameSprite):
    def update(self):
        global missed
        self.rect.y += self.speed
        if self.rect.y >= 500:
            missed = missed + 1
            self.rect.y = 0
            self.rect.x = randint(0, 650)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(0, 650)
    
hero = Player(10, 350, 420, "rocket.png")
monsters = sprite.Group()
bullets = sprite.Group()

asteroids = sprite.Group()

for l in range(3):
    asteroid = Asteroid(randint(1,2), randint(10, 640), 0,"asteroid.png")
    asteroids.add(asteroid)
for s in range(5):
    enemy = Enemy(randint(1,2), randint(10, 640), 0, "ufo.png")
    monsters.add(enemy)


game = 1
while game:
    for e in event.get():
        if e.type == QUIT:
            game = 0
        elif e.type== KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                     hero.fire()
                     fire.play()
                     num_fire += 1
                else:
                    rel_time = True
                    last_time = timer()


    if finish != True:
        


        missed_text = font.render('Пропущено: '+ str(missed), True, (255, 255, 255))
        score_text = font.render('Счет: '+ str(score), True, (255, 255, 255))

        window.blit(background, (0,0))
        window.blit(score_text, (5, 25))
        
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        
        hero.reset()
        hero.update()

        bullets.update()
        monsters.update()
        asteroids.update()
        
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprite_list:
            score += 1
            enemy = Enemy(randint(1,2), randint(10, 640), 0, "ufo.png")
            monsters.add(enemy)

        if score == 10:
            finish = True
            window.blit(win, (325, 225))
        sprite_list_two = sprite.spritecollide(hero, monsters, True)
        sprite_list_three = sprite.spritecollide(hero, asteroids, True)
        if sprite_list_two or sprite_list_three or missed >= 13:
            finish = True
            window.blit(lose, (325, 225))
        if rel_time == True:
            new_time = timer()
            if new_time - last_time >= 3:
                num_fire = 0
                rel_time = False
            
            window.blit(reload_time, (300, 450))
    window.blit(missed_text, (5, 75))
    display.update()
    clock.tick(60)


"""#создай игру "Лабиринт"!
from pygame import *
font.init()
mixer.init()

mixer.music.load("jungles.ogg")
mixer.music.play()
kick = mixer.Sound("kick.ogg")
money = mixer.Sound("money.ogg")

font = font.Font(None, 70)
win = font.render('You WIN', True, (255, 215, 0))
lose = font.render('You lose', True, (255, 215, 0))

finish = False
w, h = 700, 500
windows = display.set_mode((w,h))
display.set_caption("Maze")
clock = time.Clock()

background = transform.scale(image.load("background.jpg"), (w, h))

sprite1 = transform.scale(image.load("hero.png"), (50,50))
sprite2 = transform.scale(image.load("cyborg.png"), (50, 50))

class GameSprite(sprite.Sprite):
    def __init__(self, player_speed, player_x, player_y, player_image):
        super().__init__() 
        self.speed = player_speed
        self.image = transform.scale(image.load(player_image), (65,65))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_UP] and self.rect.y > 5:
            self.rect.y -= 10
        elif key_pressed[K_DOWN] and self.rect.y < 430:
            self.rect.y += 10
        elif key_pressed[K_RIGHT] and self.rect.x < 630:
            self.rect.x += 10
        elif key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= 10

class Enemy(GameSprite):
    def update(self):
        #self.dir = ''
        if self.rect.x <= 450:
            self.dir = 'right'

        if self.rect.x >= 550:
            self.dir = 'left'

        if self.dir == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        windows.blit(self.image, (self.rect.x, self.rect.y))

hero = Player(1000, 20, 400, "hero.png")
enemy = Enemy(3, 450, 320, "cyborg.png")
treasure = GameSprite(10, 550, 400, "treasure.png")

wall1 = Wall(2, 227, 37, 100, 50, 535, 10)
wall2 = Wall(2, 227, 37, 100, 50, 10, 300)
wall3 = Wall(2, 227, 37, 625, 50, 10, 430)
wall4 = Wall(2, 227, 37, 100, 475, 535, 10)
wall5 = Wall(2, 227, 37, 445, 150, 10, 325)
wall6 = Wall(2, 227, 37, 300, 50, 10, 325)


game = 1
while game: 
    

    for e in event.get():
        if e.type == QUIT:
            game = 0
    if finish != True:
        

        windows.blit(background, (0, 0))
        treasure.reset()
        hero.reset()
        hero.update()

        
        enemy.reset()
        enemy.update()
        
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()
        if sprite.collide_rect(hero, treasure):
            finish = True
            money.play()
            windows.blit(win, (200, 200))
        
        if sprite.collide_rect(hero, enemy) or sprite.collide_rect(hero, wall1) or sprite.collide_rect(hero, wall2) or sprite.collide_rect(hero, wall3) or sprite.collide_rect(hero, wall4) or sprite.collide_rect(hero, wall5) or sprite.collide_rect(hero, wall6):
            finish = True
            kick.play()
            windows.blit(lose, (200, 200))



    display.update()
    clock.tick(60)"""