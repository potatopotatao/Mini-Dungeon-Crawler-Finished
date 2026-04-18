import pygame
import random
import math

# --------------------
# INIT
# --------------------
pygame.init()

WIDTH, HEIGHT = 1200, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Micro RPG Arena")

clock = pygame.time.Clock()
FPS = 60


menu_surface = pygame.Surface((200,1000))



# --------------------
# COLORS
# --------------------
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (20, 20, 20)



# --------------------
# PLAYER CLASS
# --------------------
class Player(pygame.sprite.Sprite):
    def __init__(self,xpos,ypos,size,speed,color):
        self.player_xpos = xpos
        self.player_ypos = ypos
        self.size = size
        self.speed = speed
        self.color = color
        self.hp = 100
        self.player_rect = pygame.Rect(self.player_xpos,self.player_ypos,self.size,self.size)
        self.player_attack_rect = pygame.Rect(0,0,self.size+50,self.size+50)
        self.player_hitbox_rect = pygame.Rect(self.player_rect.x,self.player_rect.y,self.size+6,self.size+6)
        self.cooldown_counter = 0
        self.attack_counter = 0
        self.damage = 10
        self.draw_hitbox = False
        self.immunity = 0

    def player_movement_handling(self,event,enemy):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_rect.y -= self.speed

        for e in enemy:
            if self.player_rect.colliderect(e.enemy_rect):
                self.player_rect.y += self.speed



            
        if keys[pygame.K_s]:
            self.player_rect.y += self.speed

        for e in enemy:
            if self.player_rect.colliderect(e.enemy_rect):
                self.player_rect.y -= self.speed

                

            
        if keys[pygame.K_a]:
            self.player_rect.x -= self.speed

        for e in enemy:
            if self.player_rect.colliderect(e.enemy_rect):
                self.player_rect.x += self.speed

            
        if keys[pygame.K_d]:
            self.player_rect.x += self.speed

        for e in enemy:
            if self.player_rect.colliderect(e.enemy_rect):
                self.player_rect.x -= self.speed

        if self.player_rect.x < 200:
            self.player_rect.x += self.speed
        if self.player_rect.x > 1200 - self.size:
            self.player_rect.x -= self.speed
        if self.player_rect.y < 0:
            self.player_rect.y += self.speed
        if self.player_rect.y > 1000 - self.size:
            self.player_rect.y -= self.speed



    def player_attack(self,event,enemy):
        if event.key == pygame.K_SPACE:
            if self.cooldown_counter <= 0:
                self.cooldown_counter = 300
                self.attack_counter = 60
                for e in enemy:
                    if self.player_attack_rect.colliderect(e.enemy_rect):
                        e.hp -= self.damage

    def attack_logistics(self,screen,collisions):
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1

        if self.attack_counter > 0:
            self.attack_counter -= 1
            self.draw_hitbox = True

        if self.immunity > 0:
            self.immunity -= max(1,collisions)

        
        if self.attack_counter <= 0:
            self.draw_hitbox = False


    def update_player(self,screen):
            self.player_hitbox_rect.topleft = (self.player_rect.x-3,self.player_rect.y-3)
            self.player_attack_rect.center = self.player_rect.center
            self.attack_logistics(screen,collisions)
            if self.draw_hitbox is True:
                pygame.draw.rect(screen,(0,0,255),self.player_attack_rect)
            pygame.draw.rect(screen,(0,255,0),self.player_hitbox_rect)
            pygame.draw.rect(screen,self.color,self.player_rect)



# --------------------
# ENEMY CLASS
# --------------------

class Enemy(pygame.sprite.Sprite):
    def __init__(self,size,speed,color,xpos,ypos):
        self.size = size
        self.speed = speed
        self.color = color
        self.enemy_xpos = xpos
        self.enemy_ypos = ypos
        self.enemy_rect = pygame.Rect(self.enemy_xpos,self.enemy_ypos,self.size,self.size)
        self.hp = 10

    def enemy_movement_handling(self,player):
        dx = self.enemy_rect.x - player.player_rect.x
        dy = self.enemy_rect.y - player.player_rect.y
        

        distance = ((dx**2)+(dy**2))**0.5

        if distance < self.speed:
            self.enemy_rect.x = player.player_rect.x
            self.enemy_rect.y = player.player_rect.y
        else:
            dx = dx/distance
            dy = dy/distance

            self.enemy_rect.topleft = (self.enemy_rect.x,self.enemy_rect.y)

            

            self.enemy_rect.x -= dx * self.speed
            if self.enemy_rect.colliderect(player.player_rect):
                self.enemy_rect.x += dx * self.speed

                
            self.enemy_rect.y -= dy * self.speed
            if self.enemy_rect.colliderect(player.player_rect):
                self.enemy_rect.y += dy * self.speed

            


    def update_enemy(self,screen):
        pygame.draw.rect(screen,self.color,self.enemy_rect)

