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
        if self.kind in ("terminal", "circle"):
            radius = self.h / 2
            inset = radius - max(0, radius**2 - (y - self.cy)**2)**0.5
            return self.x + inset, self.right - inset
        if self.kind == "io":
            fraction = (y - self.y) / self.h
            return self.x + 18 * (1 - fraction), self.right - 18 * fraction
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
        self.show_key = False

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
        draw.text(pixels((28, 24)), "Land Grand · Proposed gameplay process flowchart",
                  font=font(16, True), fill=MUTED, anchor="lt")
        draw.text(pixels((28, 50)), f"{self.number}. {self.title}",
                  font=font(31, True), fill=INK, anchor="lt")

        for route in self.routes:
            draw_route(draw, route)
        for x, y in self.junctions:
            draw.ellipse(pixels((x - 3, y - 3, x + 3, y + 3)), fill=STROKE)
        for key, (shape, main, details) in self.nodes.items():
            draw_shape(draw, shape)
            draw_node_text(draw, self.number, key, shape, main, details)
        for x, y, label in self.labels:
            x0, y0, x1, y1 = font(15.5, True).getbbox(label, anchor="mm")
            for key, (shape, _, _) in self.nodes.items():
                assert all(not shape.contains(x + dx / SCALE, y + dy / SCALE)
                           for dx in (x0, x1) for dy in (y0, y1)), (self.number, label, key)
            draw.text(pixels((x, y)), label, font=font(15.5, True), fill=INK, anchor="mm")
        if self.show_key:
            draw_shape_key(draw, self.height)
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
    if shape.kind in ("terminal", "circle"):
        draw.rounded_rectangle(bounds, radius=round(shape.h * SCALE / 2),
                               fill=PALE, outline=STROKE, width=width)
    elif shape.kind in ("decision", "connector", "io"):
        if shape.kind == "decision":
            vertices = [(cx, y), (r, cy), (cx, b), (x, cy)]
        elif shape.kind == "io":
            vertices = [(x + 18, y), (r, y), (r - 18, b), (x, b)]
        else:
            shoulder = y + shape.h * 0.72
            vertices = [(x, y), (r, y), (r, shoulder), (cx, b), (x, shoulder)]
        polygon = [pixels(p) for p in vertices]
        draw.polygon(polygon, fill=PALE)
        draw.line(polygon + polygon[:1], fill=STROKE, width=width, joint="curve")
    elif shape.kind == "storage":
        cap = min(16, shape.h / 4)
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



def draw_shape_key(draw, height):
    draw.text(pixels((28, height - 92)), "Flowchart symbols",
              font=font(16, True), fill=INK, anchor="lt")
    symbols = [
        ("terminal", "Start or end"),
        ("process", "Process"),
        ("io", "Input or output"),
        ("decision", "Decision"),
        ("storage", "Local storage"),
        ("connector", "Panel link"),
    ]
    for (kind, label), cx in zip(symbols, (75, 196, 320, 441, 566, 691)):
        draw_shape(draw, Shape(kind, cx - 26, height - 61, 52, 22))
        draw.text(pixels((cx, height - 21)), label,
                  font=font(15), fill=INK, anchor="mm")


