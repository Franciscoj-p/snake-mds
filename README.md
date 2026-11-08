# Snake — Metodologías de Desarrollo de Software

Juego Snake desarrollado con Scrum en una semana por un equipo de 5 personas.
Universidad del Valle — Escuela de Ingeniería Eléctrica y Electrónica.

## Instalación

```bash
git clone <url-del-repo>
cd snake-mds

python -m venv .venv
# Windows (PowerShell):  .venv\Scripts\Activate.ps1
# Linux o Mac:           source .venv/bin/activate

pip install -r requirements.txt
```

## Jugar

```bash
python -m snake.main
```

| Tecla | Acción |
| --- | --- |
| Flechas o WASD | Mover la serpiente |
| ENTER | Iniciar la partida desde el menú |
| R | Jugar otra vez tras perder |
| ESC | Volver al menú o salir |

## Pruebas

```bash
pytest
```

18 pruebas que cubren las 10 historias de usuario.

## Equipo y archivos

| Persona | Rol | Administra | Su archivo |
| --- | --- | --- | --- |
| Persona 1 | Product Owner | Confluence | `snake/screens.py` |
| Persona 2 | Scrum Master | Jira | `snake/config.py`, `snake/main.py` |
| Persona 3 | Desarrollo | — | `snake/snake_logic.py` |
| Persona 4 | Desarrollo | — | `snake/world.py` |
| Persona 5 | Desarrollo y calidad | GitHub | `snake/ui.py`, `tests/` |

`snake/game.py` es compartido: se escribió el sábado entre las Personas 2 y 5,
y después solo cambia por Pull Request.
