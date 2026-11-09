"""Dibujo del tablero, la serpiente y el alimento.

Duenio: Persona 5
Historias: US02 (ver el tablero)
"""

import pygame

from snake import config


def _rect(celda, margen=1):
    x, y = celda
    return pygame.Rect(
        x * config.CELL + margen,
        config.HUD + y * config.CELL + margen,
        config.CELL - margen * 2,
        config.CELL - margen * 2,
    )


def dibujar_tablero(surface):
    """Fondo y rejilla del area de juego (US02)."""
    pygame.draw.rect(
        surface,
        config.FONDO,
        pygame.Rect(0, config.HUD, config.WIDTH, config.ROWS * config.CELL),
    )
    for x in range(config.COLS + 1):
        px = x * config.CELL
        pygame.draw.line(surface, config.REJILLA, (px, config.HUD), (px, config.HEIGHT))
    for y in range(config.ROWS + 1):
        py = config.HUD + y * config.CELL
        pygame.draw.line(surface, config.REJILLA, (0, py), (config.WIDTH, py))


def dibujar_serpiente(surface, serpiente):
    """Dibuja cada segmento del cuerpo de la serpiente (US02)."""
    for i, celda in enumerate(serpiente.body):
        color = config.CABEZA if i == 0 else config.CUERPO
        pygame.draw.rect(surface, color, _rect(celda), border_radius=5)


def dibujar_alimento(surface, alimento):
    """Dibuja el alimento en su posicion actual (US02)."""
    if alimento is not None:
        pygame.draw.ellipse(surface, config.ALIMENTO, _rect(alimento, margen=4))


def dibujar_juego(surface, juego):
    """Un cuadro completo de la partida en curso (US02)."""
    dibujar_tablero(surface)
    dibujar_alimento(surface, juego.alimento)
    if juego.serpiente:
        dibujar_serpiente(surface, juego.serpiente)
