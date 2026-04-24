from __future__ import annotations

import pygame


WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
TOOLBAR_HEIGHT = 110

CANVAS_WIDTH = WINDOW_WIDTH
CANVAS_HEIGHT = WINDOW_HEIGHT - TOOLBAR_HEIGHT


class PaintApp:
    """Simple paint app with pen, rectangle, circle, eraser, and color palette."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Practice 10 - Paint")

        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20, bold=True)

        # Canvas stores final (committed) drawings.
        self.canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
        self.canvas.fill((255, 255, 255))

        self.tools = []
        self.colors = []
        self.build_toolbar()

        self.current_tool = "pen"
        self.current_color = (0, 0, 0)

        self.pen_size = 4
        self.eraser_size = 22
        self.shape_border_width = 3

        # Store drawn shapes so they can be selected and deleted later.
        self.shapes: list[dict[str, object]] = []
        self.erase_strokes: list[dict[str, object]] = []

        # Temporary state while drawing.
        self.is_drawing = False
        self.start_pos: tuple[int, int] | None = None
        self.current_pos: tuple[int, int] | None = None
        self.active_stroke_points: list[tuple[int, int]] = []

        # Custom cursor icons for pen/eraser modes.
        self.pen_cursor, self.pen_hotspot = self.create_pen_cursor_icon()
        self.eraser_cursor, self.eraser_hotspot = self.create_eraser_cursor_icon()
        pygame.mouse.set_visible(False)

    def build_toolbar(self) -> None:
        # Tool button layout
        tool_names = ["pen", "rectangle", "circle", "eraser"]
        x = 12
        y = 14
        button_width = 130
        button_height = 36

        for name in tool_names:
            rect = pygame.Rect(x, y, button_width, button_height)
            self.tools.append((name, rect))
            x += button_width + 10

        # Color palette layout
        palette = [
            (0, 0, 0),
            (255, 0, 0),
            (0, 120, 255),
            (40, 170, 70),
            (255, 180, 0),
            (170, 65, 225),
            (120, 120, 120),
            (255, 255, 255),
        ]
        color_x = 14
        color_y = 64
        color_size = 34

        for color in palette:
            rect = pygame.Rect(color_x, color_y, color_size, color_size)
            self.colors.append((color, rect))
            color_x += color_size + 10

    def get_canvas_pos(self, screen_pos: tuple[int, int]) -> tuple[int, int] | None:
        sx, sy = screen_pos
        cy = sy - TOOLBAR_HEIGHT

        if 0 <= sx < CANVAS_WIDTH and 0 <= cy < CANVAS_HEIGHT:
            return (sx, cy)
        return None

    def create_pen_cursor_icon(self) -> tuple[pygame.Surface, tuple[int, int]]:
        surface = pygame.Surface((26, 26), pygame.SRCALPHA)

        # Pen body
        pygame.draw.polygon(surface, (60, 70, 85), [(5, 3), (21, 19), (16, 24), (0, 8)])
        # Pen highlight
        pygame.draw.polygon(surface, (120, 136, 154), [(7, 4), (17, 14), (14, 17), (4, 7)])
        # Pen tip
        pygame.draw.polygon(surface, (236, 216, 175), [(16, 24), (22, 18), (24, 20), (18, 26)])
        pygame.draw.polygon(surface, (40, 40, 40), [(20, 22), (24, 20), (22, 24)])

        # Cursor "hotspot" is where drawing actually happens.
        hotspot = (20, 22)
        return surface, hotspot

    def create_eraser_cursor_icon(self) -> tuple[pygame.Surface, tuple[int, int]]:
        surface = pygame.Surface((26, 26), pygame.SRCALPHA)

        pygame.draw.rect(surface, (245, 127, 151), (4, 6, 18, 14), border_radius=4)
        pygame.draw.rect(surface, (255, 255, 255), (4, 6, 9, 14), border_radius=4)
        pygame.draw.rect(surface, (95, 95, 100), (4, 6, 18, 14), width=2, border_radius=4)

        hotspot = (13, 13)
        return surface, hotspot

    def get_drag_rect(self, start: tuple[int, int], end: tuple[int, int]) -> pygame.Rect:
        left = min(start[0], end[0])
        top = min(start[1], end[1])
        width = abs(start[0] - end[0])
        height = abs(start[1] - end[1])
        return pygame.Rect(left, top, width, height)

    def draw_shape(self, surface: pygame.Surface, shape: dict[str, object]) -> None:
        shape_type = str(shape["type"])

        if shape_type == "stroke":
            points = list(shape["points"])  # type: ignore[arg-type]
            color = tuple(shape["color"])  # type: ignore[arg-type]
            width = int(shape["width"])
            if len(points) <= 1:
                pygame.draw.circle(surface, color, points[0], max(1, width // 2))
            else:
                pygame.draw.lines(surface, color, False, points, width)

        elif shape_type == "rectangle":
            rect = pygame.Rect(shape["rect"])  # type: ignore[arg-type]
            color = tuple(shape["color"])  # type: ignore[arg-type]
            width = int(shape["width"])
            pygame.draw.rect(surface, color, rect, width=width)

        elif shape_type == "circle":
            rect = pygame.Rect(shape["rect"])  # type: ignore[arg-type]
            color = tuple(shape["color"])  # type: ignore[arg-type]
            width = int(shape["width"])
            pygame.draw.ellipse(surface, color, rect, width=width)

    def rebuild_canvas(self) -> None:
        self.canvas.fill((255, 255, 255))
        for shape in self.shapes:
            self.draw_shape(self.canvas, shape)
        for erase_stroke in self.erase_strokes:
            self.draw_shape(self.canvas, erase_stroke)

    def point_to_segment_distance(
        self,
        point: tuple[int, int],
        a: tuple[int, int],
        b: tuple[int, int],
    ) -> float:
        px, py = point
        ax, ay = a
        bx, by = b

        abx = bx - ax
        aby = by - ay
        apx = px - ax
        apy = py - ay

        ab_len_sq = abx * abx + aby * aby
        if ab_len_sq == 0:
            return ((px - ax) ** 2 + (py - ay) ** 2) ** 0.5

        t = (apx * abx + apy * aby) / ab_len_sq
        t = max(0.0, min(1.0, t))

        closest_x = ax + t * abx
        closest_y = ay + t * aby
        return ((px - closest_x) ** 2 + (py - closest_y) ** 2) ** 0.5

    def point_hits_shape(self, point: tuple[int, int], shape: dict[str, object]) -> bool:
        shape_type = str(shape["type"])

        if shape_type == "stroke":
            points = list(shape["points"])  # type: ignore[arg-type]
            width = int(shape["width"])
            threshold = max(6, width + 3)

            if len(points) == 1:
                dx = point[0] - points[0][0]
                dy = point[1] - points[0][1]
                return (dx * dx + dy * dy) <= threshold * threshold

            for index in range(len(points) - 1):
                dist = self.point_to_segment_distance(point, points[index], points[index + 1])
                if dist <= threshold:
                    return True
            return False

        if shape_type in {"rectangle", "circle"}:
            rect = pygame.Rect(shape["rect"])  # type: ignore[arg-type]
            return rect.inflate(8, 8).collidepoint(point)

        return False

    def get_shape_index_at_point(self, point: tuple[int, int]) -> int:
        # Remove top-most shape first (last drawn = highest index).
        for index in range(len(self.shapes) - 1, -1, -1):
            if self.point_hits_shape(point, self.shapes[index]):
                return index
        return -1

    def delete_shape_at_point(self, point: tuple[int, int]) -> bool:
        index = self.get_shape_index_at_point(point)
        if index == -1:
            return False

        del self.shapes[index]
        self.rebuild_canvas()
        return True

    def handle_left_mouse_down(self, pos: tuple[int, int]) -> None:
        # Check tool clicks.
        for tool_name, rect in self.tools:
            if rect.collidepoint(pos):
                self.current_tool = tool_name
                return

        # Check color clicks.
        for color, rect in self.colors:
            if rect.collidepoint(pos):
                self.current_color = color
                return

        # If click is on canvas, start drawing.
        canvas_pos = self.get_canvas_pos(pos)
        if canvas_pos is None:
            return

        self.is_drawing = True
        self.start_pos = canvas_pos
        self.current_pos = canvas_pos

        # Pen and eraser both start stroke points from mouse down.
        if self.current_tool in {"pen", "eraser"}:
            self.active_stroke_points = [canvas_pos]

    def handle_mouse_motion(self, pos: tuple[int, int]) -> None:
        if not self.is_drawing:
            return

        canvas_pos = self.get_canvas_pos(pos)
        if canvas_pos is None:
            return

        self.current_pos = canvas_pos

        if self.current_tool in {"pen", "eraser"}:
            if not self.active_stroke_points or self.active_stroke_points[-1] != canvas_pos:
                self.active_stroke_points.append(canvas_pos)

    def handle_right_mouse_down(self, pos: tuple[int, int]) -> None:
        # Right-click deletes top-most whole shape immediately.
        canvas_pos = self.get_canvas_pos(pos)
        if canvas_pos is None:
            return
        self.delete_shape_at_point(canvas_pos)

    def handle_left_mouse_up(self, pos: tuple[int, int]) -> None:
        if not self.is_drawing:
            return

        end_pos = self.get_canvas_pos(pos)
        if end_pos is None:
            end_pos = self.current_pos

        # Save finished pen stroke.
        if self.start_pos is not None and end_pos is not None:
            if self.current_tool == "pen":
                if self.active_stroke_points:
                    self.shapes.append(
                        {
                            "type": "stroke",
                            "points": list(self.active_stroke_points),
                            "color": self.current_color,
                            "width": self.pen_size,
                        }
                    )
                    self.rebuild_canvas()

            elif self.current_tool == "eraser":
                if self.active_stroke_points:
                    self.erase_strokes.append(
                        {
                            "type": "stroke",
                            "points": list(self.active_stroke_points),
                            "color": (255, 255, 255),
                            "width": self.eraser_size,
                        }
                    )
                    self.rebuild_canvas()

            # Rectangle and circle are stored only after mouse release.
            elif self.current_tool == "rectangle":
                rect = self.get_drag_rect(self.start_pos, end_pos)
                if rect.width > 0 and rect.height > 0:
                    self.shapes.append(
                        {
                            "type": "rectangle",
                            "rect": rect,
                            "color": self.current_color,
                            "width": self.shape_border_width,
                        }
                    )
                    self.rebuild_canvas()

            elif self.current_tool == "circle":
                rect = self.get_drag_rect(self.start_pos, end_pos)
                if rect.width > 0 and rect.height > 0:
                    self.shapes.append(
                        {
                            "type": "circle",
                            "rect": rect,
                            "color": self.current_color,
                            "width": self.shape_border_width,
                        }
                    )
                    self.rebuild_canvas()

        self.is_drawing = False
        self.start_pos = None
        self.current_pos = None
        self.active_stroke_points = []

    def draw_toolbar(self) -> None:
        pygame.draw.rect(self.screen, (230, 230, 235), (0, 0, WINDOW_WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(self.screen, (170, 170, 180), (0, TOOLBAR_HEIGHT), (WINDOW_WIDTH, TOOLBAR_HEIGHT), 2)

        # Draw tool buttons.
        for tool_name, rect in self.tools:
            if tool_name == self.current_tool:
                color = (85, 145, 255)
            else:
                color = (205, 210, 220)
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            pygame.draw.rect(self.screen, (100, 100, 110), rect, width=2, border_radius=8)

            label = self.font.render(tool_name.upper(), True, (20, 20, 25))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)

        # Draw color buttons.
        for color, rect in self.colors:
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            border_color = (0, 0, 0) if color == self.current_color else (95, 95, 105)
            border_width = 3 if color == self.current_color else 1
            pygame.draw.rect(self.screen, border_color, rect, width=border_width, border_radius=5)

        info_text = self.font.render(
            "Left drag with eraser = manual erase | Right click = delete whole shape",
            True,
            (32, 32, 42),
        )
        self.screen.blit(info_text, (390, 74))

    def draw_preview_shape(self) -> None:
        # Show live preview while dragging.
        if not self.is_drawing:
            return

        if self.current_tool == "pen":
            if not self.active_stroke_points:
                return

            shifted_points = [(x, y + TOOLBAR_HEIGHT) for x, y in self.active_stroke_points]
            if len(shifted_points) == 1:
                pygame.draw.circle(
                    self.screen,
                    self.current_color,
                    shifted_points[0],
                    max(1, self.pen_size // 2),
                )
            else:
                pygame.draw.lines(self.screen, self.current_color, False, shifted_points, self.pen_size)
            return

        if self.current_tool == "eraser":
            if not self.active_stroke_points:
                return

            shifted_points = [(x, y + TOOLBAR_HEIGHT) for x, y in self.active_stroke_points]
            if len(shifted_points) == 1:
                pygame.draw.circle(
                    self.screen,
                    (255, 255, 255),
                    shifted_points[0],
                    max(1, self.eraser_size // 2),
                )
            else:
                pygame.draw.lines(
                    self.screen,
                    (255, 255, 255),
                    False,
                    shifted_points,
                    self.eraser_size,
                )
            return

        if self.current_tool in {"rectangle", "circle"}:
            if self.start_pos is None or self.current_pos is None:
                return

            preview_rect = self.get_drag_rect(self.start_pos, self.current_pos)
            screen_preview_rect = preview_rect.move(0, TOOLBAR_HEIGHT)

            if self.current_tool == "rectangle":
                pygame.draw.rect(self.screen, self.current_color, screen_preview_rect, width=2)
            elif self.current_tool == "circle":
                pygame.draw.ellipse(self.screen, self.current_color, screen_preview_rect, width=2)

    def draw_delete_highlight(self) -> None:
        mouse_pos = pygame.mouse.get_pos()
        canvas_pos = self.get_canvas_pos(mouse_pos)
        if canvas_pos is None:
            return

        index = self.get_shape_index_at_point(canvas_pos)
        if index == -1:
            return

        shape = self.shapes[index]
        shape_type = str(shape["type"])

        if shape_type in {"rectangle", "circle"}:
            rect = pygame.Rect(shape["rect"])  # type: ignore[arg-type]
            highlight_rect = rect.inflate(10, 10).move(0, TOOLBAR_HEIGHT)
        else:
            points = list(shape["points"])  # type: ignore[arg-type]
            min_x = min(point[0] for point in points)
            min_y = min(point[1] for point in points)
            max_x = max(point[0] for point in points)
            max_y = max(point[1] for point in points)
            highlight_rect = pygame.Rect(min_x, min_y, max_x - min_x, max_y - min_y).inflate(16, 16)
            highlight_rect.y += TOOLBAR_HEIGHT

        pygame.draw.rect(self.screen, (255, 80, 80), highlight_rect, width=2, border_radius=5)

    def draw_custom_cursor(self) -> None:
        mouse_x, mouse_y = pygame.mouse.get_pos()

        if self.current_tool == "pen":
            self.screen.blit(self.pen_cursor, (mouse_x - self.pen_hotspot[0], mouse_y - self.pen_hotspot[1]))
            return

        if self.current_tool == "eraser":
            self.screen.blit(
                self.eraser_cursor,
                (mouse_x - self.eraser_hotspot[0], mouse_y - self.eraser_hotspot[1]),
            )
            return

        # Default crosshair cursor for other tools.
        pygame.draw.line(self.screen, (35, 35, 35), (mouse_x - 8, mouse_y), (mouse_x + 8, mouse_y), 1)
        pygame.draw.line(self.screen, (35, 35, 35), (mouse_x, mouse_y - 8), (mouse_x, mouse_y + 8), 1)

    def draw(self) -> None:
        self.screen.fill((240, 240, 244))
        self.screen.blit(self.canvas, (0, TOOLBAR_HEIGHT))
        self.draw_toolbar()
        self.draw_preview_shape()
        self.draw_delete_highlight()
        self.draw_custom_cursor()

    def run(self) -> None:
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_left_mouse_down(event.pos)

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.handle_right_mouse_down(event.pos)

                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.handle_left_mouse_up(event.pos)

            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.mouse.set_visible(True)
        pygame.quit()


def run_paint_app() -> None:
    app = PaintApp()
    app.run()