def startup():
    chart = Chart(1, "Launch and Main Menu", "01-launch-and-main-menu.png", 912)
    chart.show_key = True
    chart.node("start", "terminal", 210, 99, 348, 57, "Open Land Grand",
               "Single-player, offline · Android 10+")
    chart.node("saved", "decision", 263, 182, 242, 114, "Saved progress\non this device?")
    chart.node("load", "process", 450, 318, 292, 106, "Load saved progress",
               "Player name and unlocked episodes",
               "Completed levels and earned stars",
               "Collected rocks and minerals")
    chart.node("M", "connector", 29, 394, 184, 60, "M · From Part 3", "Main Menu")
    chart.node("menu", "io", 198, 480, 372, 66, "Show Main Menu",
               "Play, Settings, Tutorial, and Exit")
    chart.node("choice", "decision", 282, 566, 204, 96, "Which option?")
    chart.node("settings", "io", 29, 587, 188, 54, "Show Settings")
    chart.node("tutorial", "io", 551, 587, 188, 54, "Show Tutorial")
    chart.node("A", "connector", 182, 736, 176, 60, "A · To Part 2", "Landform Map")
    chart.node("exit", "terminal", 414, 736, 168, 56, "Close Land Grand")

    chart.route("start", "saved", (384, 156), (384, 182))
    chart.route("saved", "load", (505, 239), (596, 239), (596, 318))
    chart.label(550, 224, "Yes")
    chart.route("saved", "main_join", (384, 296), (384, 460), arrow=False)
    chart.label(407, 322, "No")
    chart.route("load", "main_join", (596, 424), (596, 460), (384, 460), arrow=False)
    chart.route("M", "main_join", (121, 454), (121, 460), (384, 460), arrow=False)
    chart.junctions.append((384, 460))
    chart.route("main_join", "menu", (384, 460), (384, 480))
    chart.route("menu", "choice", (384, 546), (384, 566))
    chart.route("choice", "settings", (282, 614), (208, 614))
    chart.label(249, 598, "Settings")
    chart.route("choice", "tutorial", (486, 614), (560, 614))
    chart.label(523, 598, "Tutorial")
    chart.route("settings", "menu", (123, 587), (123, 513), (207, 513))
    chart.label(163, 498, "Return")
    chart.route("tutorial", "menu", (645, 587), (645, 513), (561, 513))
    chart.label(605, 498, "Return")
    chart.route("choice", "menu_split", (384, 662), (384, 694), arrow=False)
    chart.junctions.append((384, 694))
    chart.route("menu_split", "A", (384, 694), (270, 694), (270, 736))
    chart.label(292, 714, "Play")
    chart.route("menu_split", "exit", (384, 694), (498, 694), (498, 736))
    chart.label(521, 714, "Exit")
    return chart


def selection():
    chart = Chart(2, "Select an Episode and Level", "02-select-episode-and-level.png", 933)
    chart.node("A", "connector", 284, 99, 200, 59, "A · From Part 1 or 5", "Landform Map")
    chart.node("map", "io", 156, 181, 456, 72, "Show Landform Map",
               "Mountains, Hills, Plains, and Plateaus")
    chart.node("tap_episode", "io", 211, 275, 346, 51, "Tap a landform episode")
    chart.node("episode_unlocked", "decision", 258, 349, 252, 110,
               "Is that episode\nunlocked?")
    chart.node("modes", "io", 163, 482, 442, 76, "Show difficulty modes and levels",
               "3 Easy, 5 Normal, and 7 Hard per episode", "60 levels across four episodes")
    chart.node("tap_level", "io", 211, 580, 346, 51, "Tap a level in sequence")
    chart.node("level_unlocked", "decision", 248, 655, 272, 108,
               "Available in an\nunlocked mode?")
    chart.node("select", "process", 191, 786, 386, 51, "Set episode, difficulty, and level")
    chart.node("B", "connector", 294, 860, 180, 58, "B · To Part 3", "Start selected level")

    chart.route("A", "map", (384, 158), (384, 181))
    chart.route("map", "tap_episode", (384, 253), (384, 275))
    chart.route("tap_episode", "episode_unlocked", (384, 326), (384, 349))
    chart.route("episode_unlocked", "map", (258, 404), (56, 404), (56, 217), (165, 217))
    chart.label(155, 388, "No · stay on map")
    chart.route("episode_unlocked", "modes", (384, 459), (384, 482))
    chart.label(408, 470, "Yes")
    chart.route("modes", "tap_level", (384, 558), (384, 580))
    chart.route("tap_level", "level_unlocked", (384, 631), (384, 655))
    chart.route("level_unlocked", "modes", (520, 709), (703, 709), (703, 520), (596, 520))
    chart.label(605, 692, "No · choose again")
    chart.route("level_unlocked", "select", (384, 763), (384, 786))
    chart.label(408, 774, "Yes")
    chart.route("select", "B", (384, 837), (384, 860))
    return chart


