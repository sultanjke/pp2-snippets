# Paint App (Practice 11)

## Objective

Extend Practice 10 paint app with more geometric tools:

- square
- right triangle
- equilateral triangle
- rhombus

## Requirements

Install dependencies from repository root:

```bash
python -m pip install -r "Practice 11/requirements.txt"
```

## Run

```bash
python "Practice 11/paint/main.py"
```

## Controls

- `Left click` tool buttons to select tool
- `Left click` color boxes to select color
- `Left click + drag` to draw selected shape/tool
- `Eraser` + `Left click + drag` for manual erase
- `Right click` on canvas to delete one full shape
- `Esc` - quit
- Close window - quit

## Features Checklist

- Pen
- Rectangle
- Circle
- Square
- Right triangle
- Equilateral triangle
- Rhombus
- Manual eraser and right-click delete
- Simple comments in code

## How It Works (Short)

1. App stores all drawings as shape objects.
2. New tools compute shape geometry from drag start/end.
3. Preview is shown while dragging.
4. On mouse release, shape is saved and drawn on canvas.
5. Right-click removes top-most selected shape.

## Files

- `main.py` - entrypoint
- `paint_app.py` - full paint logic
