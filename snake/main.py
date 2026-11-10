"""Bucle principal del juego. Duenio: Persona 2.

Ejecutar con:  python -m snake.main
"""

import pygame

from snake import config, game
from snake.snake_logic import ABAJO, ARRIBA, DERECHA, IZQUIERDA

# Flechas para mover la serpiente (US04)
TECLAS = {
    pygame.K_UP: ARRIBA,
    pygame.K_DOWN: ABAJO,
    pygame.K_LEFT: IZQUIERDA,
    pygame.K_RIGHT: DERECHA,
}


def main():
    pygame.init()
    surface = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
    pygame.display.set_caption(config.TITULO)
    reloj = pygame.time.Clock()

    juego = game.Juego()

    corriendo = True

    while corriendo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

            elif evento.type == pygame.KEYDOWN:
                if juego.estado == game.MENU:
                    if evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        juego.iniciar()
                    elif evento.key == pygame.K_ESCAPE:
                        corriendo = False

                elif juego.estado == game.JUGANDO:
                    if evento.key in TECLAS:
                        juego.girar(TECLAS[evento.key])
                    elif evento.key == pygame.K_ESCAPE:
                        juego.estado = game.MENU

        juego.tick()

        surface.fill(config.FONDO_HUD)
        pygame.display.flip()
        reloj.tick(config.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()