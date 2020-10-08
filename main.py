import pygame
import random
from os import path
# directory images are present
img_dir = path.join(path.dirname(__file__),'images')
# directory in which sound files are present
snd_dir = path.join(path.dirname(__file__),'music')

# default values used in code frequently
width = 480
height = 600
fps = 60
POWERUP_TIME = 5000

# define colours plxel values
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# , initialise pygame and create window
pygame.init()  # initialise the game
pygame.mixer.init()  # to enable or initialise sound
screen = pygame.display.set_mode((width, height))  # to display the window it doesnt draw
pygame.display.set_caption("shoot up")  # caption of the game
clock = pygame.time.Clock()            # clock
font_name = pygame.font.match_font('arial')  # type of font which u wanna use

def draw_text(surf,text,size,x,y):
    font=pygame.font.Font(font_name,size)         # details of font includes size
    text_surface = font.render(text,True,white)   # true means anti-alias type
    text_rect = text_surface.get_rect()           # imp command to get the rectangles where the text must ppear
    text_rect.midtop = (int(x),int(y))            # where the text must appear
    surf.blit(text_surface,text_rect)             # text or any image must be blitted on the screen

def newmob():
    # if u wanna add mobs wif any mobs are destroyed
    m = Mob()                   # m is a mob calls  mob class
    all_sprites.add(m)          # add t o sprites grp
    mobs.add(m)                 # add to mobs grp

def draw_shield_bar(surface,x,y,pct):
    if pct < 0:
        pct = 0
    bar_length = 100
    bar_height = 10
    fill = (pct/100) * bar_length
    outlne_rect = pygame.Rect(x,y,bar_length,bar_height)
    fill_rect = pygame.Rect(x,y,fill,bar_height)
    pygame.draw.rect(surface,green,fill_rect)
    pygame.draw.rect(surface,white,outlne_rect,2)

def draw_lives(surf,x,y,lives,img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30*i     # for representing lives x cor
        img_rect.y = y            # y vor
        surf.blit(img,img_rect)   # blitting on screen

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img,(50,38))  # making rectangle
        self.rect = self.image.get_rect()
        self.radius =20
       # pygame.draw.circle(self.image,red,self.rect.center,self.radius)   # to adjust the radius
        self.rect.centerx = int( width / 2)
        self.rect.bottom = height - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250 # in milli seconds
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # time out for powerups
        if self.power>= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.bottom = height - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5  # 5 is the speed
        if keystate[pygame.K_RIGHT]:
            self.speedx = 5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx  # to move the rect in the x speed
        if self.rect.right > width:
            self.rect.right = width
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power +=1
        self.power_time = pygame.time.get_ticks()


    def shoot(self):
        now = pygame.time.get_ticks()
        if ( now - self.last_shot) > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx,self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
                shoot_sound.play()
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left,self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
                shoot_sound.play()


    def hide(self):
        self.hidden =True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (width/2,height+200)

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image = self.image_orig.copy()
        self.image_orig.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.85/2)
      #  pygame.draw.circle(self.image,red,self.rect.center,self.radius)   # to adjust the radius
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(width - self.rect.width)   #self.rect.width is 30
        self.rect.y  = random.randrange(-50,0)
        self.speedy = random.randrange(1,8)
        self.speedx = random.randrange(-3,3)
        self.rot =0
        self.rot_speed = random.randrange(-8,8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > height + 10 or self.rect.left < -25  or self.rect.right > width + 20 :
            self.rect.x = random.randrange(width - self.rect.width)  # self.rect.width is 30
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

class Bullet(pygame.sprite.Sprite):
    def __init__(self , x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10


    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()   # delets it\\

class Pow(pygame.sprite.Sprite):
    def __init__(self ,center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield','gun'])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2


    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.top > height:
            self.kill()   # delets it\\

class Explosion(pygame.sprite.Sprite):
    def __init__(self,center,size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75


    def update(self):
        now = pygame.time.get_ticks()
        if now-self.last_update > self.frame_rate:
            self.last_upate = now
            self.frame +=1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen,"shoot em up " , 64,width/2,height/4)
    draw_text(screen,"arrow keys move,space to fire",22,width/2,height/2)
    draw_text(screen, "press a key to begin ", 18 , width / 2, height *3/4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

#load all images
background = pygame.image.load(path.join(img_dir,"image.jpg"))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir,"playerShip1_orange.png")).convert()
player_mini_ig = pygame.transform.scale(player_img, (25,19))
player_mini_ig.set_colorkey(black)
bullet_img = pygame.image.load(path.join(img_dir,"laserRed07.png")).convert()
meteor_images = []
meteor_list = ["meteorBrown_big1.png","meteorBrown_big2.png",
                "meteorBrown_tiny1.png","meteorBrown_tiny2.png",
               "meteorBrown_med1.png","meteorBrown_med3.png",
               "meteorBrown_small1.png","meteorBrown_small2.png"]
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

#images for all explosions
for i in range(9):
    filename = 'expl_01_000{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(black)
    img_lg = pygame.transform.scale(img, (75,75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32,32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir,filename)).convert()
    img.set_colorkey(black)
    explosion_anim['player'].append(img)

powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir,'shield_gold.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir,'bolt_gold.png')).convert()

for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir,img)).convert())

