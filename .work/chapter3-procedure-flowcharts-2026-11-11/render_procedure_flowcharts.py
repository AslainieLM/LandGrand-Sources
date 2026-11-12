from dataclasses import dataclass
from hashlib import sha256
from math import ceil, hypot
from pathlib import Path
import json
import sys

from PIL import Image, ImageDraw, ImageFont


WIDTH = 768
PPI = 400
OUTPUT_WIDTH = 6 * PPI
SCALE = OUTPUT_WIDTH * 2 / WIDTH
INK = "#202933"
STROKE = "#35404c"
MUTED = "#455361"
PALE = "#f2f4f6"
WHITE = "#ffffff"
FONT_DIR = Path(r"C:\Windows\Fonts")

FONTS = {}


def font(size, bold=False):
    key = size, bold
    if key not in FONTS:
        face = "segoeuib.ttf" if bold else "segoeui.ttf"
        FONTS[key] = ImageFont.truetype(str(FONT_DIR / face), round(size * SCALE))
    return FONTS[key]


def pixels(point):
    return tuple(round(value * SCALE) for value in point)


@dataclass(frozen=True)
class Shape:
    kind: str
    x: float
    y: float
    w: float
    h: float

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    @property
    def right(self):
        return self.x + self.w

    @property
    def bottom(self):
        return self.y + self.h

    def span(self, y):
        if self.kind == "decision":
            half = self.w / 2 * (1 - abs(y - self.cy) / (self.h / 2))
            return self.cx - half, self.cx + half
        if self.kind == "connector" and y > self.y + self.h * 0.72:
            half = self.w / 2 * ((self.bottom - y) / (self.h * 0.28))
            return self.cx - half, self.cx + half
        if self.kind == "terminal":
            radius = self.h / 2
            inset = radius - max(0, radius**2 - (y - self.cy)**2)**0.5
            return self.x + inset, self.right - inset
        return self.x, self.right

    def contains(self, x, y):
        if not self.y + 0.4 < y < self.bottom - 0.4:
            return False
        left, right = self.span(y)
        return left + 0.4 < x < right - 0.4


@dataclass(frozen=True)
class Route:
    source: str
    target: str
    points: tuple
    data: bool
    arrow: bool


