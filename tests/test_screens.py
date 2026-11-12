"""Pruebas de la pantalla de Game Over (US10). Duenia: Persona 1.

Corren sin abrir ventana: dibujan sobre una Surface en memoria.
"""

import random

import pygame
import pytest

from snake import config, game, screens

TAMANIO = (config.WIDTH, config.HEIGHT)


@pytest.fixture(autouse=True, scope="module")
def fuentes():
    pygame.font.init()


def perder_contra_el_borde():
    j = game.Juego(rng=random.Random(3))
    j.iniciar()
    for _ in range(config.COLS):
        j.tick()
    assert j.estado == game.PERDIO and j.causa == game.POR_BORDE
    return j


def pantalla(juego):
    surface = pygame.Surface(TAMANIO)
    screens.dibujar_game_over(surface, juego)
    return pygame.image.tobytes(surface, "RGB")


def test_game_over_dibuja_sobre_el_fondo():
    surface = pygame.Surface(TAMANIO)
    screens.dibujar_game_over(surface, perder_contra_el_borde())
    vacia = pygame.Surface(TAMANIO)
    vacia.fill(config.FONDO_HUD)
    assert tuple(surface.get_at((0, 0)))[:3] == config.FONDO_HUD
    assert pygame.image.tobytes(surface, "RGB") != pygame.image.tobytes(vacia, "RGB")


def test_chocar_y_morderse_muestran_mensajes_distintos():
    borde = perder_contra_el_borde()
    cola = perder_contra_el_borde()
    cola.causa = game.POR_COLA
    assert screens._MENSAJE[game.POR_BORDE] != screens._MENSAJE[game.POR_COLA]
    assert pantalla(borde) != pantalla(cola)


def test_game_over_muestra_el_puntaje_final():
    sin_puntos = perder_contra_el_borde()
    con_puntos = perder_contra_el_borde()
    con_puntos.puntaje.comer()
    assert pantalla(sin_puntos) != pantalla(con_puntos)


def test_game_over_sin_causa_no_falla():
    pantalla(game.Juego())
