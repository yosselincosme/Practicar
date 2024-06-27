import pygame
import constantes
class Personaje:
    def __init__(self, x, y, animaciones, energia):
        self.energia = energia
        self.vivo = True
        self.flip = False #Atributo para que cuando cambie a True el personaje se voltee
        self.animaciones = animaciones
        #imagen de la animacion que se está mostrando actualmente
        self.frame_index = 0
        # Aquí se almacena la hora actual (en milisegundos desde que se inició 'pygame')
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.forma = self.image.get_rect()
        self.forma.center = (x,y) #centrar el personaje en la coordenada x,y


    def movimiento(self, delta_x, delta_y):
        if delta_x < 0:
            self.flip = True
        if delta_x > 0:
            self.flip = False

        self.forma.x = self.forma.x + delta_x
        self.forma.y = self.forma.y + delta_y

    #método para actualizar las animaciones
    def update(self):
        if self.energia <= 0:
            self.energia = 0
            self.vivo = False

        cooldown_animacion = 100 # Tiempo que dura una imagen antes de actualizarse
        self.image = self.animaciones[self.frame_index]
        if pygame.time.get_ticks() - self.update_time >= cooldown_animacion:
            self.frame_index = self.frame_index + 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animaciones):
            self.frame_index = 0
    def draw(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False) #Guarda la transformación de la imagen
        interfaz.blit(imagen_flip, self.forma)
        #pygame.draw.rect(interfaz, (255,255,0), self.forma, 1)
