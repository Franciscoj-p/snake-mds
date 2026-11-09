"""La serpiente: direccion, avance y crecimiento.

Duenio: Persona 3
Historias: US04 (controlar), US05 (avanzar), US07 (crecer), US09 (morderse)

Una celda es una tupla (x, y). Una direccion tambien: (dx, dy).
"""

ARRIBA = (0, -1)
ABAJO = (0, 1)
IZQUIERDA = (-1, 0)
DERECHA = (1, 0)


class Serpiente:
    """body[0] es siempre la cabeza."""

    def __init__(self, x, y, largo=3):
        # El cuerpo se extiende hacia la izquierda de la cabeza.
        self.body = [(x - i, y) for i in range(largo)]
        self.direccion = DERECHA
        self._siguiente = DERECHA

    @property
    def cabeza(self):
        return self.body[0]

    def __len__(self):
        return len(self.body)

    def girar(self, direccion):
        """Guarda el giro para el proximo avance. False si es invalido (US04).

        Se rechaza el giro de 180 grados. El giro se aplica en el siguiente
        avance y no de inmediato: asi dos teclas en el mismo instante no
        pueden partir la serpiente.
        """
        opuesta = (-self.direccion[0], -self.direccion[1])
        if direccion == opuesta or direccion == self.direccion:
            return False
        self._siguiente = direccion
        return True

    def proxima_celda(self):
        """A donde va a llegar la cabeza en el siguiente avance."""
        x, y = self.cabeza
        dx, dy = self._siguiente
        return (x + dx, y + dy)

    def avanzar(self, crecer=False):
        """Mueve la serpiente una celda. Si crece, no suelta la cola (US07)."""
        self.direccion = self._siguiente
        self.body.insert(0, self.proxima_celda())
        if not crecer:
            self.body.pop()

    def se_muerde(self, celda, va_a_crecer):
        """True si esa celda choca con el cuerpo (US09).

        Si no va a crecer, la cola se libera en el mismo turno y no cuenta.
        """
        cuerpo = self.body if va_a_crecer else self.body[:-1]
        return celda in cuerpo