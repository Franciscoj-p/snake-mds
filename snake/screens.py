"""Pantallas de menu y de fin de partida.

Persona 1
Historias: US01 (menu inicial), US10 (Game Over y reiniciar)
"""

import pygame

from snake import config, game

_fuentes = {}

# Un mensaje distinto por cada forma de perder (US10)
_MENSAJE = {
    game.POR_BORDE: "Chocaste contra el borde",
    game.POR_COLA: "Te mordiste la cola",
}


def _fuente(tam, negrita=False):
    """Crea la fuente una sola vez y la reutiliza."""
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


def dibujar_game_over(surface, juego):
    """Pantalla final: causa, puntaje y longitud finales, R y ESC (US10)."""
    surface.fill(config.FONDO_HUD)
    _centrar(surface, [
        ("GAME OVER", 44, config.ALIMENTO),
        (_MENSAJE.get(juego.causa, ""), 14, config.TEXTO_GRIS),
        (f"Puntaje final: {juego.puntaje.valor}", 20, config.TEXTO),
        (f"Longitud final: {juego.largo}", 20, config.TEXTO),
        ("R    -  Jugar otra vez", 20, config.TEXTO),
        ("ESC  -  Volver al menu", 20, config.TEXTO_GRIS),
    ])
