import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

FPS=60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 6
SCORE = 0

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

font = pygame.font.Font("arcade.ttf", 40)
font_small = pygame.font.Font("arcade.ttf", 30)
menu_font = pygame.font.Font("arcade.ttf", 40)

background = pygame.image.load("background.jpg")
background_menu = pygame.image.load("background_menu.png")
gameover_background = pygame.image.load("gameover.png")
play_button = pygame.transform.scale(pygame.image.load("start.png"), (300,100))

play_button_rect = play_button.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

score_rect_img = pygame.transform.scale(pygame.image.load("scoreboard.png"), (200, 100))
score_rect_pos = (SCREEN_WIDTH // 2 - score_rect_img.get_width() // 2, 10)

pygame.mixer.Sound('backgroundmusic.mp3').play()

DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

def show_menu():
    while True:
        
        DISPLAYSURF.blit(background_menu, (0, 0))
        DISPLAYSURF.blit(play_button, play_button_rect)
        
        # Verifica eventos do menu
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    return  

        pygame.display.update()


show_menu()
 

class Rat(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


        self.images = [
            pygame.transform.scale(pygame.image.load('rat-1.png'), (100, 150)),
            pygame.transform.scale(pygame.image.load('rat-2.png'), (100, 150)),
            pygame.transform.scale(pygame.image.load('rat-3.png'), (100, 150))
        ]

        self.index = 0
        
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = (160,520)

        self.animation_speed = 0.05
        self.current_time = 0

    


    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.top > 600):
            #SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        self.current_time += self.animation_speed
        if self.current_time >= 1:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]




class Enemy(pygame.sprite.Sprite):
      def __init__(self):
        super().__init__() 

        self.images = [
            pygame.transform.scale(pygame.image.load('poison-1.png'), (60, 70)),
            pygame.transform.scale(pygame.image.load('poison-2.png'), (60, 70)),
            pygame.transform.scale(pygame.image.load('poison-3.png'), (60, 70))
        ]

        self.index = 0
        
        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        self.animation_speed = 0.05
        self.current_time = 0



 
      def move(self):

        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

 
        self.current_time += self.animation_speed
        if self.current_time >= 1:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 


        self.images = [
        pygame.image.load("catpop-1.png"),
        pygame.image.load("catpop-2.png")
        ]


        self.index = 0

        self.image = self.images[self.index]

        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

        self.animation_speed=0.1
        self.current_time=0
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
         
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(5, 0)
                   


        self.current_time += self.animation_speed
        if self.current_time >= 1:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]


#Setting up Sprites        
P1 = Player()
E1 = Enemy()
R1 = Rat()
 
#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
rat = pygame.sprite.Group()
rat.add(R1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(R1)
 
#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 5000)
 
#Game Loop
while True:
       
    #Cycles through all events occurring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 1    
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.blit(background, (0,0))


    DISPLAYSURF.blit(score_rect_img, score_rect_pos)
   
    scores = font_small.render(str(SCORE), True, BLACK)
  
    text_rect = scores.get_rect(center=(score_rect_pos[0] + score_rect_img.get_width() // 2, score_rect_pos[1] + score_rect_img.get_height() // 2))
    DISPLAYSURF.blit(scores, text_rect)

    
 
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
 


    #collision player and rat
    if pygame.sprite.spritecollideany(P1, rat):
        SCORE += 10
        eating_sound = pygame.mixer.Sound("eating.mp3")
        eating_sound.play(loops=0)
        
        for rats in rat:
            rats.rect.top = 0
            rats.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            

    #collision player and enemy
    if pygame.sprite.spritecollideany(P1, enemies):
          pygame.mixer.Sound('oof.mp3').play()
          time.sleep(0.5)
                    
          DISPLAYSURF.blit(gameover_background, (0,0))
           
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(2)
          pygame.quit()
          sys.exit()        
         
    pygame.display.update()
    FramePerSec.tick(FPS)