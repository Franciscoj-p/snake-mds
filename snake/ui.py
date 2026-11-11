"""Dibujo del tablero, la serpiente, el alimento y el puntaje.

Duenio: Persona 5
Historias: US02 (ver el tablero), US08 (ver el puntaje)
"""

import pygame

from snake import config

_fuentes = {}


def fuente(tam, negrita=False):
    """Crea la fuente una sola vez y la reutiliza."""
    clave = (tam, negrita)
    if clave not in _fuentes:
        _fuentes[clave] = pygame.font.SysFont("consolas,monospace", tam, bold=negrita)
    return _fuentes[clave]


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
    for i, celda in enumerate(serpiente.body):
        color = config.CABEZA if i == 0 else config.CUERPO
        pygame.draw.rect(surface, color, _rect(celda), border_radius=5)


def dibujar_alimento(surface, alimento):
    if alimento is not None:
        pygame.draw.ellipse(surface, config.ALIMENTO, _rect(alimento, margen=4))


def dibujar_hud(surface, juego):
    """Franja superior con el puntaje y la longitud (US08)."""
    pygame.draw.rect(
        surface, config.FONDO_HUD, pygame.Rect(0, 0, config.WIDTH, config.HUD)
    )
    izq = fuente(20, True).render(f"PUNTOS {juego.puntaje.valor}", True, config.TEXTO)
    surface.blit(izq, (12, 10))
    der = fuente(14).render(f"LARGO {juego.largo}", True, config.TEXTO_GRIS)
    surface.blit(der, (config.WIDTH - der.get_width() - 12, 14))


def dibujar_juego(surface, juego):
    """Un cuadro completo de la partida en curso."""
    dibujar_tablero(surface)
    dibujar_alimento(surface, juego.alimento)
    dibujar_serpiente(surface, juego.serpiente)
    dibujar_hud(surface, juego)
