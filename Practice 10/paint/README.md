# Paint App

## Objective

Extend a basic Pygame paint program (inspired by NerdParadise input tutorial style) with:

- rectangle drawing
- circle drawing
- eraser
- color selection

## Requirements

Install dependencies from repository root:

```bash
python -m pip install -r "Practice 10/requirements.txt"
```

## Run

```bash
python "Practice 10/paint/main.py"
```

## Controls

- `Left click` tool buttons to select drawing mode
- `Left click` color boxes to select color
- `Left click + drag` on canvas to draw
- `Eraser` + `Left click + drag`: manual erasing (white brush)
- `Right click` on canvas: delete whole selected shape immediately
- `Esc` - quit
- Close window - quit

## Features Checklist

- Pen tool (free drawing)
- Rectangle tool (drag and release)
- Circle tool (drag and release)
- Eraser tool with manual mouse-hold erase
- Right-click full-shape deletion (works for pen strokes, rectangles, circles)
- Color selection palette
- Pen cursor icon in pen mode
- Eraser cursor icon in eraser mode
- Toolbar UI with selected tool/color highlight
- Beginner-level commented implementation

## How It Works (Short)

1. Toolbar is at top, canvas is below.
2. Drawn objects are stored as shapes (stroke/rectangle/circle), then rendered onto canvas.
3. Pen creates a stroke object from drag points.
4. Rectangle/Circle use preview while dragging and finalize on mouse release.
5. Left-drag in eraser mode creates erase strokes (white brush effect).
6. Right-click on a shape removes that whole shape from saved drawings.
7. Custom cursor icon is drawn for pen and eraser modes.

## Files

- `main.py` - entrypoint
- `paint_app.py` - full paint logic and UI handling