class Chart:
    def __init__(self, number, title, filename, height):
        self.number = number
        self.title = title
        self.filename = filename
        self.height = height
        self.nodes = {}
        self.routes = []
        self.labels = []
        self.junctions = []
        self.footer = None

    def node(self, key, kind, x, y, w, h, main, *detail):
        self.nodes[key] = Shape(kind, x, y, w, h), tuple(main.split("\n")), detail

    def route(self, source, target, *points, data=False, arrow=True):
        self.routes.append(Route(source, target, points, data, arrow))

    def label(self, x, y, text):
        self.labels.append((x, y, text))

    def validate(self):
        for key, (shape, _, _) in self.nodes.items():
            assert 16 <= shape.x < shape.right <= WIDTH - 16, (self.number, key)
            assert 90 <= shape.y < shape.bottom < self.height - 12, (self.number, key)
        for route in self.routes:
            for start, end in zip(route.points, route.points[1:]):
                assert start[0] == end[0] or start[1] == end[1], route
                assert start != end, route
                steps = ceil(hypot(end[0] - start[0], end[1] - start[1]) / 2)
                for i in range(1, steps):
                    x = start[0] + i / steps * (end[0] - start[0])
                    y = start[1] + i / steps * (end[1] - start[1])
                    for key, (shape, _, _) in self.nodes.items():
                        assert not shape.contains(x, y), (self.number, route, key, x, y)

    def draw(self, delivery, preview):
        self.validate()
        canvas = Image.new("RGB", pixels((WIDTH, self.height)), WHITE)
        draw = ImageDraw.Draw(canvas)
        draw.text(pixels((28, 24)), "Land Grand · Proposed game procedure",
                  font=font(16, True), fill=MUTED, anchor="lt")
        draw.text(pixels((28, 50)), f"{self.number}. {self.title}",
                  font=font(31, True), fill=INK, anchor="lt")

        for route in self.routes:
            draw_route(draw, route)
        for x, y in self.junctions:
            draw.ellipse(pixels((x - 3, y - 3, x + 3, y + 3)), fill=STROKE)
        for key, (shape, main, details) in self.nodes.items():
            if shape.kind == "difficulty":
                draw_difficulty(draw, shape)
                continue
            draw_shape(draw, shape)
            draw_node_text(draw, self.number, key, shape, main, details)
        for x, y, label in self.labels:
            x0, y0, x1, y1 = font(15.5, True).getbbox(label, anchor="mm")
            for key, (shape, _, _) in self.nodes.items():
                assert all(not shape.contains(x + dx / SCALE, y + dy / SCALE)
                           for dx in (x0, x1) for dy in (y0, y1)), (self.number, label, key)
            draw.text(pixels((x, y)), label, font=font(15.5, True), fill=INK, anchor="mm")
        if self.footer:
            draw.text(pixels((28, self.height - 24)), self.footer,
                      font=font(15.5), fill=MUTED, anchor="lb")

        path = delivery / self.filename
        target_height = round(self.height * OUTPUT_WIDTH / WIDTH)
        result = canvas.resize((OUTPUT_WIDTH, target_height), Image.Resampling.LANCZOS)
        result.save(path, dpi=(PPI, PPI), optimize=True)
        result.resize((WIDTH, self.height), Image.Resampling.LANCZOS).save(preview / self.filename)
        with Image.open(path) as reopened:
            assert reopened.size == (OUTPUT_WIDTH, target_height)
            assert round(reopened.info["dpi"][0]) == PPI
            reopened.verify()
        return {
            "filename": path.name,
            "size_px": [OUTPUT_WIDTH, target_height],
            "width_inches": 6,
            "height_inches": round(target_height / PPI, 2),
            "sha256": sha256(path.read_bytes()).hexdigest(),
        }


def draw_route(draw, route):
    points = route.points
    width = round((1.8 if route.data else 2.1) * SCALE)
    color = MUTED if route.data else STROKE
    if route.data:
        for start, end in zip(points, points[1:]):
            length = hypot(end[0] - start[0], end[1] - start[1])
            ux = (end[0] - start[0]) / length
            uy = (end[1] - start[1]) / length
            for offset in range(0, ceil(length), 12):
                limit = min(offset + 6, length)
                draw.line([pixels((start[0] + ux * offset, start[1] + uy * offset)),
                           pixels((start[0] + ux * limit, start[1] + uy * limit))],
                          fill=color, width=width)
    else:
        draw.line([pixels(p) for p in points], fill=color, width=width, joint="curve")
    if route.arrow:
        x, y = points[-1]
        ax, ay = points[-2]
        length = hypot(x - ax, y - ay)
        ux, uy = (x - ax) / length, (y - ay) / length
        bx, by = x - ux * 9, y - uy * 9
        triangle = [(x, y), (bx - uy * 4.8, by + ux * 4.8), (bx + uy * 4.8, by - ux * 4.8)]
        draw.polygon([pixels(p) for p in triangle], fill=color)


