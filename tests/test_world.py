"""Pruebas del modulo world (US06 y US07). Duenio: Persona 4."""
import random

from snake import config
from snake.world import Puntaje, dentro_del_tablero, nuevo_alimento


def test_las_cuatro_esquinas_estan_dentro():
    assert dentro_del_tablero((0, 0))
    assert dentro_del_tablero((config.COLS - 1, 0))
    assert dentro_del_tablero((0, config.ROWS - 1))
    assert dentro_del_tablero((config.COLS - 1, config.ROWS - 1))


def test_celdas_fuera_del_tablero():
    assert not dentro_del_tablero((-1, 0))
    assert not dentro_del_tablero((0, -1))
    assert not dentro_del_tablero((config.COLS, 0))
    assert not dentro_del_tablero((0, config.ROWS))


def test_alimento_siempre_dentro_y_libre():
    """US06: 200 intentos, todos dentro del tablero y fuera de la serpiente."""
    rng = random.Random(1)
    ocupadas = {(x, 5) for x in range(config.COLS)}
    for _ in range(200):
        celda = nuevo_alimento(ocupadas, rng)
        assert celda is not None
        assert celda not in ocupadas
        assert dentro_del_tablero(celda)


def test_tablero_lleno_devuelve_none():
    ocupadas = {(x, y) for x in range(config.COLS) for y in range(config.ROWS)}
    assert nuevo_alimento(ocupadas, random.Random(1)) is None


def test_una_sola_celda_libre_es_la_elegida():
    ocupadas = {(x, y) for x in range(config.COLS) for y in range(config.ROWS)}
    ocupadas.remove((3, 4))
    assert nuevo_alimento(ocupadas, random.Random(1)) == (3, 4)


def test_misma_semilla_mismo_alimento():
    a = nuevo_alimento(set(), random.Random(7))
    b = nuevo_alimento(set(), random.Random(7))
    assert a == b


def test_puntaje_empieza_en_cero():
    assert Puntaje().valor == 0


def test_comer_suma_diez_y_reiniciar_vuelve_a_cero():
    p = Puntaje()
    p.comer()
    p.comer()
    assert p.valor == 2 * config.PUNTOS_POR_ALIMENTO
    p.reiniciar()
    assert p.valor == 0