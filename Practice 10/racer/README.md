# Racer Game

## Objective

Build a simple lane-based racing game inspired by the CodersLegacy 3-part tutorial series, then extend it with collectible coins.

## Requirements

Install dependencies from repository root:

```bash
python -m pip install -r "Practice 10/requirements.txt"
```

## Run

```bash
python "Practice 10/racer/main.py"
```

## Controls

- `Left Arrow` - move to left lane
- `Right Arrow` - move to right lane
- `R` - restart after game over
- `Esc` - quit
- Close window - quit

## Features Checklist

- Player car and enemy car in lane-based movement
- Enemy collision leads to game over
- Restart from game-over screen without closing app
- Speed increases over time (custom timer event)
- Random coins appear on the road
- Coin collisions increase collected coin count
- Coin counter shown in top-right corner
- Local placeholder assets included in `assets/`
- Fallback drawing if asset load fails

## How It Works (Short)

1. `main.py` calls `run_racer_game()`.
2. `RacerGame` loads assets, creates sprite objects, and sets two timed events:
   - speed increase event
   - coin spawn event
3. Game loop:
   - read keyboard/events
   - move enemy and coins
   - check player collision with enemy (game over)
   - check player collision with coins (collect)
4. HUD draws speed and coin count each frame.
5. If collision with enemy happens, game-over overlay appears.
6. Player can press `R` to restart immediately or `Esc` to quit.

## Files

- `main.py` - entrypoint
- `racer.py` - main game logic
- `assets/road.png` - road background
- `assets/player_car.png` - player sprite
- `assets/enemy_car.png` - enemy sprite
- `assets/coin.png` - coin sprite
