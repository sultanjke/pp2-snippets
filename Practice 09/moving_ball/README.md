# Moving Ball Game

## Objective

Create a red ball that moves with arrow keys and stays inside the screen.

## Requirements

Install dependencies from repo root:

```bash
python -m pip install -r "Practice 09/requirements.txt"
```

## Run

```bash
python "Practice 09/moving_ball/main.py"
```

## Controls

- Arrow keys: move ball (`Up`, `Down`, `Left`, `Right`)
- Close window to quit

## Folder Files

- `main.py`: simple entrypoint that starts the game.
- `ball.py`: full game logic (input, movement, boundaries, drawing).

## How This Mini-Game Works (Step by Step)

1. `main.py` calls `run_ball_game()`.
2. `ball.py` creates a window with white background.
3. Ball starts at center of screen.
4. On each arrow-key press:
   - a new position is calculated by adding/subtracting `20`
   - the move is accepted only if the new position stays inside screen
5. If move is invalid (would go out of bounds), it is ignored.
6. Every frame:
   - screen is cleared to white
   - red ball is drawn with `pygame.draw.circle()`
   - display updates

## Brief Code Explanation

- Main constants:
  - `width = 800`, `height = 600`
  - `radius = 25` (ball size 50x50)
  - `step = 20` (movement amount)
- Key handling block:
  - reads `KEYDOWN` events
  - computes `new_x`, `new_y`
  - applies boundary check:
    - `radius <= new_x <= width - radius`
    - `radius <= new_y <= height - radius`
- Draw block:
  - `screen.fill((255, 255, 255))`
  - `pygame.draw.circle(screen, (220, 0, 0), (x, y), radius)`
  - `pygame.display.flip()`
- `clock.tick(60)` keeps animation smooth and stable.

## Key Notes

- Movement is step-based exactly as requested.
- Ball never leaves screen area.
