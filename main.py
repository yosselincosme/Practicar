import pygame
import constantes
from personaje import Personaje
from weapon import Weapon
from textos import DamageText
from items import Item
pygame.init()

ventana = pygame.display.set_mode((constantes.ANCHO,
                                   constantes.ALTO))

pygame.display.set_caption("Proyecto de POO")

#fuentes
font = pygame.font.Font("assets/fonts/m6x11.ttf")


#escalar imagen
def escalar_img(image, scale): #escala de imagen
    w = image.get_width()
    h = image.get_height()
    nueva_imagen = pygame.transform.scale(image, (w*scale, h*scale))
    return nueva_imagen

# Importar imagenes
#energia
corazon_vacio = pygame.image.load("assets//images//items//cora_vacio.png").convert_alpha()
corazon_vacio = escalar_img(corazon_vacio, constantes.SCALA_CORAZON)
corazon_mitad = pygame.image.load("assets//images//items//cora_medio.png").convert_alpha()
corazon_mitad = escalar_img(corazon_mitad, constantes.SCALA_CORAZON)
corazon_lleno = pygame.image.load("assets//images//items//cora_lleno.png").convert_alpha()
corazon_lleno = escalar_img(corazon_lleno, constantes.SCALA_CORAZON)



#Personaje
animaciones = []
for i in range(7):
    img = pygame.image.load(f'assets//images//characters//Player//Player_{i}.png')
    img = escalar_img(img, constantes.SCALA_PERSONAJE)
    animaciones.append(img)

#enemigos

directorio_enemigos = "assets/images/characters/enemigos"
tipo_enemigos = ["Pajaro", "Vampiro"]  # Definir nombres de carpetas manualmente

animacion_enemigos = []

for eni in tipo_enemigos:
    lista_temp = []
    num_animaciones = 5  # Número fijo de imágenes por cada tipo de enemigo

    for i in range(num_animaciones):
        ruta_temp = f"{directorio_enemigos}/{eni}/{eni}_{i + 1}.png"
        img_enemigo = pygame.image.load(ruta_temp).convert_alpha()
        img_enemigo = escalar_img(img_enemigo, constantes.SCALA_ENEMIGO)  # Escalar la imagen
        lista_temp.append(img_enemigo)

    animacion_enemigos.append(lista_temp)

#Arma
imagen_pistola = pygame.image.load(f'assets//images//weapons//gun.png')
imagen_pistola = escalar_img(imagen_pistola, constantes.SCALA_ARMA)

#Balas
imagen_balas= pygame.image.load(f'assets//images//weapons//bala.png')
imagen_balas = escalar_img(imagen_balas, constantes.SCALA_ARMA)

#Imagenes Items
pocion_roja = pygame.image.load("assets//images//items//pocion.png")
pocion_roja = escalar_img(pocion_roja, 0.05)

coin_images = []
ruta_img = "assets/images/items/coin"
num_coin_images = 5  # Número fijo de imágenes para las monedas (asumido según la descripción)

for i in range(num_coin_images):
    ruta_temp = f"{ruta_img}/coin_{i+1}.png"
    img = pygame.image.load(ruta_temp)
    img = escalar_img(img, 0.1)  # Escalar la imagen (asumiendo que tienes una función escalar_img definida)
    coin_images.append(img)

def vida_jugador():
    c_mitad_dibujado = False
    for i in range(5):
        if jugador.energia >=((i+1)*20):
            ventana.blit(corazon_lleno,(5+i*50, 5))
        elif jugador.energia % 20 >0 and c_mitad_dibujado == False:
            ventana.blit(corazon_mitad,(5+i*50, 5))
            c_mitad_dibujado = True
        else:
            ventana.blit(corazon_vacio,(5+i*50, 5))



# Crear un jugador de la clase Personaje
jugador = Personaje(50, 50, animaciones, 100)

# crear un enemigo
pajaro = Personaje(500, 300, animacion_enemigos[0], 100)
vampiro = Personaje(400, 300, animacion_enemigos[1], 100)
pajaro_2 = Personaje(100, 200, animacion_enemigos[0], 100)

#crear lista de enemigos
lista_enemigos = []
lista_enemigos.append(pajaro)
lista_enemigos.append(vampiro)
lista_enemigos.append(pajaro_2)


#Crear un arma de la clase Weapor
pistola = Weapon(imagen_pistola, imagen_balas)


#crear un grupo de sprites
grupo_damage_text = pygame.sprite.Group()
grupo_balas = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()

coin = Item(350, 25, 0, coin_images)
pocion = Item(320, 60, 1, [pocion_roja])

grupo_items.add(coin)
grupo_items.add(pocion)

#definir variables de movimiento del jugador
mover_arriba = False
mover_abajo = False
mover_izquierda = False
mover_derecha = False

# Controlar el frame rate
reloj = pygame.time.Clock()

run = True
while run == True:

    #que vaya a 60 FPS
    reloj.tick(constantes.FPS)

    ventana.fill(constantes.COLOR_BG)

    #calcular movimiento del jugador
    delta_x = 0
    delta_y = 0

    if mover_derecha == True:
        delta_x = constantes.VELOCIDAD
    if mover_izquierda == True:
        delta_x = -constantes.VELOCIDAD
    if mover_arriba == True:
        delta_y = -constantes.VELOCIDAD
    if mover_abajo == True:
        delta_y = constantes.VELOCIDAD

    #mover al jugador
    jugador.movimiento(delta_x, delta_y)

    # Actualiza estado del jugador
    jugador.update()

    #Actualiza el estado del enemigo
    for ene in lista_enemigos:
        ene.update()
        print(ene.energia)

    # Actualiza el estado del arma
    bala = pistola.update(jugador)
    if bala:
        grupo_balas.add(bala)
    for bala in grupo_balas:
        damage, pos_damage = bala.update(lista_enemigos)
        if damage:
            damage_text = DamageText(pos_damage.centerx, pos_damage.centery, str(damage), font , constantes.ROJO)
            grupo_damage_text.add(damage_text)
    #Actualiza el daño
    grupo_damage_text.update()

    #actualiza los items
    grupo_items.update()

    # dibuja al jugador
    jugador.draw(ventana)

    #dibujar enemigo
    for ene in lista_enemigos:
        ene.draw(ventana)

    # Dibuja el arma
    pistola.draw(ventana)

    #dihujar balas
    for bala in grupo_balas:
        bala.dibujar(ventana)

    #dibujar los corazones
    vida_jugador()

    #dibujar textos
    grupo_damage_text.draw(ventana)

    #dibujar items
    grupo_items.draw(ventana)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                mover_izquierda = True
            if event.key == pygame.K_d:
                mover_derecha = True
            if event.key == pygame.K_w:
                mover_arriba = True
            if event.key == pygame.K_s:
                mover_abajo = True

        #para cuando se suelte la tecla
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                mover_izquierda = False
            if event.key == pygame.K_d:
                mover_derecha = False
            if event.key == pygame.K_w:
                mover_arriba = False
            if event.key == pygame.K_s:
                mover_abajo = False



    pygame.display.update()  # ACTUALIZAR LA VENTANA PARA HACER VISIBLELOS CAMBIOS

pygame.quit()