# to load all sounds

shoot_sound = pygame.mixer.Sound(path.join(snd_dir,'Randomize2.wav'))
shield_sound = pygame.mixer.Sound(path.join(snd_dir,'Randomize7.wav'))
power_sound = pygame.mixer.Sound(path.join(snd_dir,'Randomize7.wav'))
expl_sounds =[]

for snd in ['Explosion4.wav','Explosion9.wav']:   # wt musics u want
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir,snd)))

player_die_sound = pygame.mixer.Sound(path.join(snd_dir,'rumble1.ogg'))
pygame.mixer.music.load(path.join(snd_dir,'tgfcoder-FrozenJam-SeamlessLoop.ogg'))
pygame.mixer.music.set_volume(0.4)

pygame.mixer.music.play(loops = -1)  # loop it when ever it ends

# game loop
game_over = True
running = True

while running:
    if game_over:
        show_go_screen()
        game_over = False

       # when the game starts again every hing must reset
        all_sprites = pygame.sprite.Group()
        player = Player()
        mobs = pygame.sprite.Group()  # grp to check for collisions
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        all_sprites.add(player)
        for i in range(10):
            newmob()

        score = 0


    # keeploop running at the right speed

    clock.tick(fps)  # loop speed

    # process input
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # update
    all_sprites.update()
    hits= pygame.sprite.groupcollide(mobs,bullets,True,True)
    for hit in hits:
        score += 50-hit.radius  # rpoints are based on the size less size more points more size less points
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center,'lg')
        all_sprites.add(expl)
        newmob()
        if random.random()  > 0.9 :    # random.random() gives a number btw 0 - 1
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)

    hits = pygame.sprite.spritecollide(player , mobs , True, pygame.sprite.collide_circle)   # if mob is collided it will be deleted sprite and grp  last cmd  is for circle collision

    # it is list of mobs hit the player
    for hit in hits:
        player.shield -= hit.radius*2
        death_expl = Explosion(hit.rect.center,'sm')
        all_sprites.add(death_expl)
        newmob()
        if player.shield <= 0:
            player_die_sound.play()
            expl = Explosion(hit.rect.center, 'player')
            all_sprites.add(expl)
            player.hide()
            player.lives -=1
            player.shield = 100

    # check to see if player hits the powerup
    hits = pygame.sprite.spritecollide(player, powerups, True, pygame.sprite.collide_circle)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10,20)
            shield_sound.play()
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            power_sound.play()
            player.powerup()

    # if the player died and explosion is finished
    if  player.lives == 0 and not death_expl.alive():
        game_over = True
    # draw / render

 #   screen.fill(black)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen,str(score),18,width/2,10)
    draw_shield_bar(screen,5,5,player.shield)  #x,y,wt per to fill
    # after drawing everything flip the display or else it takes more time
    # we have to do it last
    draw_lives(screen, width-100, 5, player.lives,player_mini_ig)
    pygame.display.flip()


pygame.quit()
