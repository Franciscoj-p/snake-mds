
import random

from snake import config


def dentro_del_tablero(celda):
    """True si la celda esta dentro de los limites (US09)."""
    x, y = celda
    return 0 <= x < config.COLS and 0 <= y < config.ROWS


def nuevo_alimento(ocupadas, rng=None):
    """Una celda libre al azar, o None si el tablero esta lleno (US06).

    rng se puede pasar para que las pruebas den siempre el mismo resultado.
    """
    rng = rng or random
    libres = [
        (x, y)
        for x in range(config.COLS)
        for y in range(config.ROWS)
        if (x, y) not in ocupadas
    ]
    return rng.choice(libres) if libres else None


class Puntaje:
    """Contador de puntos de la partida (US07)."""

    def __init__(self):
        self.valor = 0

    def comer(self):
        self.valor += config.PUNTOS_POR_ALIMENTO

    def reiniciar(self):
        self.valor = 0
