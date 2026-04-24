# Snake Game (Practice 11)

## Objective

Extend Practice 10 snake with weighted foods and food disappearing timer.

## Requirements

Install dependencies from repository root:

```bash
python -m pip install -r "Practice 11/requirements.txt"
```

## Run

```bash
python "Practice 11/snake/main.py"
```

## Controls

- `Arrow keys` - move snake
- `R` - restart after game over
- `Esc` - quit
- Close window - quit

## Features Checklist

- Weighted random food (`1`, `2`, `3` points)
- Food has timer and disappears after a few seconds
- Food timer shown in HUD
- Border and self collision detection
- Level and speed system from Practice 10 kept
- Simple comments in code

## How It Works (Short)

1. Game creates food with random weight and color.
2. Each food has spawn time and lifetime.
3. If food timer reaches zero, old food disappears and new one appears.
4. If snake eats food, score increases by food weight.
5. Score changes level and speed as before.

## Files

- `main.py` - entrypoint
- `snake.py` - full game logic
