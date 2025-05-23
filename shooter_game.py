from pygame import *
from random import randint,random
import os

os.environ['SDL_VIDEO_CENTERED'] = "True"

mixer.init()
font.init()

font1 = font.SysFont('sans-serif',40)
font2 = font.SysFont('sans-serif',80)

mixer.music.load('2 - Into the Unknown.mp3')
mixer.music.play(-1)
fire = mixer.Sound('fire.ogg')



class GameSprite(sprite.Sprite):
    def __init__(self,filename,w,h,speed,x,y):
        super().__init__()
        self.image = transform.scale(
            image.load(filename),
            (w,h)
        )
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))



class Player(GameSprite):
    def __init__(self,filename,w,h,speed,x,y):
        super().__init__(filename,w,h,speed,x,y)
        self.buff_count = 0
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 925:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png',75,100,60,self.rect.centerx,self.rect.top)
        bullets.add(bullet)
    def apply_buff(self):
        if self.buff_count == 0:
            self.buff_count += 1
            self.speed += 5
            print(self.speed)
    def remove_buff(self):
        self.buff_count -= 1
        self.speed -= 5
        




class Enemy(GameSprite):
    def update(self):
        if self.rect.y < 810:
            self.rect.y += self.speed
        global lost
        if self.rect.y >= 810:
            self.rect.y = 0
            self.rect.x = randint(0,900)
            lost += 1


        
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()



class AnimatedSprite:
    def __init__(self, images, frame_rate):
        self.images = images  # Список изображений для анимации
        self.frame_rate = frame_rate  # Количество кадров в секунду
        self.current_frame = 0  # Текущий кадр
        self.last_update = time.get_ticks()  # Время последнего обновления

    def update(self):
        now = time.get_ticks()
        if now - self.last_update > 1000 / self.frame_rate:
            self.current_frame = (self.current_frame + 1) % len(self.images)
            self.last_update = now

    def draw(self, surface, x, y):
        surface.blit(self.images[self.current_frame], (x, y))

# Загрузка изображений для анимации
def load_images():
    images = []
    for i in range(1, 5):  # Предполагается, что у вас есть изображения sprite_1.png, sprite_2.png и т.д.
        image_ = transform.scale(image.load(f'sprite_{i}.png').convert_alpha(), (120, 120))
        images.append(image_)
    return images

def load_images_background():
    images = []
    for i in range(1, 2):  # Предполагается, что у вас есть изображения sprite_1.png, sprite_2.png и т.д.
        image_ = transform.scale(image.load(f'space_{i}.png').convert_alpha(), (120, 120))
        images.append(image_)
    return images



# Класс для баффов
class Buff(GameSprite):
    def __init__(self, x, y, duration, filename, w, h, speed):
        super().__init__(filename,w,h,speed,x,y)
        self.duration = duration
        self.start_time = time.get_ticks()
        self.active = True

    def update(self):
        if self.rect.y < 810:
            self.rect.y += self.speed
        if time.get_ticks() - self.start_time > self.duration:
            self.active = False
            self.kill()
            player.remove_buff()




bullets = sprite.Group()
buffs = sprite.Group()

monsters = sprite.Group()
monsters.add(Enemy('vrag.png',100,60,1.5,randint(0,900),0))
monsters.add(Enemy('vrag.png',100,60,1.5,randint(0,900),0))
monsters.add(Enemy('vrag.png',100,60,1.5,randint(0,900),0))
monsters.add(Enemy('vrag.png',100,60,1.5,randint(0,900),0))
monsters.add(Enemy('vrag.png',100,60,1.5,randint(0,900),0))

window = display.set_mode((1200,800))

display.set_caption('Шутер')

background = transform.scale(
    image.load("space.png"),
    (1200,800)
)

menu_btn = GameSprite('start_button.png',200,200,0,350,400)

player = Player('sprite_1.png',120,120,5,100,650)

monster1 = Enemy('vrag.png',100,60,1.5,randint(0,900),0)
monster2 = Enemy('vrag.png',100,60,1.5,randint(0,900),0)
monster3 = Enemy('vrag.png',100,60,1.5,randint(0,900),0)
monster4 = Enemy('vrag.png',100,60,1.5,randint(0,900),0)
monster5 = Enemy('vrag.png',100,60,1.5,randint(0,900),0)

clock = time.Clock()
FPS = 60

game = True
finish = True
menu = True
images = load_images()  # Загрузка изображений
animated_sprite = AnimatedSprite(images, frame_rate=10)
background_images = load_images_background()  # Загрузка изображений
animated_background = AnimatedSprite(background_images, frame_rate=10)

lost = 0
score = 0

text_finish_lose = font2.render('ВЫ ПРОИГРАЛИ!',1,(214, 23, 14))
text_finish_win = font2.render('ВЫ ВЫИГРАЛИ!',1,(8, 222, 13))

while game:
    clock.tick(FPS)
    if finish == False:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    player.fire()

        # window.blit(background,(0,0))
        animated_background.update()
        animated_background.draw(window,0,0)
        player.update()
        player.reset()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        text_lose = font1.render('Пропущено: ' + str(lost),1,(255, 255, 255))
        window.blit(text_lose,(10,10))
        score_text = font1.render('Счет: ' + str(score),1,(255,255,255))
        window.blit(score_text,(10,60))
        animated_sprite.update()
        animated_sprite.draw(window, player.rect.x, player.rect.y)
        buffs.update()
        buffs.draw(window)


        monsters_list = sprite.groupcollide(monsters, bullets, False, True)
        sprites_list = sprite.spritecollide(player,monsters,True)
        buffs_list = sprite.spritecollide(player,buffs,True)
        for monster in monsters_list:
            score += 1
            monsters.add(Enemy('vrag.png',100,60,1,randint(0,900),0))
            if random() < 0.2:  # Случайное условие для создания баффа
                buffs.add(Buff(monster.rect.x, monster.rect.y, 7000, "buff.png",50,60,4))
            monster.kill()
        for buff in buffs_list:
            player.apply_buff()



        if score >= 45:
            finish = True
            window.blit(text_finish_win,(285,350))

        if lost >= 1 or sprites_list == True:
            finish = True
            window.blit(text_finish_lose,(285,350))



    if menu:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == MOUSEBUTTONDOWN:
                x,y = e.pos
                if menu_btn.rect.collidepoint(x,y):
                    menu = False
                    finish = False
        window.blit(background,(0,0))
        menu_btn.reset()

    if finish == True and menu == False:
        for e in event.get():
            if e.type == QUIT:
                game = False

    display.update()