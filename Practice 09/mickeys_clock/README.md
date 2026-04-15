# Mickey's Clock Application

<img width="300" height="450" alt="mickeysclock" src="https://github.com/user-attachments/assets/884f3df5-77d6-45bb-940c-21d23a6aa7f3" />

## Objective

Create a Mickey-themed clock that uses Mickey hand graphics as clock hands.

## Requirements

Install dependencies from repo root:

```bash
python -m pip install -r "Practice 09/requirements.txt"
```

## Run

```bash
python "Practice 09/mickeys_clock/main.py"
```

## Controls

- Close the window to quit.

## Folder Files

- `main.py`: small starter file that runs the app.
- `clock.py`: all clock logic (time read, hand rotation, drawing).
- `images/mickey_hand.png`: hand image used for both left and right hands.

## How This Mini-Game Works (Step by Step)

1. `main.py` calls `run_clock_app()`.
2. `MickeyClockApp` creates the window, loads fonts, and loads `mickey_hand.png`.
3. In the main loop, the app reads current system time (`datetime.now()`).
4. It calculates:
   - minute angle = `minute * 6 + second * 0.1`
   - second angle = `second * 6`
5. It draws Mickey-style face and `MM:SS` text.
6. It rotates the hand image with `pygame.transform.rotate()` and draws:
   - right hand = minutes
   - left hand = seconds
7. The screen updates continuously, so each new second is shown in real-time.

## Brief Code Explanation

- `__init__` in `MickeyClockApp`:
  - sets screen size
  - prepares center position
  - loads image + fonts
  - initializes angle/time variables
- `update_time()`:
  - checks if second changed
  - recalculates angles and display text
- `draw_hand(pivot_pos, angle)`:
  - rotates image by angle
  - blits it centered on the hand pivot point
- `draw_background()`:
  - paints simple Mickey head and labels
  - draws current time text
- `run()`:
  - handles quit event
  - calls update + draw methods each frame
  - uses `Clock.tick(60)` for smooth refresh

## Key Notes

- Time display uses only **minutes and seconds** as requested.
- No manual second counter is used, so it stays synchronized with real system time.