def draw_shape(draw, shape):
    x, y, r, b = shape.x, shape.y, shape.right, shape.bottom
    cx, cy = shape.cx, shape.cy
    bounds = pixels((x, y, r, b))
    width = round(2.1 * SCALE)
    if shape.kind == "terminal":
        draw.rounded_rectangle(bounds, radius=round(shape.h * SCALE / 2),
                               fill=PALE, outline=STROKE, width=width)
    elif shape.kind in ("decision", "connector"):
        if shape.kind == "decision":
            vertices = [(cx, y), (r, cy), (cx, b), (x, cy)]
        else:
            shoulder = y + shape.h * 0.72
            vertices = [(x, y), (r, y), (r, shoulder), (cx, b), (x, shoulder)]
        polygon = [pixels(p) for p in vertices]
        draw.polygon(polygon, fill=PALE)
        draw.line(polygon + polygon[:1], fill=STROKE, width=width, joint="curve")
    elif shape.kind == "storage":
        cap = 16
        draw.rectangle(pixels((x, y + cap, r, b - cap)), fill=PALE)
        draw.ellipse(pixels((x, b - cap * 2, r, b)), fill=PALE)
        draw.line([pixels((x, y + cap)), pixels((x, b - cap))], fill=STROKE, width=width)
        draw.line([pixels((r, y + cap)), pixels((r, b - cap))], fill=STROKE, width=width)
        draw.arc(pixels((x, b - cap * 2, r, b)), 0, 180, fill=STROKE, width=width)
        draw.ellipse(pixels((x, y, r, y + cap * 2)), fill=PALE, outline=STROKE, width=width)
    else:
        draw.rectangle(bounds, fill=WHITE, outline=STROKE, width=width)


def draw_node_text(draw, number, key, shape, main, details):
    if shape.kind == "connector":
        main_size, detail_size, center = 16.5, 15.5, shape.y + shape.h * 0.42
    elif shape.kind == "storage":
        main_size, detail_size, center = 17, 15.5, shape.cy + 5
    else:
        main_size, detail_size, center = 18.5, 16, shape.cy
    lines = [(line, main_size, True) for line in main]
    lines += [(line, detail_size, False) for line in details]
    band_height = sum(size + 2.5 for _, size, _ in lines)
    current = center - band_height / 2
    for line, size, bold in lines:
        face = font(size, bold)
        y = current + (size + 2.5) / 2
        a, t, z, b = face.getbbox(line, anchor="mm")
        upper, lower = y + t / SCALE, y + b / SCALE
        left = max(shape.span(upper)[0], shape.span(lower)[0])
        right = min(shape.span(upper)[1], shape.span(lower)[1])
        assert shape.y + 5 <= upper <= lower <= shape.bottom - 5, (number, key, line)
        assert shape.cx + a / SCALE >= left + 6, (number, key, line, "left")
        assert shape.cx + z / SCALE <= right - 6, (number, key, line, "right")
        draw.text(pixels((shape.cx, y)), line, font=face, fill=INK if bold else MUTED, anchor="mm")
        current += size + 2.5


def draw_difficulty(draw, shape):
    x, y, r, b = shape.x, shape.y, shape.right, shape.bottom
    draw.rectangle(pixels((x, y, r, b)), fill=PALE, outline=STROKE, width=round(1.7 * SCALE))
    draw.text(pixels((x + 17, y + 21)), "Levels per episode",
              font=font(18.5, True), fill=INK, anchor="lt")
    for row, (mode, count) in enumerate((("Easy", 3), ("Normal", 5), ("Hard", 7))):
        line_y = y + 66 + row * 34
        draw.text(pixels((x + 17, line_y)), mode,
                  font=font(17, True), fill=INK, anchor="lm")
        draw.text(pixels((r - 17, line_y)), str(count),
                  font=font(17), fill=INK, anchor="rm")
        draw.line([pixels((x + 17, line_y + 17)), pixels((r - 17, line_y + 17))],
                  fill="#b9c1ca", width=round(SCALE))
    for offset, label in [
        (171, "Finish Easy to unlock Normal."),
        (193, "Finish Normal to unlock Hard."),
        (229, "60 levels across four episodes."),
    ]:
        face = font(15.5, offset == 229)
        assert face.getlength(label) / SCALE <= shape.w - 34, label
        draw.text(pixels((x + 17, y + offset)), label, font=face, fill=INK, anchor="lm")


