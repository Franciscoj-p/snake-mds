"""Pruebas del juego. Duenia: Persona 5.

Cubren las 10 historias de usuario. Corren sin abrir ventana.
"""

import random

import pytest

from snake import config, game
from snake.snake_logic import ABAJO, ARRIBA, DERECHA, IZQUIERDA, Serpiente
from snake.world import dentro_del_tablero, nuevo_alimento


def partida(seed=3):
    j = game.Juego(rng=random.Random(seed))
    j.iniciar()
    return j


# ---------- US04: controlar la serpiente ----------

def test_girar_a_un_lado_funciona():
    s = Serpiente(5, 5)
    assert s.girar(ARRIBA) is True
    s.avanzar()
    assert s.cabeza == (5, 4)


def test_girar_180_grados_se_rechaza():
    s = Serpiente(5, 5)
    assert s.girar(IZQUIERDA) is False
    s.avanzar()
    assert s.cabeza == (6, 5)


def test_repetir_la_misma_direccion_no_hace_nada():
    s = Serpiente(5, 5)
    assert s.girar(DERECHA) is False


def test_dos_giros_antes_de_avanzar_no_parten_la_serpiente():
    s = Serpiente(5, 5)
    s.girar(ARRIBA)
    s.avanzar()
    assert s.girar(ABAJO) is False


# ---------- US05: avance automatico ----------

def test_la_serpiente_avanza_y_suelta_la_cola():
    s = Serpiente(5, 5, largo=3)
    assert s.body == [(5, 5), (4, 5), (3, 5)]
    s.avanzar()
    assert s.cabeza == (6, 5)
    assert len(s) == 3
    assert (3, 5) not in s.body


def test_tick_mueve_la_serpiente():
    j = partida()
    antes = j.serpiente.cabeza
    j.tick()
    assert j.serpiente.cabeza != antes


# ---------- US02: limites del tablero ----------

def test_dentro_del_tablero():
    assert dentro_del_tablero((0, 0)) is True
    assert dentro_del_tablero((config.COLS - 1, config.ROWS - 1)) is True
    assert dentro_del_tablero((-1, 0)) is False
    assert dentro_del_tablero((config.COLS, 0)) is False


# ---------- US06: generar alimento ----------

def test_el_alimento_nunca_cae_sobre_la_serpiente():
    rng = random.Random(42)
    ocupadas = {(x, 5) for x in range(config.COLS)}
    for _ in range(200):
        celda = nuevo_alimento(ocupadas, rng)
        assert celda not in ocupadas
        assert dentro_del_tablero(celda)


def test_si_el_tablero_esta_lleno_no_hay_alimento():
    todas = {(x, y) for x in range(config.COLS) for y in range(config.ROWS)}
    assert nuevo_alimento(todas, random.Random(1)) is None


# ---------- US03: iniciar partida ----------

def test_el_juego_arranca_en_el_menu():
    j = game.Juego(rng=random.Random(1))
    assert j.estado == game.MENU
    assert j.serpiente is None


def test_iniciar_crea_serpiente_y_alimento():
    j = partida()
    assert j.estado == game.JUGANDO
    assert len(j.serpiente) == config.LARGO_INICIAL
    assert j.alimento is not None
    assert j.alimento not in j.serpiente.body
    assert j.puntaje.valor == 0


# ---------- US06 + US07: comer, crecer y puntuar ----------

def test_comer_suma_puntos_y_alarga():
    j = partida()
    largo = len(j.serpiente)
    j.alimento = j.serpiente.proxima_celda()   # ponemos el alimento delante
    j.tick()
    assert j.puntaje.valor == config.PUNTOS_POR_ALIMENTO
    assert len(j.serpiente) == largo + 1
    assert j.alimento != j.serpiente.cabeza    # se repuso en otra celda


def test_comer_dos_veces_suma_dos_veces():
    j = partida()
    for _ in range(2):
        j.alimento = j.serpiente.proxima_celda()
        j.tick()
    assert j.puntaje.valor == 2 * config.PUNTOS_POR_ALIMENTO
    assert len(j.serpiente) == config.LARGO_INICIAL + 2


# ---------- US09: perder al chocar ----------

def test_chocar_con_el_borde_termina_la_partida():
    j = partida()
    j.girar(ARRIBA)
    for _ in range(40):
        j.tick()
    assert j.estado == game.PERDIO
    assert j.causa == game.POR_BORDE


def test_morderse_la_cola_termina_la_partida():
    j = partida()
    for _ in range(6):                      # alargar hasta 9 segmentos
        j.alimento = j.serpiente.proxima_celda()
        j.tick()
    assert len(j.serpiente) == config.LARGO_INICIAL + 6
    j.alimento = (0, 0)                     # lejos, para que no interfiera
    for d in (ARRIBA, IZQUIERDA, ABAJO, DERECHA):
        j.girar(d)
        j.tick()
        if j.estado == game.PERDIO:
            break
    assert j.estado == game.PERDIO
    assert j.causa == game.POR_COLA


def test_seguir_a_la_cola_de_cerca_no_es_choque():
    """La cola se libera en el mismo turno, asi que no cuenta como mordida."""
    s = Serpiente(5, 5, largo=3)
    assert s.se_muerde((3, 5), va_a_crecer=False) is False
    assert s.se_muerde((3, 5), va_a_crecer=True) is True


def test_despues_de_perder_no_se_mueve_ni_gira():
    j = partida()
    j.girar(ARRIBA)
    for _ in range(40):
        j.tick()
    cabeza = j.serpiente.cabeza
    j.tick()
    assert j.serpiente.cabeza == cabeza
    assert j.girar(IZQUIERDA) is False


# ---------- US10: reiniciar ----------

def test_reiniciar_deja_todo_en_cero():
    j = partida()
    j.alimento = j.serpiente.proxima_celda()
    j.tick()
    assert j.puntaje.valor > 0
    j.girar(ARRIBA)
    for _ in range(40):
        j.tick()
    assert j.estado == game.PERDIO
    j.iniciar()
    assert j.estado == game.JUGANDO
    assert j.puntaje.valor == 0
    assert j.causa is None
    assert len(j.serpiente) == config.LARGO_INICIAL
