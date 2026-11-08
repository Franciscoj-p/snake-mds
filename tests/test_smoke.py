"""Prueba inicial de verificacion de entorno y constantes."""
from snake import config

def test_config():
    assert config.WIDTH > 0
    assert config.HEIGHT > 0
    assert config.CELL == 24