def startup():
    chart = Chart(1, "Startup and Main Menu", "01-startup-and-main-menu.png", 590)
    chart.node("open", "terminal", 210, 102, 348, 56, "Open Land Grand",
               "Single-player, offline · Android 10+")
    chart.node("load", "process", 261, 184, 246, 61, "Load available\nsaved progress")
    chart.node("local", "storage", 574, 168, 164, 92, "Local device", "Saved progress")
    chart.node("menu", "decision", 277, 291, 214, 114, "Main Menu")
    chart.node("settings", "process", 29, 320, 180, 56, "Open Settings")
    chart.node("tutorial", "process", 559, 320, 180, 56, "Open Tutorial")
    chart.node("A", "connector", 182, 500, 176, 60, "A · To Part 2", "Landform Map")
    chart.node("exit", "terminal", 419, 501, 158, 48, "Close game")
    chart.route("open", "load", (384, 158), (384, 184))
    chart.route("local", "load", (574, 214), (507, 214), data=True)
    chart.label(540, 196, "Load")
    chart.route("load", "menu", (384, 245), (384, 291))
    chart.route("menu", "settings", (277, 348), (209, 348))
    chart.route("menu", "tutorial", (491, 348), (559, 348))
    chart.label(243, 331, "Settings")
    chart.label(525, 331, "Tutorial")
    chart.route("settings", "menu", (119, 320), (119, 273), (384, 273), arrow=False)
    chart.route("tutorial", "menu", (649, 320), (649, 273), (384, 273), arrow=False)
    chart.junctions.append((384, 273))
    chart.label(251, 259, "Return")
    chart.label(516, 259, "Return")
    chart.route("menu", "choice", (384, 405), (384, 442), arrow=False)
    chart.route("choice", "A", (384, 442), (270, 442), (270, 500))
    chart.route("choice", "exit", (384, 442), (498, 442), (498, 501))
    chart.junctions.append((384, 442))
    chart.label(294, 471, "Play")
    chart.label(519, 471, "Exit")
    return chart


def selection():
    chart = Chart(2, "Episode and Level Selection", "02-episode-and-level-selection.png", 617)
    chart.node("A", "connector", 169, 103, 182, 58, "A · From Part 1 or 4", "Landform Map")
    chart.node("map", "process", 59, 197, 402, 81, "Show Landform Map",
               "Mountains, Hills, Plains, and Plateaus")
    chart.node("episode", "process", 84, 317, 352, 60, "Select an unlocked episode")
    chart.node("level", "process", 76, 416, 368, 72, "Select an available level",
               "Choose from unlocked difficulty modes")
    chart.node("B", "connector", 170, 528, 180, 58, "B · To Part 3", "Begin level")
    chart.node("modes", "difficulty", 478, 300, 262, 255, "")
    chart.route("A", "map", (260, 161), (260, 197))
    chart.route("map", "episode", (260, 278), (260, 317))
    chart.route("episode", "level", (260, 377), (260, 416))
    chart.route("level", "B", (260, 488), (260, 528))
    return chart


def gameplay():
    chart = Chart(3, "Lesson, Exploration, and Collection", "03-lesson-exploration-and-collection.png", 788)
    chart.node("B", "connector", 219, 100, 192, 60, "B · From Part 2 or 4", "Begin level")
    chart.node("lesson", "process", 124, 190, 382, 66, "Show a short Science lesson",
               "Landform and related rocks or minerals")
    chart.node("play", "process", 115, 285, 400, 84, "Explore the 2D level",
               "Move, jump, and collect items with touch controls",
               "Obstacles, traps, pitfalls, and time limits")
    chart.node("collect", "decision", 196, 397, 238, 106, "Rock or mineral\ncollected?")
    chart.node("item", "process", 499, 405, 241, 90, "Show item pop-up",
               "Illustration, name,", "and short description")
    chart.node("complete", "decision", 210, 554, 210, 96, "Level complete?")
    chart.node("C", "connector", 225, 698, 180, 59, "C · To Part 4", "Completed level")
    chart.route("B", "lesson", (315, 160), (315, 190))
    chart.route("lesson", "play", (315, 256), (315, 285))
    chart.route("play", "collect", (315, 369), (315, 397))
    chart.route("collect", "item", (434, 450), (499, 450))
    chart.label(466, 433, "Yes")
    chart.route("collect", "join", (315, 503), (315, 534), arrow=False)
    chart.label(336, 519, "No")
    chart.route("item", "join", (619.5, 495), (619.5, 534), (315, 534))
    chart.label(470, 518, "Return to play")
    chart.junctions.append((315, 534))
    chart.route("join", "complete", (315, 534), (315, 554))
    chart.route("complete", "play", (210, 602), (50, 602), (50, 327), (115, 327))
    chart.label(131, 585, "No · still active")
    chart.route("complete", "C", (315, 650), (315, 698))
    chart.label(337, 673, "Yes")
    return chart