def gameplay():
    chart = Chart(3, "Run the Lesson and Level", "03-lesson-gameplay-and-level-outcomes.png", 921)
    chart.node("B", "connector", 267, 98, 234, 58, "B · From Parts 2, 4, or 5", "Begin this level")
    chart.node("R_in", "circle", 121, 153, 40, 40, "R")
    chart.node("lesson", "io", 160, 194, 448, 75, "Show Lesson Screen",
               "Short lesson on the selected landform", "and related rocks or minerals")
    chart.node("start_level", "process", 260, 290, 248, 47, "Start this level")
    chart.node("play", "io", 162, 359, 444, 76, "Use the touch controls",
               "Move and jump through the 2D landform", "Obstacles, traps, pitfalls, and time limits")
    chart.node("event", "decision", 265, 470, 238, 126, "Level event?")
    chart.node("fail_options", "io", 21, 574, 248, 70, "Show attempt options",
               "Retry or Back to Main Menu")
    chart.node("fail_choice", "decision", 46, 668, 198, 90, "Next action?")
    chart.node("R_out", "circle", 59, 829, 40, 40, "R")
    chart.node("M", "connector", 154, 828, 186, 61, "M · To Part 1", "Main Menu")
    chart.node("item", "process", 502, 572, 240, 64, "Add the rock or mineral",
               "to this level's collection")
    chart.node("popup", "io", 499, 656, 246, 82, "Show item pop-up",
               "Illustration, name,", "and short description")
    chart.node("C", "connector", 294, 665, 180, 60, "C · To Part 4", "Level complete")

    chart.route("B", "retry_join", (384, 156), (384, 173), arrow=False)
    chart.route("R_in", "retry_join", (161, 173), (384, 173), arrow=False)
    chart.label(220, 158, "Same level")
    chart.junctions.append((384, 173))
    chart.route("retry_join", "lesson", (384, 173), (384, 194))
    chart.route("lesson", "start_level", (384, 269), (384, 290))
    chart.route("start_level", "play", (384, 337), (384, 359))
    chart.route("play", "event", (384, 435), (384, 470))

    chart.route("event", "play", (324.5, 501.5), (39, 501.5), (39, 397), (171, 397))
    chart.label(153, 486, "Play continues")
    chart.route("event", "fail_options", (265, 533), (145, 533), (145, 574))
    chart.label(207, 518, "Timeout or pit fall")
    chart.route("fail_options", "fail_choice", (145, 644), (145, 668))
    chart.route("fail_choice", "fail_split", (145, 758), (145, 784), arrow=False)
    chart.junctions.append((145, 784))
    chart.route("fail_split", "R_out", (145, 784), (79, 784), (79, 829))
    chart.label(105, 806, "Retry")
    chart.route("fail_split", "M", (145, 784), (247, 784), (247, 828))
    chart.label(247, 806, "Back to Main Menu")

    chart.route("event", "item", (503, 533), (622, 533), (622, 572))
    chart.label(562, 518, "Item collected")
    chart.route("item", "popup", (622, 636), (622, 656))
    chart.route("popup", "play", (622, 738), (622, 762), (752, 762), (752, 397), (597, 397))
    chart.label(687, 750, "Return to play")
    chart.route("event", "C", (384, 596), (384, 665))
    chart.label(451, 644, "End goal reached")
    return chart


def score_and_unlock():
    chart = Chart(4, "Score, Save, and Unlock Difficulty", "04-score-save-and-unlock-difficulty.png", 923)
    chart.node("C", "connector", 289, 97, 190, 58, "C · From Part 3", "Level complete")
    chart.node("score", "process", 177, 175, 414, 73, "Calculate gameplay stars",
               "Count the rocks collected in this level",
               "Apply the thresholds for up to three stars")
    chart.node("record", "process", 184, 270, 400, 64, "Record level results",
               "Completed level, stars, and collected items")
    chart.node("storage", "storage", 611, 257, 127, 90, "Local save", "Automatic")
    chart.node("mode", "decision", 265, 355, 238, 104, "Which difficulty\nwas played?")
    chart.node("easy_complete", "decision", 43, 475, 254, 104,
               "All 3 Easy\nlevels cleared?")
    chart.node("normal_complete", "decision", 471, 475, 254, 104,
               "All 5 Normal\nlevels cleared?")
    chart.node("normal", "process", 66, 608, 208, 50, "Unlock Normal")
    chart.node("hard", "process", 494, 608, 208, 50, "Unlock Hard")
    chart.node("results", "io", 160, 714, 448, 80, "Show Result Screen",
               "Collected rocks and minerals, short lesson review",
               "Up to three earned gameplay stars")
    chart.node("choice", "decision", 288, 815, 192, 88, "Next action?")
    chart.node("B", "connector", 25, 830, 195, 58, "B · To Part 3", "Replay same level")
    chart.node("D", "connector", 548, 830, 195, 58, "D · To Part 5", "Continue")

    chart.route("C", "score", (384, 155), (384, 175))
    chart.route("score", "record", (384, 248), (384, 270))
    chart.route("record", "storage", (584, 302), (611, 302), data=True)
    chart.route("record", "mode", (384, 334), (384, 355))
    chart.route("mode", "easy_complete", (265, 407), (170, 407), (170, 475))
    chart.label(215, 392, "Easy")
    chart.route("mode", "normal_complete", (503, 407), (598, 407), (598, 475))
    chart.label(550, 392, "Normal")
    chart.route("mode", "result_join", (384, 459), (384, 692), arrow=False)
    chart.label(408, 480, "Hard")

    chart.route("easy_complete", "normal", (170, 579), (170, 608))
    chart.label(194, 592, "Yes")
    chart.route("easy_complete", "easy_join", (297, 527), (322, 527), (322, 692), arrow=False)
    chart.label(321, 512, "No")
    chart.route("normal", "easy_join", (170, 658), (170, 692), (322, 692), arrow=False)
    chart.junctions.append((322, 692))
    chart.route("easy_join", "result_join", (322, 692), (384, 692), arrow=False)

    chart.route("normal_complete", "hard", (598, 579), (598, 608))
    chart.label(622, 592, "Yes")
    chart.route("normal_complete", "normal_join", (471, 527), (446, 527), (446, 692), arrow=False)
    chart.label(447, 512, "No")
    chart.route("hard", "normal_join", (598, 658), (598, 692), (446, 692), arrow=False)
    chart.junctions.append((446, 692))
    chart.route("normal_join", "result_join", (446, 692), (384, 692), arrow=False)

    chart.junctions.append((384, 692))
    chart.route("result_join", "results", (384, 692), (384, 714))
    chart.route("results", "choice", (384, 794), (384, 815))
    chart.route("choice", "B", (288, 859), (220, 859))
    chart.label(252, 843, "Replay")
    chart.route("choice", "D", (480, 859), (548, 859))
    chart.label(508, 843, "Continue")
    return chart


