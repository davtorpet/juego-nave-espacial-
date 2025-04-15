import pygame
import random
import math
from pygame import mixer # Para sonidos

#Inicializar a pygame
pygame.init()

#Crear la pantalla
pantalla = pygame.display.set_mode((800,600))

#Titulo e Icono
pygame.display.set_caption ("Invasion Espacial")
icono = pygame.image.load(r"C:\Users\David\Desktop\Python\fotos\astronave.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load(r"C:\Users\David\Desktop\Python\fotos\fondo_mejor.jpg")

#agregar musica
mixer.music.load(r"C:\Users\David\Desktop\Python\sonidos\MusicaFondo.mp3")
#mixer.music.set_volume(0.5) Para bajarle o subirle el sonido
mixer.music.play(-1)

#Variables Jugador
img_jugador = pygame.image.load(r"C:\Users\David\Desktop\Python\fotos\cohete.png")
jugador_x = 368  #800/2-32 32 es la mitad de 64 que son los pixeles
jugador_y = 500   #600-64
jugador_x_cambio = 0.3

#Variables Enemigo
img_enemigo = []
enemigo_x = []
enemigo_y =[]
enemigo_x_cambio = []
enemigo_y_cambio = []
cantidad_enemigos = 8

for e in range(cantidad_enemigos):
    img_enemigo.append(pygame.image.load(r"C:\Users\David\Desktop\Python\fotos\enemigo.png"))
    enemigo_x.append(random.randint(0,736))
    enemigo_y.append(random.randint(50,200))
    enemigo_x_cambio.append(0.5)
    enemigo_y_cambio.append(50)

#Variables de la bala
balas = []
img_bala = pygame.image.load(r"C:\Users\David\Desktop\Python\fotos\bala_bien.jpg")
bala_x = 0
bala_y = 500
bala_x_cambio = 0
bala_y_cambio = 3
bala_visible = False

#Variable para puntaje
puntaje = 0
fuente = pygame.font.Font("freesansbold.ttf",32)
texto_x = 10
texto_y = 10

#texto final de juego
fuente_final = pygame.font.Font("freesansbold.ttf",40)

def texto_final():
    mi_fuente_final =  fuente_final.render("JUEGO TERMINADO",True,(255,255,255))
    pantalla.blit(mi_fuente_final,(60,200))

#funcion mostrar puntaje
def mostrar_puntaje(x,y):
    texto = fuente.render(f"Puntaje: {puntaje}",True,(255,255,255))
    pantalla.blit(texto,(x,y))

#funcion jugador
def jugador(x,y):
    pantalla.blit(img_jugador,(x,y))

def enemigo(x,y,ene):
    pantalla.blit(img_enemigo[ene],(x,y))

#funcion disparar bala
def disparar_bala(x,y):
    global bala_visible
    bala_visible = True
    pantalla.blit(img_bala,(x + 16,y + 10))

#funcion detectar colisiones
def hay_colision(x_1,y_1,x_2,y_2):
    distancia = math.sqrt(math.pow(x_2-x_1,2) + math.pow(y_2-y_1,2))
    if distancia < 27:
        return True
    else:
        return False

#Loop del juego
se_ejecuta = True
while se_ejecuta:

    #Poniendo RGB de la pantalla
    #pantalla.fill((205,104,228))
    pantalla.blit(fondo,(0,0))

    #iterar eventos
    for evento in pygame.event.get():

        #evento cerrar
        if evento.type == pygame.QUIT:
            se_ejecuta = False

        #Evento presionar teclas
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 1
            if evento.key == pygame.K_SPACE:
                sonido_bala = mixer.Sound(r"C:\Users\David\Desktop\Python\sonidos\Disparo.mp3")
                sonido_bala.play()
                if not bala_visible:
                    bala_x = jugador_x
                    disparar_bala(bala_x,bala_y)
        #Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0

    #Modificar ubicacion del jugador
    jugador_x += jugador_x_cambio
    #mantener dentro de bordes al jugador
    if jugador_x <= 0:
        jugador_x = 0
    if jugador_x >= 736:
        jugador_x = 736

    
    #Modificar ubicacion del enemigo
    for e in range(cantidad_enemigos):

        #fin del juego
        if enemigo_y[e] > 500:
            for k in range(cantidad_enemigos):
                enemigo_y[k] = 1000
            texto_final()
            break
        enemigo_x[e] += enemigo_x_cambio[e]
        #mantener dentro de bordes al enemigo
        if enemigo_x[e] <= 0:
            enemigo_x_cambio[e] = 1
            enemigo_y[e] += enemigo_y_cambio[e]
        if enemigo_x[e] >= 736:
            enemigo_x_cambio[e] = -1
            enemigo_y[e] += enemigo_y_cambio[e]
        #Detectar colision
        colision = hay_colision(enemigo_x[e],enemigo_y[e],bala_x,bala_y)
        if colision:
            sonido_colision = mixer.Sound(r"C:\Users\David\Desktop\Python\sonidos\golpe.mp3")
            sonido_colision.play()
            bala_y = 500
            bala_visible = False
            puntaje += 1
            enemigo_x[e] = random.randint(0,736)
            enemigo_y[e] = random.randint(50,200)
        enemigo(enemigo_x[e],enemigo_y[e],e)


    #movimiento bala
    if bala_y <= -64:
        bala_y = 500
        bala_visible = False
    if bala_visible:
        disparar_bala(bala_x,bala_y)
        bala_y -= bala_y_cambio




    jugador(jugador_x,jugador_y)

    mostrar_puntaje(texto_x,texto_y)

    #actualizar 
    pygame.display.update()
