"""Vector props, expressive poses and 19 looping scenes for the existing rig.

The original seven enum IDs and Mascot/Main/Default remain unchanged. New enum
values are appended in data/model.json; this module adds matching animations.
Artwork uses 500px artboard coordinates, authored back-to-front via N/shape.
IDs above 20000 are reserved here, independently of the front-art generator.
"""

from __future__ import annotations
from math import atan2, hypot, cos, sin, pi
import sys
import xml.etree.ElementTree as ET
from build_data import read
from wing_poses import WingPoses

INK = "FF06442B"
GREEN = "FF409449"
LIME = "FFA8D35B"
MINT = "FF64D2AA"
CREAM = "FFFFF4DE"
PINK = "FFF38B92"
RED = "FFF05966"
GOLD = "FFFFC644"
BROWN = "FF925022"
BLUE = "FF73CEE7"
WHITE = "FFFFFDF3"
_id = 20000
_api = None


def E(parent, tag, **attrs):
    global _id
    _id += 1
    attrs.setdefault("id", f"0:{_id}")
    return ET.SubElement(parent, tag, {k: str(v) for k, v in attrs.items()})


def front(parent, child):
    parent.remove(child)
    parent.insert(0, child)
    return child


def N(parent, name, **attrs):
    return front(parent, E(parent, "Node", name=name, **attrs))


def paint(s, fill=None, stroke=INK, width=3):
    if fill:
        E(E(s, "Fill"), "SolidColor", colorValue=fill)
    if stroke:
        E(
            E(s, "Stroke", thickness=width, cap="round", join="round"),
            "SolidColor",
            colorValue=stroke,
        )
    return s


def shape(parent, name, **attrs):
    return front(parent, E(parent, "Shape", name=name, **attrs))


def ellipse(parent, name, x, y, w, h, fill, stroke=None, width=3):
    s = shape(parent, name, x=x, y=y)
    E(s, "Ellipse", width=w, height=h)
    return paint(s, fill, stroke, width)


def rect(parent, name, x, y, w, h, fill, stroke=INK, radius=8, width=3):
    s = shape(parent, name, x=x, y=y)
    E(s, "Rectangle", width=w, height=h, cornerRadiusTL=radius)
    return paint(s, fill, stroke, width)


def path(parent, name, data, fill=None, stroke=INK, width=3):
    s = shape(parent, name)
    points, closed = _api.vertices(data)
    p = E(s, "PointsPath", isClosed=str(closed).lower())
    for xy, inc, out in points:
        xy, inc, out = [tuple(v / _api.SCALE for v in point) for point in (xy, inc, out)]
        dx, dy = inc[0] - xy[0], inc[1] - xy[1]
        ox, oy = out[0] - xy[0], out[1] - xy[1]
        E(
            p,
            "CubicDetachedVertex",
            x=xy[0],
            y=xy[1],
            inRotation=atan2(dy, dx),
            inDistance=hypot(dx, dy),
            outRotation=atan2(oy, ox),
            outDistance=hypot(ox, oy),
        )
    return paint(s, fill, stroke, width)


def line(parent, name, points, color=INK, width=3):
    return path(
        parent, name, "M " + " L ".join(f"{x} {y}" for x, y in points), stroke=color, width=width
    )


def star(parent, name, x, y, size=18, color=GOLD):
    s = shape(parent, name, x=x, y=y)
    E(s, "Star", width=size, height=size, points=4, innerRadius=0.27, cornerRadius=1)
    return paint(s, color, None)


def heart(parent, name, x, y, scale=1):
    g = N(parent, name, x=x, y=y, scaleX=scale, scaleY=scale)
    path(
        g,
        "Heart",
        "M 0 40 C -18 24 -54 4 -51 -19 C -48 -45 -16 -48 0 -25 C 16 -48 48 -45 51 -19 C 54 4 18 24 0 40 Z",
        RED,
        "FFAD3548",
        3,
    )
    ellipse(g, "HeartShine", -28, -23, 15, 8, "FFFFBEC0")
    return g


def drop(parent, name, x, y, size=1):
    g = N(parent, name, x=x, y=y, scaleX=size, scaleY=size)
    path(
        g,
        "Drop",
        "M 0 -16 C -4 -6 -13 2 -11 10 C -8 23 9 23 12 10 C 14 1 5 -7 0 -16 Z",
        BLUE,
        "FF2B99BC",
        2,
    )
    ellipse(g, "Shine", -4, 6, 4, 9, WHITE)
    return g


def leaf(parent, name, x, y, rotation=0, scale=1):
    g = N(parent, name, x=x, y=y, rotation=rotation, scaleX=scale, scaleY=scale)
    path(g, "Leaf", "M 0 20 C -27 8 -27 -17 -2 -33 C 24 -15 26 10 0 20 Z", LIME, INK, 2.5)
    path(g, "Vein", "M 0 18 C 3 0 0 -9 -2 -25", stroke=GREEN, width=2)
    return g


