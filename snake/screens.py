"""Pantallas de menu y de fin de partida.

Persona 1
Historias: US01 (menu inicial), US10 (Game Over y reiniciar)
"""

import pygame

from snake import config

_fuentes = {}


def _fuente(tam, negrita=False):
    

    clave = (tam, negrita)
    if clave not in _fuentes:
        _fuentes[clave] = pygame.font.SysFont("consolas,monospace", tam, bold=negrita)
    return _fuentes[clave]


def _centrar(surface, lineas):
    """Dibuja una lista de texto, tamaño, color centrada en la pantalla."""
    alto = sum(tam + 14 for _, tam, _ in lineas)
    y = (config.HEIGHT - alto) // 2
    for texto, tam, color in lineas:
        img = _fuente(tam, tam >= 40).render(texto, True, color)
        surface.blit(img, ((config.WIDTH - img.get_width()) // 2, y))
        y += tam + 14


def dibujar_menu(surface):
    """Pantalla de inicio: titulo SNAKE, ENTER inicia y ESC cierra."""
    surface.fill(config.FONDO_HUD)
    _centrar(surface, [
        ("SNAKE", 44, config.CABEZA),
        ("Metodologias de Desarrollo de Software", 14, config.TEXTO_GRIS),
        ("ENTER  -  Jugar", 20, config.TEXTO),
        ("ESC    -  Salir", 20, config.TEXTO_GRIS),
    ])
