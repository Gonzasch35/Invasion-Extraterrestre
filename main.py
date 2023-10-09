import pygame
import random
import math
from pygame import mixer

# Inicializar pygame
pygame.init()

#crear pantalla
pantalla = pygame.display.set_mode((800, 600))

# Titulo y fondo
pygame.display.set_caption('Invacion Espacial')
fondo = pygame.image.load('fondo.png')

# Musica
mixer.music.load('MusicaFondo.mp3')
mixer.music.set_volume(0.2)
mixer.music.play(-1)

# Jugador
img_jugador = pygame.image.load("avion.png")
# Bala
img_bala = pygame.image.load("bala.png")


# Variables jugador
jugador_x = 368
jugador_y = 500
jugador_x_cambio = 0
jugador_y_cambio = 0

# Variables enemigo
img_enemigo = []
enemigo_x = []
enemigo_y = []
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 5

for enemigo in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load("alien.png"))
    enemigo_x.append(random.randint(0, 736))
    enemigo_y.append(random.randint(50, 200))
    enemigo_x_cambio.append(3.5)
    enemigo_y_cambio.append(50)

# Variables de la bala
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 8
bala_visible = False
balas= []

# Puntaje
puntaje = 0
fuente = pygame.font.Font('alba.ttf', 32)
texto_x = 10
texto_y = 550

# Texto final del juego
fuente_final = pygame.font.Font('alba.ttf', 80)

def texto_final():
    mi_texto_final = fuente_final.render('Game Over', True, (200, 200, 200))
    pantalla.blit(mi_texto_final, (200, 220))

def mostrar_puntaje(x, y):
    texto = fuente.render(f'Puntaje: {puntaje}', True, (255, 255, 255))
    pantalla.blit(texto, (x, y))

# Funcion jugador
def jugador(x, y):
    pantalla.blit(img_jugador, (x, y))

# Funcion Enemigo
def enemigo(x, y, enemigo):
    pantalla.blit(img_enemigo[enemigo], (x, y))

# Funcion de la Bala
def disparar(x, y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala, (x + 16, y + 10))

# Funcion detectar colision
def colision(x1, y1, x2, y2):
    distancia = math.sqrt(math.pow(x1 - x2, 2) + math.pow(y1 - y2, 2))
    if distancia < 27:
        return True
    else:
        return False


# Loop del juego
se_ejecuta = True

while se_ejecuta:

    # Fondo
    pantalla.blit(fondo, (0 , 0))
    
    for evento in pygame.event.get():

        #Evento para cerrar el programa
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        
        #Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -5
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 5

            if evento.key == pygame.K_SPACE:
                if not bala_visible:
                    sonido_bala = mixer.Sound('disparo.mp3')
                    sonido_bala.play()
                    bala_x = jugador_x
                    disparar(bala_x, bala_y)

        #Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    # Modificar ubicacion0 al jugador
    jugador_x += jugador_x_cambio
    
    # Mantener dentro de bordes al jugador
    # Eje x
    if jugador_x <= 0:
        jugador_x = 0
    if jugador_x >= 736:
        jugador_x = 736

    # Modificar ubicacion al enemigo
    for e in range(cantidad_enemigos):

        # Fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break

        enemigo_x[e] += enemigo_x_cambio[e]

    
    # Mantener dentro de bordes al enemigo
    # Eje x
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 3.5
            enemigo_y[e] += enemigo_y_cambio[e]
        if enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -3.5
            enemigo_y[e] += enemigo_y_cambio[e]

        # Colision
        hay_colision = colision(enemigo_x[e], enemigo_y[e], bala_x, bala_y)
        if hay_colision:
            sonido_colision = mixer.Sound('Golpe.mp3')
            sonido_colision.play()
            bala_y = 520
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0, 736)
            enemigo_y[e] = random.randint(50, 200)

        enemigo(enemigo_x[e], enemigo_y[e], e)

    # Movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar(bala_x, bala_y)
        bala_y -= bala_y_cambio



    jugador(jugador_x, jugador_y)

    mostrar_puntaje(texto_x, texto_y)


    pygame.display.update()