def coin(parent, x, y, scale=1):
    g = N(parent, "Coin", x=x, y=y, scaleX=scale, scaleY=scale)
    ellipse(g, "Rim", 0, 0, 30, 30, GOLD, "FFC06F17", 2.5)
    ellipse(g, "Inset", 0, 0, 21, 21, None, "FFF0A522", 2)
    leaf(g, "LeafStamp", 0, 1, -0.3, 0.22)
    return g


def held(parent, name, y=365):
    return N(parent, name, x=250, y=y)


def blush(g):
    ellipse(g, "BlushL", 148, 267, 29, 15, "BFF38B92")
    ellipse(g, "BlushR", 353, 267, 29, 15, "BFF38B92")


def worried_brows(g):
    # The cream patches replace the master's relaxed eyebrows.
    ellipse(g, "BrowCoverL", 181, 170, 44, 25, CREAM)
    ellipse(g, "BrowCoverR", 311, 170, 44, 25, CREAM)
    path(g, "BrowL", "M 165 173 C 176 172 189 165 194 157", stroke=GREEN, width=5)
    path(g, "BrowR", "M 298 157 C 303 165 316 172 329 173", stroke=GREEN, width=5)


def draw_scene(key, fg, face, back):
    """Return semantic nodes for animation; every prop remains editable vector."""
    wings = WingPoses(sys.modules[__name__], fg)
    refs = {"wings": wings}
    grip = wings.hold
    if key in {
        "love",
        "nutrition",
        "wallet",
        "saving",
        "checklist",
        "celebrate",
        "cheer",
        "meditate",
        "letter",
        "bedtime",
    }:
        blush(face)
    if key in {"sad", "worried"}:
        worried_brows(face)
        refs["dropL"] = drop(face, "TearL", 149, 272, 0.55)
        refs["dropR"] = drop(face, "TearR", 349, 272, 0.55)
    if key == "idea":
        g = N(face, "LightBulb", x=411, y=83)
        for i in range(7):
            a = (-190 + i * 34) * pi / 180
            line(g, "Ray", [(cos(a) * 35, sin(a) * 35), (cos(a) * 43, sin(a) * 43)], GOLD, 4)
        ellipse(g, "Bulb", 0, -4, 47, 51, "FFFFDF6A", "FFD19724", 3)
        rect(g, "Socket", 0, 25, 23, 18, "FF81AFAA", INK, 4)
        line(g, "SocketRib", [(-9, 24), (9, 24)], WHITE, 2)
        path(
            g,
            "Filament",
            "M -5 16 L -5 0 C -16 -11 -12 -17 -5 -9 C -1 -2 2 -2 7 -10 C 14 -16 18 -8 7 0 L 7 16",
            stroke="FFD08A1C",
            width=2,
        )
        ellipse(g, "BulbShine", -10, -14, 8, 14, WHITE)
        refs["accent"] = g
        wings.add(
            "ThinkingWing",
            "L",
            (244, 299),
            (201, 322),
            width=0.80,
            full_size=True,
            motion=lambda t, d: (0, -5 * (1 - cos(2 * pi * t / d)) / 2),
        )
    elif key == "love":
        g = held(fg, "LoveHug", 356)
        refs["heart"] = heart(g, "HeldHeart", 0, 0, 1.6)
        grip(g, 77, 12)
        for i, (x, y, s) in enumerate([(401, 133, 0.32), (432, 96, 0.25), (99, 130, 0.23)]):
            refs[f"float{i}"] = heart(face, f"FloatingHeart{i}", x, y, s)
        refs["prop"] = g
    elif key == "nutrition":
        g = held(fg, "SaladBowl", 377)
        for x, y, r in [
            (-65, -26, -0.5),
            (-36, -39, -0.2),
            (0, -32, 0),
            (35, -39, 0.3),
            (65, -24, 0.7),
        ]:
            leaf(g, "SaladLeaf", x, y, r, 0.75)
        for x, y in [(-43, -22), (22, -31), (48, -16), (-3, -15)]:
            ellipse(g, "Tomato", x, y, 27, 25, RED, "FFB74537", 2)
            star(g, "TomatoLeaf", x, y - 10, 13, GREEN)
        path(g, "Carrot", "M 19 -23 L 41 -12 L 20 20 Z", "FFFFA33B", BROWN, 2)
        path(
            g,
            "Bowl",
            "M -88 -9 L 88 -9 C 77 33 53 54 0 55 C -53 54 -78 33 -88 -9 Z",
            "FFD7EDEF",
            "FF3F7677",
            3.5,
        )
        path(
            g,
            "BowlLight",
            "M -75 0 L 69 0 C 60 25 33 36 -9 35 C -39 33 -62 18 -75 0 Z",
            WHITE,
            None,
        )
        grip(g, 82, 12)
        refs["prop"] = g
    elif key == "running":
        g = N(back, "SpeedLines")
        for x, y, w in [(55, 174, 33), (48, 197, 45), (53, 352, 39), (66, 375, 24)]:
            line(g, "Speed", [(x, y), (x + w, y)], "FF6FA980", 4)
        refs["speed"] = g
    elif key == "tired":
        path(face, "EyeBagL", "M 150 248 C 168 267 200 269 219 251", stroke="BBA08DAC", width=7)
        path(face, "EyeBagR", "M 283 251 C 304 269 333 264 345 248", stroke="BBA08DAC", width=7)
        g = N(face, "TiredDots", x=405, y=137)
        for x in (-15, 0, 15):
            ellipse(g, "Dot", x, 0, 6, 6, GREEN)
        refs["accent"] = g
    elif key == "worried":
        refs["sweat"] = drop(face, "Sweat", 375, 146, 0.8)
        for side, x, bx in [("L", 120, 139), ("R", 380, 361)]:
            wings.add(
                "WorriedWing" + side,
                side,
                (x, 275),
                (bx, 291),
                width=0.70,
                motion=lambda t, d: (0, -4 * (1 - cos(4 * pi * t / d)) / 2),
                cadence=30,
            )
    elif key == "pomodoro":
        path(face, "Headband", "M 110 216 C 74 67 419 66 390 216", stroke=INK, width=19)
        path(face, "BandLight", "M 110 216 C 74 67 419 66 390 216", stroke=LIME, width=11)
        for x in (106, 394):
            rect(face, "Headphone", x, 218, 31, 71, GREEN, INK, 13, 4)
            rect(face, "EarCushion", x, 218, 13, 54, "FF78C05F", None, 6)
        g = held(fg, "Laptop", 382)
        rect(g, "Screen", 0, -8, 179, 113, "FF91ABB2", "FF34565B", 9, 4)
        rect(g, "ScreenLight", 0, -10, 166, 98, "FFC5D4D6", None, 5)
        ellipse(g, "TomatoLogo", 0, -3, 47, 45, RED, "FFC03E38", 2.5)
        star(g, "TomatoLeaf", 0, -26, 29, GREEN)
        ellipse(g, "LogoShine", -11, -9, 7, 10, "FFFFBEC0")
        path(g, "Base", "M -100 49 L 100 49 L 92 65 L -92 65 Z", "FFDFE7E6", "FF34565B", 3)
        refs["led"] = ellipse(g, "PowerLight", 67, 40, 5, 5, MINT)
        # Keep the supplied pointed wing while its inner edge follows the laptop.
        for side, sign, beat in [("L", -1, 1), ("R", 1, -1)]:
            wings.add(
                "TypingWing" + side,
                side,
                (sign * 41, 22),
                (250 + sign * 121, 385),
                follow=g,
                style="hug",
                motion=lambda t, d, s=beat: (0, s * 3 * cos(2 * pi * t / 48)),
                cadence=24,
            )
    elif key == "bedtime":
        hat = N(face, "NightCap")
        path(
            hat,
            "Cap",
            "M 146 126 C 181 39 329 56 355 111 L 400 161 C 364 156 340 147 315 119 Z",
            "FF4A9CAE",
            INK,
            3.5,
        )
        path(
            hat,
            "Band",
            "M 143 124 C 206 101 271 101 323 116 L 318 136 C 255 124 203 125 150 144 Z",
            "FFACDDD8",
            INK,
            3,
        )
        for x, y in [(203, 89), (249, 81), (289, 97)]:
            star(hat, "HatStar", x, y, 15, "FFCDF1DB")
        ellipse(hat, "PomPom", 397, 159, 30, 30, "FFB5E5DF", INK, 3)
        wings.add(
            "YawningWing",
            "L",
            (235, 230),
            (201, 302),
            width=0.78,
            full_size=True,
            motion=lambda t, d: (0, -5 * (1 - cos(2 * pi * t / d)) / 2),
        )
        g = N(face, "BedtimeZ", x=409, y=206)
        line(g, "Z", [(-10, -12), (8, -12), (-10, 10), (9, 10)], "FF4A9CAE", 4)
        refs["accent"] = g
    elif key == "cheer":
        g = N(face, "CheerSparkles")
        for x, y, s in [(100, 119, 24), (397, 120, 24), (425, 165, 14), (77, 163, 14)]:
            star(g, "Sparkle", x, y, s, GOLD)
        refs["sparkles"] = g
    elif key in {"sad", "wallet"}:
        g = held(fg, "Wallet", 373)
        if key == "wallet":
            bills = N(g, "Bills")
            for x, y, r in [(-42, -51, -0.22), (-6, -58, 0.06), (31, -46, 0.25)]:
                bill = N(bills, "Banknote", x=x, y=y, rotation=r)
                rect(bill, "Paper", 0, 0, 37, 73, "FFAADE8B", INK, 3, 2.5)
                rect(bill, "Border", 0, 0, 26, 60, None, GREEN, 3, 1.5)
                ellipse(bill, "Seal", 0, 0, 17, 22, "FF72B965")
            refs["bills"] = bills
            coin(g, -20, -37, 0.9)
            coin(g, 39, -27, 1.1)
        rect(g, "WalletBody", 0, 8, 158, 104, "FFB5743E", BROWN, 17, 4)
        rect(g, "WalletEdge", 0, 8, 145, 91, None, "FFE5B36A", 12, 2)
        rect(g, "Clasp", 58, 7, 48, 30, "FFD19550", BROWN, 7, 3)
        ellipse(g, "Button", 49, 7, 8, 8, GOLD)
        if key == "sad":
            path(
                g, "Crack", "M -8 -45 L 8 -17 L -9 -1 L 12 17 L -3 36 L 7 61", stroke=CREAM, width=8
            )
            path(
                g,
                "CrackEdge",
                "M -15 -45 L 1 -17 L -16 -1 L 5 17 L -10 36 L 0 61",
                stroke=BROWN,
                width=3,
            )
            coin(fg, 363, 464, 0.85)
        grip(g, 76, 8)
        refs["prop"] = g
    elif key == "saving":
        g = held(fg, "PiggyBank", 372)
        for x in (-37, 39):
            rect(g, "PigFoot", x, 49, 22, 30, "FFF08D99", "FFA74A62", 6)
        path(g, "Tail", "M 65 1 C 93 -22 95 18 78 8", stroke="FFA74A62", width=4)
        ellipse(g, "Body", 0, 0, 145, 107, "FFF5A0AA", "FFA74A62", 3.5)
        path(g, "Ear", "M -29 -41 L -38 -68 C -19 -72 -10 -50 -13 -42 Z", "FFF5A0AA", "FFA74A62", 3)
        ellipse(g, "Snout", -59, 13, 49, 34, "FFF7B4B9", "FFA74A62", 3)
        for x in (-68, -52):
            ellipse(g, "Nostril", x, 13, 5, 9, "FFA74A62")
        ellipse(g, "Eye", -27, -9, 7, 9, INK)
        ellipse(g, "Cheek", -25, 7, 15, 10, PINK)
        line(g, "Slot", [(-10, -42), (17, -42)], "FF8D4653", 5)
        refs["coin"] = coin(g, 3, -91, 0.9)
        grip(g, 78, 12)
        refs["prop"] = g
    elif key == "checklist":
        g = held(fg, "Checklist", 369)
        rect(g, "Board", -15, 0, 122, 139, "FF629A98", INK, 9, 3.5)
        rect(g, "Paper", -15, 3, 107, 122, WHITE, None, 4)
        rect(g, "Clip", -15, -65, 47, 18, "FFB6D4D1", INK, 4, 2.5)
        ellipse(g, "ClipRing", -15, -77, 13, 13, None, INK, 3)
        for y in (-36, -6, 24):
            rect(g, "Box", -50, y, 12, 12, None, "FF91B9AD", 1, 2)
            line(g, "Task", [(-30, y), (21, y)], "FF8EAAA2", 3)
        line(g, "SmallCheck", [(-55, -38), (-51, -33), (-43, -42)], GREEN, 3)
        tick = N(g, "SuccessSeal", x=66, y=33)
        ellipse(tick, "Seal", 0, 0, 90, 90, "FF55B867", INK, 3.5)
        ellipse(tick, "Rim", 0, 0, 78, 78, None, "FFA4E393", 2)
        line(tick, "Check", [(-22, -1), (-5, 17), (26, -19)], WHITE, 8)
        refs["accent"] = tick
        grip(g, 80, 18)
        refs["prop"] = g
    elif key == "celebrate":
        g = N(fg, "Trophy", x=76, y=266)
        for x in (-29, 29):
            ellipse(g, "Handle", x, -16, 29, 41, None, "FFD78A1A", 8)
        rect(g, "Stem", 0, 28, 12, 37, GOLD, "FFD78A1A", 3, 2)
        rect(g, "Base", 0, 50, 62, 15, GOLD, "FFD78A1A", 5, 3)
        path(g, "Cup", "M -32 -43 L 32 -43 L 27 -9 C 25 18 -25 18 -27 -9 Z", GOLD, "FFD78A1A", 3.5)
        path(
            g, "CupShine", "M -20 -35 L -10 -35 L -8 4 C -21 -2 -20 -14 -20 -35 Z", "FFFFE598", None
        )
        star(g, "CupStar", 7, -18, 19, "FFFFF0B3")
        wings.add("TrophyWing", "L", (24, 36), (134, 319), follow=g, style="hug", full_size=True)
        # The cup faces the viewer; its bowl and rim must stay in front of the gripping wing.
        front(fg, g)
        refs["prop"] = g
        confetti = N(back, "Confetti")
        for i, (x, y) in enumerate(
            [
                (60, 115),
                (92, 61),
                (151, 45),
                (375, 58),
                (422, 98),
                (445, 169),
                (65, 269),
                (424, 315),
                (106, 394),
                (394, 413),
            ]
        ):
            p = N(confetti, f"Confetti{i}", x=x, y=y, rotation=(i % 3 - 1) * 0.5)
            rect(p, "Paper", 0, 0, 7, 18, [RED, GOLD, BLUE, LIME][i % 4], None, 2)
        refs["confetti"] = confetti
    elif key == "alarm":
        g = held(fg, "AlarmClock", 365)
        for x in (-49, 49):
            line(g, "Leg", [(x, 48), (x * 1.17, 68)], "FFC34B51", 7)
            bell = N(g, "Bell", x=x, y=-62, rotation=-0.5 if x < 0 else 0.5)
            ellipse(bell, "BellShell", 0, 0, 50, 29, RED, "FFA73547", 3)
        rect(g, "TopButton", 0, -72, 20, 10, "FFCF5260", INK, 3, 2)
        ellipse(g, "ClockCase", 0, 0, 142, 142, RED, "FFA73547", 4)
        ellipse(g, "ClockFace", 0, 0, 122, 122, WHITE, "FFC9545E", 3)
        for i in range(12):
            a = 2 * pi * i / 12
            line(g, "Tick", [(sin(a) * 48, -cos(a) * 48), (sin(a) * 54, -cos(a) * 54)], INK, 2.5)
        hand = N(g, "ClockHands")
        line(hand, "Hour", [(0, 0), (-17, -23)], INK, 5)
        line(hand, "Minute", [(0, 0), (5, -39)], INK, 3.5)
        ellipse(g, "Pin", 0, 0, 9, 9, RED)
        grip(g, 80, 15)
        refs["prop"] = g
    elif key == "workout":
        g = held(fg, "Dumbbells", 390)
        rect(g, "Bar", 0, 0, 289, 12, "FFC2CAC0", INK, 5, 3)
        for x in (-145, -124, 124, 145):
            rect(g, "Weight", x, 0, 21, 60 if abs(x) > 130 else 83, LIME, INK, 7, 3.5)
            rect(g, "WeightLight", x - 4, -3, 6, 44 if abs(x) > 130 else 63, "FFD4EC83", None, 2)
        for side, sign in [("L", -1), ("R", 1)]:
            wings.add(
                "LiftingWing" + side,
                side,
                (sign * 75, 8),
                (250 + sign * 104, 358),
                follow=g,
                style="hug",
            )
        refs["prop"] = g
        refs["sweat"] = drop(face, "WorkoutSweat", 361, 157, 0.65)
    elif key == "meditate":
        g = N(back, "BreathingHalo", x=250, y=274)
        ellipse(g, "OuterRing", 0, 0, 384, 339, "FFE1F0DC", "FF9CD2AD", 4)
        ellipse(g, "InnerRing", 0, 0, 358, 313, None, "FFC0E1C0", 2)
        refs["aura"] = g
        for side, x, bx in [("L", 92, 165), ("R", 408, 335)]:
            wings.add(
                "RestingWing" + side,
                side,
                (x, 406),
                (bx, 412),
                width=0.88,
                motion=lambda t, d: (0, -4 * (1 - cos(2 * pi * t / d)) / 2),
            )
    elif key == "letter":
        g = held(fg, "ThankYouLetter", 373)
        rect(g, "Envelope", 0, 0, 169, 110, "FFFFE5AB", "FFAD8141", 8, 3.5)
        path(g, "BottomFold", "M -78 46 L 0 -4 L 78 46", stroke="FFD5AC6B", width=2)
        path(g, "TopFold", "M -82 -51 L 0 15 L 82 -51", CREAM, "FFAD8141", 3)
        refs["heart"] = heart(g, "HeartSeal", 0, 11, 0.36)
        grip(g, 81, 4)
        refs["prop"] = g
    elif key == "energized":
        g = N(back, "LeafAura", x=250, y=285)
        path(
            g,
            "Aura",
            "M -91 142 C -196 105 -203 -30 -149 -90 C -151 -56 -124 -44 -127 -19 C -172 -113 -65 -174 -53 -238 C -18 -194 -30 -166 -3 -147 C 30 -166 19 -209 48 -245 C 60 -190 138 -173 139 -111 C 166 -128 165 -147 166 -161 C 216 -62 202 62 115 132 Z",
            "FFD7EFA7",
            "FF94CB55",
            3,
        )
        refs["aura"] = g
        stars = N(face, "EnergyStars")
        for x, y, s in [(89, 154, 24), (402, 158, 22), (423, 236, 14), (81, 232, 13)]:
            star(stars, "EnergyStar", x, y, s, "FFC8F386")
        refs["sparkles"] = stars
    return refs