def progression():
    chart = Chart(4, "Results, Saving, and Progression", "04-results-saving-and-progression.png", 973)
    chart.node("C", "connector", 271, 98, 186, 56, "C · From Part 3", "Completed level")
    chart.node("record", "process", 199, 175, 330, 72, "Record level progress",
               "Completion, stars, and collected items",
               "Update available levels and modes")
    chart.node("local", "storage", 582, 154, 151, 166, "Local device",
               "Player name", "Unlocked episodes", "Completed levels", "Earned stars", "Collected items")
    chart.node("results", "process", 200, 270, 328, 76, "Show Result Screen",
               "Collected items and short lesson review", "Up to three gameplay stars")
    chart.node("action", "decision", 276, 368, 176, 88, "Next action?")
    chart.node("B_replay", "connector", 32, 383, 173, 58, "B · To Part 3", "Replay this level")
    chart.node("episode", "decision", 246, 481, 236, 100, "Episode finished\nby this level?")
    chart.node("B_next", "connector", 32, 502, 173, 58, "B · To Part 3", "Next available level")
    chart.node("summary", "process", 201, 612, 326, 64, "Landform Description Screen",
               "Short summary of the landform")
    chart.node("all", "decision", 230, 693, 268, 98, "All four episodes\ncomplete?")
    chart.node("final", "terminal", 30, 788, 292, 90, "Completion Screen",
               "Total stars and collected items", "Congratulatory message")
    chart.node("unlock", "process", 459, 785, 254, 51, "Unlock the next episode")
    chart.node("A", "connector", 498, 868, 176, 58, "A · To Part 2", "Landform Map")
    chart.route("C", "record", (364, 154), (364, 175))
    chart.route("record", "local", (529, 211), (582, 211), data=True)
    chart.route("record", "results", (364, 247), (364, 270))
    chart.route("results", "action", (364, 346), (364, 368))
    chart.route("action", "B_replay", (276, 412), (205, 412))
    chart.label(241, 397, "Replay")
    chart.route("action", "episode", (364, 456), (364, 481))
    chart.label(408, 468, "Continue")
    chart.route("episode", "B_next", (246, 531), (205, 531))
    chart.label(226, 517, "No")
    chart.route("episode", "summary", (364, 581), (364, 612))
    chart.label(386, 596, "Yes")
    chart.route("summary", "all", (364, 676), (364, 693))
    chart.route("all", "final", (230, 742), (176, 742), (176, 788))
    chart.label(200, 727, "Yes")
    chart.route("all", "unlock", (498, 742), (586, 742), (586, 785))
    chart.label(543, 727, "No")
    chart.route("unlock", "A", (586, 836), (586, 868))
    chart.route("unlock", "local", (713, 810), (751, 810), (751, 242), (733, 242), data=True)
    chart.footer = "Dashed arrows show automatic saving to the device."
    return chart


def main():
    delivery, preview = map(Path, sys.argv[1:])
    delivery.mkdir(parents=True, exist_ok=True)
    preview.mkdir(parents=True, exist_ok=True)
    results = [chart.draw(delivery, preview) for chart in (startup(), selection(), gameplay(), progression())]
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()

