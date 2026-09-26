import pygame
from random import randint

pygame.init()
pygame.mixer.init()


# ---------------------------------
# VENTANA
# ---------------------------------
ANCHO = 700
ALTO = 500

window = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Tirador Espacial")

clock = pygame.time.Clock()
FPS = 60


# ---------------------------------
# FONDO
# ---------------------------------
background = pygame.image.load("galaxy.jpg")
background = pygame.transform.scale(background, (ANCHO, ALTO))


# ---------------------------------
# SONIDO DE DISPARO
# ---------------------------------
fire_sound = pygame.mixer.Sound("fire.ogg")


# ---------------------------------
# FUENTES
# ---------------------------------
font = pygame.font.Font(None, 36)
font_grande = pygame.font.Font(None, 80)


# ---------------------------------
# PANTALLA DE BIENVENIDA
# ---------------------------------
window.blit(background, (0, 0))

texto_bienvenida = font_grande.render(
    "¡BIENVENIDO!",
    True,
    (255, 255, 255)
)

texto_juego = font.render(
    "Tirador Espacial",
    True,
    (255, 255, 255)
)

rect_bienvenida = texto_bienvenida.get_rect(
    center=(ANCHO // 2, ALTO // 2 - 30)
)

rect_juego = texto_juego.get_rect(
    center=(ANCHO // 2, ALTO // 2 + 35)
)

window.blit(texto_bienvenida, rect_bienvenida)
window.blit(texto_juego, rect_juego)

pygame.display.update()

# Esperar 1 segundo
pygame.time.delay(1000)


# ---------------------------------
# CRONÓMETRO
# ---------------------------------
tiempo_inicio = pygame.time.get_ticks()
tiempo_limite = 60


# ---------------------------------
# CONTADORES
# ---------------------------------
score = 0
missed = 0

# Si se escapan 5, pierdes
max_missed = 5

# Si destruyes 10, ganas
goal = 10


# ---------------------------------
# CLASE BASE
# ---------------------------------
class GameSprite(pygame.sprite.Sprite):

    def __init__(
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_speed
    ):

        super().__init__()

        self.image = pygame.image.load(player_image)

        self.image = pygame.transform.scale(
            self.image,
            (size_x, size_y)
        )

        self.speed = player_speed

        self.rect = self.image.get_rect()

        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):

        window.blit(
            self.image,
            (self.rect.x, self.rect.y)
        )


# ---------------------------------
# JUGADOR
# ---------------------------------
class Player(GameSprite):

    def update(self):

        keys = pygame.key.get_pressed()

        # Mover a la izquierda
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed

        # Mover a la derecha
        if keys[pygame.K_RIGHT] and self.rect.x < ANCHO - self.rect.width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.y < ALTO - self.rect.height:
            self.rect.y += self.speed


    # ---------------------------------
    # DISPARAR
    # ---------------------------------
    def fire(self):

        bullet = Bullet(
            "bullet.png",

            # Centro de la nave
            self.rect.centerx - 8,

            # Arriba de la nave
            self.rect.top,

            15,
            30,
            10
        )

        bullets.add(bullet)

        fire_sound.play()


# ---------------------------------
# BALA
# ---------------------------------
class Bullet(GameSprite):

    def update(self):

        # La bala sube
        self.rect.y -= self.speed

        # Si sale de la pantalla
        if self.rect.bottom < 0:
            self.kill()
        def delay(self, milliseconds):
            pygame.time.delay(milliseconds)


# ---------------------------------
# ENEMIGO
# ---------------------------------
class Enemy(GameSprite):

    def __init__(
        self,
        player_image,
        player_x,
        player_y,
        size_x,
        size_y,
        player_speed
    ):

        super().__init__(
            player_image,
            player_x,
            player_y,
            size_x,
            size_y,
            player_speed
        )

        # Dirección horizontal
        self.speed_x = randint(-3, 3)

        # Evitar que salga 0
        if self.speed_x == 0:
            self.speed_x = 2


    def update(self):

        global missed

        # Movimiento diagonal
        self.rect.x += self.speed_x
        self.rect.y += self.speed

        # Rebotar en borde izquierdo
        if self.rect.left <= 0:
            self.speed_x *= -1

        # Rebotar en borde derecho
        if self.rect.right >= ANCHO:
            self.speed_x *= -1


        # Si logra escapar por abajo
        if self.rect.top > ALTO:

            missed += 1

            # Volver a aparecer arriba
            self.rect.x = randint(
                0,
                ANCHO - self.rect.width
            )

            self.rect.y = randint(
                -300,
                -50
            )

            # Nueva velocidad hacia abajo
            self.speed = randint(2, 4)

            # Nueva dirección horizontal
            self.speed_x = randint(-3, 3)

            if self.speed_x == 0:
                self.speed_x = 2


# ---------------------------------
# CREAR ENEMIGO
# ---------------------------------
def crear_enemigo():

    enemy = Enemy(
        "ufo.png",
        randint(0, ANCHO - 80),
        randint(-400, -50),
        80,
        50,
        randint(2, 4)
        
    )

    enemies.add(enemy)


# ---------------------------------
# JUGADOR
# ---------------------------------
player = Player(
    "rocket.png",
    310,
    390,
    80,
    100,
    7
)


# ---------------------------------
# GRUPOS
# ---------------------------------
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()


# Crear 5 enemigos
for i in range(5):
    crear_enemigo()


# ---------------------------------
# VARIABLES DEL JUEGO
# ---------------------------------
game = True
finish = False
win = False


# ---------------------------------
# CICLO PRINCIPAL
# ---------------------------------
while game:

    # ---------------------------------
    # EVENTOS
    # ---------------------------------
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            game = False

        # Disparar con ESPACIO
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE and not finish:
                player.fire()


    # ---------------------------------
    # JUEGO ACTIVO
    # ---------------------------------
    if not finish:

        # ---------------------------------
        # CALCULAR TIEMPO
        # ---------------------------------
        tiempo_actual = pygame.time.get_ticks()

        segundos_pasados = (
            tiempo_actual - tiempo_inicio
        ) // 1000

        tiempo_restante = (
            tiempo_limite - segundos_pasados
        )

        # Evitar números negativos
        if tiempo_restante < 0:
            tiempo_restante = 0


        # ---------------------------------
        # FONDO
        # ---------------------------------
        window.blit(background, (0, 0))


        # ---------------------------------
        # JUGADOR
        # ---------------------------------
        player.update()
        player.reset()


        # ---------------------------------
        # ENEMIGOS
        # ---------------------------------
        enemies.update()
        enemies.draw(window)


        # ---------------------------------
        # BALAS
        # ---------------------------------
        bullets.update()
        bullets.draw(window)


        # ---------------------------------
        # COLISIÓN:
        # BALA CONTRA ENEMIGO
        # ---------------------------------
        collisions = pygame.sprite.groupcollide(
            enemies,
            bullets,
            True,
            True
        )


        # Si destruimos enemigos
        for enemy in collisions:

            score += 1

            # Crear nuevo enemigo
            crear_enemigo()


        # ---------------------------------
        # COLISIÓN:
        # ENEMIGO CONTRA JUGADOR
        # ---------------------------------
        if pygame.sprite.spritecollide(
            player,
            enemies,
            False
        ):

            finish = True
            win = False


        # ---------------------------------
        # PERDER POR ENEMIGOS ESCAPADOS
        # ---------------------------------
        if missed >= max_missed:

            finish = True
            win = False


        # ---------------------------------
        # GANAR
        # ---------------------------------
        if score >= goal:

            finish = True
            win = True


        # ---------------------------------
        # PERDER POR TIEMPO
        # ---------------------------------
        if tiempo_restante <= 0 and score < goal:

            finish = True
            win = False


        # ---------------------------------
        # TEXTOS
        # ---------------------------------
        texto_score = font.render(
            "Aciertos: " + str(score),
            True,
            (255, 255, 255)
        )

        texto_missed = font.render(
            "Fallados: " + str(missed),
            True,
            (255, 255, 255)
        )

        texto_tiempo = font.render(
            "Tiempo: " + str(tiempo_restante),
            True,
            (255, 255, 255)
        )


        window.blit(
            texto_score,
            (10, 10)
        )

        window.blit(
            texto_missed,
            (10, 45)
        )

        window.blit(
            texto_tiempo,
            (ANCHO - 160, 10)
        )


    # ---------------------------------
    # PANTALLA FINAL
    # ---------------------------------
    else:

        window.blit(
            background,
            (0, 0)
        )


        # ---------------------------------
        # GANASTE
        # ---------------------------------
        if win:

            texto_final = font_grande.render(
                "¡GANASTE!",
                True,
                (0, 255, 0)
            )


        # ---------------------------------
        # PERDISTE
        # ---------------------------------
        else:

            texto_final = font_grande.render(
                "PERDISTE",
                True,
                (255, 0, 0)
            )


        # Centrar texto
        rect_texto = texto_final.get_rect(
            center=(
                ANCHO // 2,
                ALTO // 2
            )
        )

        window.blit(
            texto_final,
            rect_texto
        )


    # ---------------------------------
    # ACTUALIZAR PANTALLA
    # ---------------------------------
    pygame.display.update()

    clock.tick(FPS)


pygame.quit()