def keys(animation, target, prop, values, discrete=False):
    oid = target if isinstance(target, str) else target.get("id")
    obj = next((o for o in animation.findall("KeyedObject") if o.get("objectId") == oid), None)
    if obj is None:
        obj = E(animation, "KeyedObject", objectId=oid)
    old = obj.find(f"KeyedProperty[@propertyKey='{prop}']")
    if old is not None:
        obj.remove(old)
    p = E(obj, "KeyedProperty", propertyKey=prop)
    for i, (frame, value) in enumerate(values):
        k = E(p, "KeyFrameId" if discrete else "KeyFrameDouble", frame=frame, value=value)
        if not discrete and len(values) > 1 and i < len(values) - 1:
            k.set("interpolationType", "cubic")
            E(k, "CubicEaseInterpolator", x1=0.42, y1=0, x2=0.58, y2=1)


def fixed(animation, target, prop, value, discrete=False):
    keys(animation, target, prop, [(0, value)], discrete)


def pulse(animation, node, prop, a, b, duration):
    keys(animation, node, prop, [(0, a), (duration // 2, b), (duration, a)])


def animate_scene(animation, spec, refs):
    key, d = spec["key"], spec["frames"]
    fixed(animation, "0:10", 13, 250)
    # Match the seven original moods: scene props need to fit around Ollie,
    # without shrinking the character (including the thinking mood).
    fixed(animation, "0:10", 16, 1)
    fixed(animation, "0:10", 17, 1)
    pulse(animation, "0:10", 14, 478, 474, d)
    fixed(animation, "0:10", 15, 0)
    pulse(animation, "0:11", 15, -0.025, 0.025, d)
    fixed(animation, "0:11", 14, -186)
    fixed(animation, "0:16", 17, 1)
    replaced = {pose["side"] for pose in refs["wings"].wings}
    for side, oid in [("L", "0:20"), ("R", "0:21")]:
        fixed(animation, oid, 18, 0 if side in replaced else 1)
        fixed(animation, oid, 15, 0)
    for oid, x in [("0:1427", -34), ("0:1447", 38)]:
        fixed(animation, oid, 13, x)
        fixed(animation, oid, 14, -30)
        fixed(animation, oid, 15, 0)
    face = {
        "love": "0:32",
        "nutrition": "0:33",
        "tired": "0:36",
        "worried": "0:35",
        "bedtime": "0:38",
        "cheer": "0:32",
        "sad": "0:36",
        "checklist": "0:33",
        "celebrate": "0:32",
        "meditate": "0:38",
        "letter": "0:38",
    }.get(key, "0:31")
    fixed(animation, "0:17", 296, face, True)
    fixed(
        animation,
        "0:18",
        296,
        "0:44" if key in {"idea", "tired", "bedtime", "sad", "meditate", "letter"} else "0:42",
        True,
    )
    fixed(animation, "0:19", 296, "0:51", True)
    if face == "0:31" and d >= 144:
        t = int(d * 0.73)
        keys(animation, "0:16", 17, [(0, 1), (t, 1), (t + 5, 0.1), (t + 11, 1), (d, 1)])
    if "prop" in refs:
        p = refs["prop"]
        y = float(p.get("y", 0))
        # A carried object has a readable lift, short hold and controlled
        # descent. The wing vertices sample these same keys, so the contact
        # point does not slide while the object travels.
        lift = {
            "love": 11,
            "nutrition": 18,
            "sad": 4,
            "wallet": 13,
            "saving": 8,
            "checklist": 10,
            "alarm": 6,
            "letter": 12,
            "pomodoro": 3,
        }.get(key, 7)
        keys(
            animation,
            p,
            14,
            [
                (0, y),
                (round(d * 0.28), y - lift * 0.85),
                (round(d * 0.42), y - lift),
                (round(d * 0.62), y - lift),
                (round(d * 0.78), y - lift * 0.35),
                (d, y),
            ],
        )
        sway = 0.008 if key == "pomodoro" else 0.025
        pulse(animation, p, 15, -sway, sway, d)
    if "accent" in refs:
        p = refs["accent"]
        pulse(animation, p, 16, 0.95, 1.06, d)
        pulse(animation, p, 17, 0.95, 1.06, d)
    if "heart" in refs:
        p = refs["heart"]
        s = float(p.get("scaleX", 1))
        pulse(animation, p, 16, s, s * 1.06, d)
        pulse(animation, p, 17, s, s * 1.06, d)
    for name, p in refs.items():
        if name.startswith("float"):
            y = float(p.get("y", 0))
            pulse(animation, p, 14, y, y - 15, d)
            pulse(animation, p, 18, 0.55, 1, d)
        if name.startswith("drop") or name == "sweat":
            y = float(p.get("y", 0))
            keys(animation, p, 14, [(0, y), (int(d * 0.8), y + 16), (d, y)])
            keys(animation, p, 18, [(0, 0.25), (int(d * 0.3), 1), (int(d * 0.8), 0), (d, 0.25)])
    if "sparkles" in refs:
        pulse(animation, refs["sparkles"], 18, 0.4, 1, d)
    if "aura" in refs:
        for prop in (16, 17):
            pulse(animation, refs["aura"], prop, 0.92, 1.06, d)
    if key == "idea":
        pulse(animation, "0:11", 15, -0.07, 0.015, d)
        pulse(animation, refs["accent"], 18, 0.5, 1, d)
    elif key == "running":
        fixed(animation, "0:10", 15, 0.045)
        fixed(animation, "0:11", 15, -0.04)
        keys(animation, "0:10", 14, [(0, 475), (12, 471), (24, 475), (36, 471), (48, 475)])
        for oid, sign in [("0:20", 1), ("0:21", -1)]:
            pulse(animation, oid, 15, -0.5 * sign, 0.65 * sign, d)
        for oid, sign in [("0:1427", 1), ("0:1447", -1)]:
            pulse(animation, oid, 15, -0.32 * sign, 0.32 * sign, d)
            pulse(animation, oid, 14, -34, -48 if sign == 1 else -26, d)
        pulse(animation, refs["speed"], 13, 8, -9, d)
        pulse(animation, refs["speed"], 18, 0.4, 1, d)
    elif key == "tired":
        pulse(animation, "0:11", 14, -173, -167, d)
        pulse(animation, "0:11", 15, 0.04, 0.10, d)
        fixed(animation, "0:20", 15, -0.10)
        fixed(animation, "0:21", 15, 0.1)
    elif key == "worried":
        keys(
            animation,
            "0:11",
            15,
            [(0, -0.035), (30, 0.035), (60, -0.035), (90, 0.035), (120, -0.035)],
        )
    elif key == "pomodoro":
        pulse(animation, refs["led"], 18, 0.35, 1, d)
        pulse(animation, "0:11", 15, -0.015, 0.025, d)
    elif key == "bedtime":
        pulse(animation, "0:11", 15, 0, 0.075, d)
        pulse(animation, refs["accent"], 14, 206, 191, d)
    elif key == "cheer":
        pulse(animation, "0:10", 14, 478, 474, d)
        pulse(animation, "0:20", 15, 1.03, 1.37, d)
        pulse(animation, "0:21", 15, -1.03, -1.37, d)
    elif key == "sad":
        pulse(animation, "0:11", 15, -0.04, 0.05, d)
        pulse(animation, "0:11", 14, -179, -174, d)
    elif key == "wallet":
        pulse(animation, refs["bills"], 14, 3, -8, d)
    elif key == "saving":
        keys(
            animation,
            refs["coin"],
            14,
            [(0, -91), (35, -91), (95, -39), (135, -39), (160, -91), (180, -91)],
        )
        keys(animation, refs["coin"], 18, [(0, 1), (70, 1), (100, 0), (145, 0), (160, 1), (180, 1)])
    elif key == "checklist":
        for prop in (16, 17):
            keys(
                animation,
                refs["accent"],
                prop,
                [(0, 0.92), (35, 1.12), (60, 1), (120, 1), (d, 0.92)],
            )
    elif key == "celebrate":
        pulse(animation, "0:10", 14, 478, 474, d)
        fixed(animation, "0:21", 18, 1)
        pulse(animation, "0:21", 15, -1.1, -1.4, d)
        pulse(animation, refs["prop"], 14, 266, 248, d)
        keys(animation, refs["confetti"], 14, [(0, -10), (100, 23), (120, -10)])
        keys(animation, refs["confetti"], 18, [(0, 0.4), (24, 1), (100, 0), (120, 0.4)])
    elif key == "alarm":
        keys(
            animation,
            refs["prop"],
            15,
            [(0, 0), (8, -0.07), (16, 0.07), (24, -0.07), (32, 0.07), (44, 0), (d, 0)],
        )
    elif key == "workout":
        keys(animation, refs["prop"], 14, [(0, 390), (50, 360), (80, 360), (130, 390), (d, 390)])
    elif key == "meditate":
        pulse(animation, "0:10", 14, 474, 470, d)
        fixed(animation, "0:11", 15, 0)
        fixed(animation, "0:1427", 13, -23)
        fixed(animation, "0:1447", 13, 25)
        fixed(animation, "0:1427", 15, -0.30)
        fixed(animation, "0:1447", 15, 0.30)
    elif key == "letter":
        pulse(animation, "0:11", 15, -0.045, 0.015, d)
    elif key == "energized":
        pulse(animation, "0:20", 15, 0.05, 0.25, d)
        pulse(animation, "0:21", 15, -0.05, -0.25, d)
        pulse(animation, "0:10", 14, 478, 474, d)
    refs["wings"].animate(animation)


def extend_runtime(artboard, api):
    global _api, _id
    _api, _id = api, 20000
    specs = read("data/expressions.json")["expressions"]
    model = read("data/model.json")
    values = {v["key"]: v["id"] for v in model["enums"][0]["values"]}
    character = artboard.find("Node[@id='0:10']")
    face = next(e for e in character.iter("Node") if e.get("id") == "0:15")
    slots = []
    for parent, name, x, y, at_front in [
        (character, "SceneProps", -250, -478, True),
        (face, "SceneFace", -250, -292, True),
        (character, "SceneBackdrop", -250, -478, False),
    ]:
        slot = E(parent, "Solo", name=name, x=x, y=y)
        if at_front:
            front(parent, slot)
        empty = E(slot, "Node", name=name + "None")
        slot.set("activeComponentId", empty.get("id"))
        slots.append((slot, empty))
    mouths = next(e for e in face.iter("Solo") if e.get("id") == "0:18")
    concerned = N(mouths, "MouthConcerned")
    path(
        concerned,
        "Beak",
        "M -19 0 C -13 -21 -3 -26 10 -14 L 20 -1 C 17 13 8 20 0 21 C -8 20 -15 10 -19 0 Z",
        GOLD,
        "FFB96A14",
        2.5,
    )
    ellipse(concerned, "Gasp", 0, 5, 14, 20, "FF8B4525")
    # Every legacy pose actively clears the new layers and restores moved joints.
    for animation in artboard.findall("LinearAnimation"):
        if not (
            animation.get("name", "").startswith("mood_")
            or animation.get("name") in {"sleep_loop", "wake_startle", "hello_wave"}
        ):
            continue
        for slot, empty in slots:
            fixed(animation, slot, 296, empty.get("id"), True)
        for oid in ("0:20", "0:21"):
            fixed(animation, oid, 18, 1)
        fixed(animation, "0:10", 13, 250)
        fixed(animation, "0:10", 16, 1)
        fixed(animation, "0:10", 15, 0)
        for oid, x in [("0:1427", -34), ("0:1447", 38)]:
            fixed(animation, oid, 13, x)
            fixed(animation, oid, 14, -30)
            fixed(animation, oid, 15, 0)
    machine = artboard.find("StateMachine")
    layer = machine.find("StateMachineLayer[@name='Mood']")
    any_state = layer.find("AnyState")
    for i, spec in enumerate(specs):
        key = spec["key"]
        groups = [N(slot, key.title()) for slot, empty in slots]
        refs = draw_scene(key, *groups)
        animation = E(
            artboard,
            "LinearAnimation",
            name="mood_" + key,
            duration=spec["frames"],
            fps=60,
            loopValue="loop",
        )
        animate_scene(animation, spec, refs)
        if key == "worried":
            fixed(animation, "0:18", 296, concerned.get("id"), True)
        if key == "energized":
            # Stars follow the pupils, inside the cream face overlay.
            eyes = N(groups[1], "StarryEyes")
            star(eyes, "LeftEyeStar", 190, 222, 25, WHITE)
            star(eyes, "RightEyeStar", 311, 222, 25, WHITE)
            pulse(animation, eyes, 18, 0.65, 1, spec["frames"])
        for (slot, _), group in zip(slots, groups):
            fixed(animation, slot, 296, group.get("id"), True)
        state = E(
            layer,
            "AnimationState",
            animationId=animation.get("id"),
            x=(i % 4) * 200,
            y=400 + (i // 4) * 200,
        )
        transition = E(any_state, "StateTransition", stateToId=state.get("id"), duration=220)
        condition = E(transition, "TransitionViewModelCondition", opValue="equal")
        comparator = E(condition, "TransitionPropertyViewModelComparator")
        binding = E(comparator, "BindablePropertyEnum")
        E(binding, "DataBindContext", sourcePathIds="0:610-0:611", propertyKey=637)
        E(condition, "TransitionValueEnumComparator", value=values[key])
