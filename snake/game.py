"""Une todo: serpiente, tablero, alimento y puntaje.

ARCHIVO COMPARTIDO. Se escribe completo el sabado 7 entre Persona 2 y
Persona 5. Despues solo se cambia por Pull Request. Las demas personas
programan usando estos metodos sin abrir este archivo.

Historias: US03 (iniciar), US05 (avanzar), US06, US07, US09, US10
"""

import random

from snake import config
from snake.snake_logic import Serpiente
from snake.world import Puntaje, dentro_del_tablero, nuevo_alimento

# Estados posibles del juego
MENU = "menu"
JUGANDO = "jugando"
PERDIO = "perdio"

# Por que se perdio
POR_BORDE = "borde"
POR_COLA = "cola"


class Juego:
    def __init__(self, rng=None):
        self.rng = rng or random.Random()
        self.puntaje = Puntaje()
        self.estado = MENU
        self.causa = None
        self.serpiente = None
        self.alimento = None

    def iniciar(self):
        """Arranca una partida nueva (US03 y US10)."""
        self.serpiente = Serpiente(
            config.COLS // 2, config.ROWS // 2, config.LARGO_INICIAL
        )
        self.puntaje.reiniciar()
        self.causa = None
        self.alimento = nuevo_alimento(set(self.serpiente.body), self.rng)
        self.estado = JUGANDO

    def girar(self, direccion):
        """Cambia la direccion si el juego esta en curso (US04)."""
        if self.estado != JUGANDO:
            return False
        return self.serpiente.girar(direccion)

    def tick(self):
        """Avanza la partida un paso (US05).

        Orden: mirar a donde va la cabeza, revisar borde, revisar cola,
        avanzar, y si comio sumar puntos y poner alimento nuevo.
        """
        if self.estado != JUGANDO:
            return

        destino = self.serpiente.proxima_celda()

        if not dentro_del_tablero(destino):
            self.estado, self.causa = PERDIO, POR_BORDE
            return

        come = destino == self.alimento

        if self.serpiente.se_muerde(destino, come):
            self.estado, self.causa = PERDIO, POR_COLA
            return

        self.serpiente.avanzar(crecer=come)

        if come:
            self.puntaje.comer()
            self.alimento = nuevo_alimento(set(self.serpiente.body), self.rng)

    @property
    def largo(self):
        return len(self.serpiente) if self.serpiente else 0