def continue_or_complete():
    chart = Chart(5, "Continue or Complete an Episode", "05-continue-and-complete-episodes.png", 821)
    chart.node("D", "connector", 224, 99, 182, 58, "D · From Part 4", "Continue")
    chart.node("episode_complete", "decision", 181, 182, 268, 112,
               "Required episode\nlevels complete?")
    chart.node("next_level", "process", 523, 327, 219, 76, "Find the next\navailable level",
               "In order within this episode")
    chart.node("B", "connector", 539.5, 429, 186, 59, "B · To Part 3", "Begin the next level")
    chart.node("summary", "io", 125, 327, 380, 75, "Show Landform Description Screen",
               "Short summary of the completed landform")
    chart.node("all_complete", "decision", 181, 424, 268, 108, "All four episodes\ncomplete?")
    chart.node("finish_screen", "io", 20, 561, 262, 99, "Show Completion Screen",
               "Total gameplay stars", "Collected rocks and minerals", "Congratulatory message")
    chart.node("end", "terminal", 38, 687, 226, 52, "End of playthrough")
    chart.node("unlock", "process", 367, 560, 282, 57, "Unlock the next episode")
    chart.node("save", "process", 344, 643, 328, 60, "Auto-save unlocked episodes",
               "Store progress on this device")
    chart.node("A", "connector", 416, 729, 184, 60, "A · To Part 2", "Landform Map")

    chart.route("D", "episode_complete", (315, 157), (315, 182))
    chart.route("episode_complete", "next_level", (449, 238), (632.5, 238), (632.5, 327))
    chart.label(535, 223, "No")
    chart.route("next_level", "B", (632.5, 403), (632.5, 429))
    chart.route("episode_complete", "summary", (315, 294), (315, 327))
    chart.label(338, 310, "Yes")
    chart.route("summary", "all_complete", (315, 402), (315, 424))
    chart.route("all_complete", "finish_screen", (181, 478), (151, 478), (151, 561))
    chart.label(165, 463, "Yes")
    chart.route("finish_screen", "end", (151, 660), (151, 687))
    chart.route("all_complete", "unlock", (449, 478), (508, 478), (508, 560))
    chart.label(478, 463, "No")
    chart.route("unlock", "save", (508, 617), (508, 643))
    chart.route("save", "A", (508, 703), (508, 729))
    return chart


def main():
    delivery, preview = map(Path, sys.argv[1:])
    delivery.mkdir(parents=True, exist_ok=True)
    preview.mkdir(parents=True, exist_ok=True)
    charts = (startup(), selection(), gameplay(), score_and_unlock(), continue_or_complete())
    print(json.dumps([chart.draw(delivery, preview) for chart in charts], indent=2))


if __name__ == "__main__":
    main()

