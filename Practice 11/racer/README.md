# Racer Game (Practice 11)

## Objective

Extend Practice 10 racer with weighted coins and extra enemy speed boost based on collected coins.

## Requirements

Install dependencies from repository root:

```bash
python -m pip install -r "Practice 11/requirements.txt"
```

## Run

```bash
python "Practice 11/racer/main.py"
```

## Controls

- `Left Arrow` - move to left lane
- `Right Arrow` - move to right lane
- `R` - restart after game over
- `Esc` - quit
- Close window - quit

## Features Checklist

- Weighted random coins (`1`, `2`, `3`)
- Coin weight is shown on coin sprite
- Enemy speed increases over time (timer event)
- Enemy speed also increases every `N` collected coins (`N = 8`)
- Game over + restart support
- Simple comments in code

## How It Works (Short)

1. Coins are spawned with random weights.
2. When player collects a coin, score increases by coin weight.
3. If total coins reach next threshold (`8`, `16`, `24`, ...), enemy speed goes up.
4. Timer event also increases speed over time.
5. Collision with enemy shows game-over overlay and allows restart.

## Files

- `main.py` - entrypoint
- `racer.py` - full game logic
- `assets/` - local images (road, cars, coin)