player = Player(500,500,50,4,RED)
enemy = [Enemy(30,3,BLUE,200,200)]


frequency = 600
counter = 0

collisions = 0

# --------------------
# FUNCTIONS
# --------------------
def collision_check(player,enemy,collisions):
    collisions = 0
    for e in enemy:
        if player.player_hitbox_rect.colliderect(e.enemy_rect):
            collisions += 1
    return collisions
    

def damage_function_shit(player,enemy,collisions):
    if collisions > 0:
        if player.immunity <= 0:
            player.hp -= 1
            player.immunity = 30


def remove_dead_enemy(enemy):
    return[e for e in enemy if e.hp > 0]


def create_enemy(enemy):
    global frequency
    global counter
    global wave
    if frequency > 60:
        if counter == 600:
            frequency -= 60
            counter = 0
            wave += 1
    if random.randint(1,frequency) is 1:
        enemy.append(Enemy(30,3,BLUE,random.randint(200,1000),random.randint(1,1000)))
    if frequency <= 0:
        wave = 999
    counter += 1


def menu_update_shit():
    global font, text_rect, player_hp_title,player_hp,menu_rect, player, time, enemy, wave
    player_hp_title = font.render("Player",True,(200,255,255))
    player_hp = font.render(str(player.hp),True,(255,255,255))

    attack_cooldown_title = font.render("Cooldown",True,(200,255,255))
    attack_cooldown = font.render(str(round((player.cooldown_counter/60),1)),True,(255,255,255))
    
    enemy_count_title = font.render("Enemies",True,(255,200,255))
    enemy_count = font.render(str(len(enemy)),True,(255,255,255))

    wave_number_title = font.render("Wave",True,(255,200,255))
    if wave <= 8:
        wave_number = font.render(str(wave),True,(255,255,255))
    if wave >= 9:
        wave_number = font.render("MAX",True,(255,0,0))

    
    game_time_title = font.render("Time",True,(255,255,200))
    game_time = font.render(str(round((time/60),1)),True,(255,255,255))
    
    #basic menu shit underneath
    menu_surface.fill((100,100,100))
    pygame.draw.rect(menu_surface,(100,100,100),menu_rect)

    #ACC text and stuff and shit
    menu_surface.blit(player_hp_title,(5,32))
    menu_surface.blit(player_hp,(3,64))

    
    menu_surface.blit(attack_cooldown_title,(5,108))
    menu_surface.blit(attack_cooldown,(5,140))

    
    menu_surface.blit(enemy_count_title,(5,204))
    menu_surface.blit(enemy_count,(5,236))
    
    menu_surface.blit(wave_number_title,(5,280))
    menu_surface.blit(wave_number,(5,312))

    
    menu_surface.blit(game_time_title,(5,376))
    menu_surface.blit(game_time,(5,408))

    




font = pygame.font.SysFont("ocra",32)

menu_rect = pygame.Rect(0,0,200,1000)


wave = 0


time = 0

# --------------------
# GAME LOOP
# --------------------
running = True
while running is True:
    dt = clock.tick(FPS)

    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            player.player_attack(event,enemy)


    # UPDATE
    create_enemy(enemy)
    enemy = remove_dead_enemy(enemy)
    player.player_movement_handling(event,enemy)
    collisions = collision_check(player,enemy,collisions)
    damage_function_shit(player,enemy,collisions)
    for e in enemy:
        e.enemy_movement_handling(player)

    # DRAW
    screen.fill(BLACK)
    player.update_player(screen)
    for e in enemy:
        e.update_enemy(screen)

    if player.hp <= 0:
        running = False

    menu_update_shit()


    screen.blit(menu_surface,(0,0))

    time += 1

    pygame.display.flip()


print(time)
pygame.quit()
