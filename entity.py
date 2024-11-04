"""
Aqui estan todas las clases de las entidades que aparecen en main2
"""

import pygame,random,os
pygame.mixer.init()
pygame.init()

# Clase del jugador
class Player:
    speed = 8
    def __init__(self, screen_width, screen_height, sprite_path="sprites/player.png"):
        # Cargar la imagen del jugador
        self.image = pygame.image.load(sprite_path)
        self.rect = self.image.get_rect()
        
        # Obtener dimensiones
        self.width = self.rect.width
        self.height = self.rect.height
        
        # Centrar el jugador en la mitad inferior de la pantalla
        self.x = (screen_width - self.width) / 2
        self.y = (screen_height * 3 / 3.5) - (self.height / 2)
        
        # Movimiento inicial
        self.x_movement = 0

        # Velocidad de movimiento
        #self.speed = 8

        # Sonido chocar pared
        self.wall_hit = pygame.mixer.Sound("sound/wallhit.wav")
        self.touch = False


    def update_position(self):
        # Actualizar posición en el eje x
        self.x += self.x_movement
        self.rect.topleft = (self.x, self.y)

        #Limites
        if self.x < 0:
            # Limite izquierdo
            self.x = 0
            # Sonido de tocar pared
            if self.touch == False:
                self.wall_hit.play()
                self.touch = True
                print (self.touch)
            
        if self.x > 800-(self.width):
            # Limite derecho
            self.x = 800-(self.width)
            # Sonido de tocar pared
            if self.touch == False:
                self.wall_hit.play()
                self.touch = True
        
        # Si no toca la pared Touch es Falso
        if self.x > 5 and self.x< 795-(self.width):
            self.touch = False
        

    def draw(self, screen):
        # Dibujar en pantalla el jugador en su posición actual
        screen.blit(self.image, (self.x, self.y))

# Clase del enemigo
class Enemy(pygame.sprite.Sprite):
    speed = 20
    def __init__(self):
        super().__init__()
        self.image_normal = pygame.image.load("sprites/enemie.png")
        self.image_angry = pygame.image.load("sprites/angry_enemie.png")
        self.image = self.image_normal  # Inicia con la imagen normal
        self.rect = self.image.get_rect()
        self.death_sound = pygame.mixer.Sound("sound/invaderkilled.wav")
        self.wall_hit = pygame.mixer.Sound("sound/wallhit2.wav")
        self.rect.x = 1
        self.rect.y = 1
        # Velocidad de movimiento
        #self.speed = 20
        self.touch = True
        self.state = True

    def update(self):
        #Movimiento
        if self.touch == False: 
            self.rect.x += self.speed
        elif self.touch == True:
            self.rect.x -= self.speed
    
        #Rebote
        if self.rect.x >= 800 - (self.rect.width):
            self.rect.y += 35
            self.wall_hit.play()
            self.speed += 0.7
            self.touch = True
        elif self.rect.x <= 0:
            self.rect.y += 35
            self.wall_hit.play()
            self.speed += 0.7
            self.touch = False
            

        #Fase 2
        if self.rect.y > 210:
            self.image = self.image_angry
        else:
            self.image = self.image_normal


        #Respawn
        if self.rect.y > 620:  
            self.speed = 8
            self.rect.x = random.randint(0, 789)
            self.rect.y = random.randint(50, 200)

    def draw(self, screen):

        if self.state:  
            screen.blit(self.image, self.rect.topleft)
        #Respawn si se va del limite
        if self.rect.y > 610:  
            self.rect.x = random.randint(0, 789)
            self.rect.y = random.randint(50, 200)
    
    def respawn(self): 
        self.speed = 8
        self.rect.x = random.randint(0, 789)
        self.rect.y = 1

    def play_death_sound(self):
        self.death_sound.play()

# Clase del disparo
class Shoot(pygame.sprite.Sprite):
    shoot_carpeta = "sprites/shoots"
    shoot_sound = pygame.mixer.Sound("sound/shoot.wav")
    shoot_imagenes = os.listdir(shoot_carpeta)
    
    def __init__(self, x, y):
        super().__init__()
        self.image = self.load_random_shoot(self.shoot_imagenes)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        # Velocidad de movimiento
        self.speed = 10

    @classmethod
    def load_random_shoot(cls, shoot_images):
        imagen_aleatoria = random.choice(shoot_images)
        return pygame.image.load(os.path.join(cls.shoot_carpeta, imagen_aleatoria))

    def update(self):
        if self.rect.y > 450:
            self.speed = 3
            self.rect.y -= self.speed
            if self.rect.y < -32:
                self.kill()
        else:
            self.speed = 10
            self.rect.y -= self.speed
            if self.rect.y < -32:
                self.kill()

    def play_shoot_sound(self):
        self.shoot_sound.play()

print ("Entity: Ready")
    