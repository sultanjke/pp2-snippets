# Snake Game

## Objective

Extend a lecture-style Snake game with wall collision checks, safe food generation, levels, speed increase, and counters for score/level.

## Requirements

Install dependencies from repository root:

```bash
python -m pip install -r "Practice 10/requirements.txt"
```

## Run

```bash
python "Practice 10/snake/main.py"
```

## Controls

- `Arrow keys` - move snake
- `R` - restart after game over
- `Esc` - quit
- Close window - quit

## Features Checklist

- Border wall collision detection
- Self-collision detection
- Food spawn avoids walls and snake body
- Score counter always visible
- Level counter always visible
- Level increases every 4 foods
- Snake speed increases on each new level
- Beginner-friendly commented code

## How It Works (Short)

1. Game uses a grid board (`24 x 24` cells).
2. Border cells are treated as walls.
3. Snake moves one cell each tick based on direction.
4. If snake hits wall or itself -> game over.
5. Food is generated only from free inner cells.
6. Eating food increases score; every 4 foods increases level.
7. Each level raises movement speed.

## Files

- `main.py` - entrypoint
- `snake.py` - full game logic (movement, collisions, levels, rendering)
