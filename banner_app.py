import streamlit as st
from streamlit_lottie import st_lottie

"""
Inline Lottie animation data – no external requests needed.
All animations are valid Lottie JSON with real keyframe motion.
"""

import math


def _ease(t):
    """cubic ease in-out bezier handles [0.42,0,0.58,1]"""
    return [0.42, 0, 0.58, 1]


# ─────────────────────────────────────────────────────────────────────────────
# LAPTOP animations  (5 distinct themes)
# ─────────────────────────────────────────────────────────────────────────────

def laptop_violet():
    """Laptop with pulsing violet screen glow"""
    return {
        "v": "5.7.4", "fr": 30, "ip": 0, "op": 120, "w": 200, "h": 180,
        "nm": "Laptop Violet", "ddd": 0, "assets": [],
        "layers": [
            # ── base plate ──────────────────────────────────────────────────
            {
                "ddd": 0, "ind": 1, "ty": 4, "nm": "base",
                "sr": 1, "ks": {
                    "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
                    "p": {"a": 0, "k": [100, 158, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "ao": 0,
                "shapes": [
                    {"ty": "rc", "nm": "r", "d": 1,
                     "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [160, 12]}, "r": {"a": 0, "k": 4}},
                    {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                     "c": {"a": 0, "k": [0.15, 0.12, 0.28, 1]}, "r": 1},
                    {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                     "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
                ],
                "ip": 0, "op": 120, "st": 0, "bm": 0
            },
            # ── hinge ───────────────────────────────────────────────────────
            {
                "ddd": 0, "ind": 2, "ty": 4, "nm": "hinge",
                "sr": 1, "ks": {
                    "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
                    "p": {"a": 0, "k": [100, 150, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "ao": 0,
                "shapes": [
                    {"ty": "rc", "nm": "r", "d": 1,
                     "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [140, 6]}, "r": {"a": 0, "k": 2}},
                    {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                     "c": {"a": 0, "k": [0.22, 0.18, 0.38, 1]}, "r": 1},
                    {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                     "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
                ],
                "ip": 0, "op": 120, "st": 0, "bm": 0
            },
            # ── screen body ─────────────────────────────────────────────────
            {
                "ddd": 0, "ind": 3, "ty": 4, "nm": "screen_body",
                "sr": 1, "ks": {
                    "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
                    "p": {"a": 0, "k": [100, 80, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {"a": 0, "k": [100, 100, 100]}
                },
                "ao": 0,
                "shapes": [
                    {"ty": "rc", "nm": "r", "d": 1,
                     "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [140, 98]}, "r": {"a": 0, "k": 8}},
                    {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                     "c": {"a": 0, "k": [0.10, 0.08, 0.20, 1]}, "r": 1},
                    {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                     "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
                ],
                "ip": 0, "op": 120, "st": 0, "bm": 0
            },
            # ── screen glow (animated opacity pulse) ────────────────────────
            {
                "ddd": 0, "ind": 4, "ty": 4, "nm": "screen_glow",
                "sr": 1, "ks": {
                    "o": {
                        "a": 1,
                        "k": [
                            {"t": 0,  "s": [60],  "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                            {"t": 60, "s": [100], "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                            {"t": 120,"s": [60],  "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}}
                        ]
                    },
                    "r": {"a": 0, "k": 0},
                    "p": {"a": 0, "k": [100, 78, 0]},
                    "a": {"a": 0, "k": [0, 0, 0]},
                    "s": {
                        "a": 1,
                        "k": [
                            {"t": 0,  "s": [96, 96, 100],  "h": 0, "i": {"x": [0.42, 0.42, 0.42], "y": [0, 0, 0]}, "o": {"x": [0.58, 0.58, 0.58], "y": [1, 1, 1]}},
                            {"t": 60, "s": [100, 100, 100], "h": 0, "i": {"x": [0.42, 0.42, 0.42], "y": [0, 0, 0]}, "o": {"x": [0.58, 0.58, 0.58], "y": [1, 1, 1]}},
                            {"t": 120,"s": [96, 96, 100],  "h": 0, "i": {"x": [0.42, 0.42, 0.42], "y": [0, 0, 0]}, "o": {"x": [0.58, 0.58, 0.58], "y": [1, 1, 1]}}
                        ]
                    }
                },
                "ao": 0,
                "shapes": [
                    {"ty": "rc", "nm": "r", "d": 1,
                     "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [126, 82]}, "r": {"a": 0, "k": 5}},
                    {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                     "c": {"a": 0, "k": [0.35, 0.20, 0.80, 1]}, "r": 1},
                    {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                     "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
                ],
                "ip": 0, "op": 120, "st": 0, "bm": 0
            },
            # ── screen content bars ─────────────────────────────────────────
            *[
                {
                    "ddd": 0, "ind": 5 + i, "ty": 4, "nm": f"bar_{i}",
                    "sr": 1, "ks": {
                        "o": {
                            "a": 1,
                            "k": [
                                {"t": i * 8,      "s": [0],   "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                                {"t": i * 8 + 20, "s": [80],  "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                                {"t": 80,         "s": [80],  "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                                {"t": 100,        "s": [0],   "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                                {"t": 120,        "s": [0],   "h": 0}
                            ]
                        },
                        "r": {"a": 0, "k": 0},
                        "p": {"a": 0, "k": [88, 52 + i * 14, 0]},
                        "a": {"a": 0, "k": [0, 0, 0]},
                        "s": {"a": 0, "k": [100, 100, 100]}
                    },
                    "ao": 0,
                    "shapes": [
                        {"ty": "rc", "nm": "r", "d": 1,
                         "p": {"a": 0, "k": [0, 0]},
                         "s": {"a": 0, "k": [40 + i * 14, 5]}, "r": {"a": 0, "k": 3}},
                        {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                         "c": {"a": 0, "k": [0.8, 0.75, 1.0, 1]}, "r": 1},
                        {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                         "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
                    ],
                    "ip": 0, "op": 120, "st": 0, "bm": 0
                }
                for i in range(4)
            ]
        ]
    }


def laptop_cyan():
    """Laptop with cyan typing cursor animation"""
    base = laptop_violet()
    base["nm"] = "Laptop Cyan"
    # Recolour screen glow to cyan
    for layer in base["layers"]:
        if layer["nm"] == "screen_glow":
            layer["shapes"][1]["c"]["k"] = [0.0, 0.55, 0.85, 1]
        if layer["nm"].startswith("bar_"):
            layer["shapes"][1]["c"]["k"] = [0.7, 1.0, 1.0, 1]
    return base


def laptop_orange():
    """Laptop with warm orange screen"""
    base = laptop_violet()
    base["nm"] = "Laptop Orange"
    for layer in base["layers"]:
        if layer["nm"] == "screen_glow":
            layer["shapes"][1]["c"]["k"] = [0.90, 0.45, 0.05, 1]
        if layer["nm"].startswith("bar_"):
            layer["shapes"][1]["c"]["k"] = [1.0, 0.88, 0.60, 1]
        if layer["nm"] == "screen_body":
            layer["shapes"][1]["c"]["k"] = [0.15, 0.08, 0.02, 1]
    return base


def laptop_green():
    """Laptop with matrix-green screen"""
    base = laptop_violet()
    base["nm"] = "Laptop Green"
    for layer in base["layers"]:
        if layer["nm"] == "screen_glow":
            layer["shapes"][1]["c"]["k"] = [0.05, 0.70, 0.25, 1]
        if layer["nm"].startswith("bar_"):
            layer["shapes"][1]["c"]["k"] = [0.6, 1.0, 0.6, 1]
        if layer["nm"] == "screen_body":
            layer["shapes"][1]["c"]["k"] = [0.02, 0.10, 0.04, 1]
    return base


def laptop_pink():
    """Laptop with rose-pink screen"""
    base = laptop_violet()
    base["nm"] = "Laptop Pink"
    for layer in base["layers"]:
        if layer["nm"] == "screen_glow":
            layer["shapes"][1]["c"]["k"] = [0.85, 0.15, 0.45, 1]
        if layer["nm"].startswith("bar_"):
            layer["shapes"][1]["c"]["k"] = [1.0, 0.80, 0.90, 1]
        if layer["nm"] == "screen_body":
            layer["shapes"][1]["c"]["k"] = [0.14, 0.04, 0.09, 1]
    return base


# ─────────────────────────────────────────────────────────────────────────────
# SMARTWATCH animations  (5 distinct styles × 3 needed per variant)
# ─────────────────────────────────────────────────────────────────────────────

def _watch_base(face_color, hand_color, accent, nm="Watch", beat=False):
    """Generic watch with rotating hands + optional heartbeat ring"""
    layers = [
        # ── strap top ───────────────────────────────────────────────────────
        {
            "ddd": 0, "ind": 1, "ty": 4, "nm": "strap_t",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [50, 18, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "ao": 0,
            "shapes": [
                {"ty": "rc", "nm": "r", "d": 1,
                 "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [22, 20]}, "r": {"a": 0, "k": 4}},
                {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                 "c": {"a": 0, "k": face_color}, "r": 1},
                {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
            ],
            "ip": 0, "op": 120, "st": 0, "bm": 0
        },
        # ── strap bottom ────────────────────────────────────────────────────
        {
            "ddd": 0, "ind": 2, "ty": 4, "nm": "strap_b",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [50, 82, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "ao": 0,
            "shapes": [
                {"ty": "rc", "nm": "r", "d": 1,
                 "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [22, 20]}, "r": {"a": 0, "k": 4}},
                {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                 "c": {"a": 0, "k": face_color}, "r": 1},
                {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
            ],
            "ip": 0, "op": 120, "st": 0, "bm": 0
        },
        # ── watch case ──────────────────────────────────────────────────────
        {
            "ddd": 0, "ind": 3, "ty": 4, "nm": "case",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [50, 50, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "ao": 0,
            "shapes": [
                {"ty": "el", "nm": "e", "d": 1,
                 "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [54, 54]}},
                {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                 "c": {"a": 0, "k": face_color}, "r": 1},
                {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
            ],
            "ip": 0, "op": 120, "st": 0, "bm": 0
        },
        # ── dial face ───────────────────────────────────────────────────────
        {
            "ddd": 0, "ind": 4, "ty": 4, "nm": "dial",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [50, 50, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "ao": 0,
            "shapes": [
                {"ty": "el", "nm": "e", "d": 1,
                 "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [44, 44]}},
                {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                 "c": {"a": 0, "k": [0.05, 0.05, 0.10, 1]}, "r": 1},
                {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
            ],
            "ip": 0, "op": 120, "st": 0, "bm": 0
        },
        # ── hour hand (slow rotation) ────────────────────────────────────────
        {
            "ddd": 0, "ind": 5, "ty": 4, "nm": "hour_hand",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100},
                "r": {
                    "a": 1,
                    "k": [
                        {"t": 0,   "s": [0],   "h": 0, "i": {"x": [0], "y": [0]}, "o": {"x": [1], "y": [1]}},
                        {"t": 120, "s": [360], "h": 0}
                    ]
                },
                "p": {"a": 0, "k": [50, 50, 0]},
                "a": {"a": 0, "k": [0, 8, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "ao": 0,
            "shapes": [
                {"ty": "rc", "nm": "r", "d": 1,
                 "p": {"a": 0, "k": [0, -8]}, "s": {"a": 0, "k": [4, 16]}, "r": {"a": 0, "k": 2}},
                {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                 "c": {"a": 0, "k": hand_color}, "r": 1},
                {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
            ],
            "ip": 0, "op": 120, "st": 0, "bm": 0
        },
        # ── minute hand (faster rotation) ───────────────────────────────────
        {
            "ddd": 0, "ind": 6, "ty": 4, "nm": "minute_hand",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100},
                "r": {
                    "a": 1,
                    "k": [
                        {"t": 0,   "s": [0],    "h": 0, "i": {"x": [0], "y": [0]}, "o": {"x": [1], "y": [1]}},
                        {"t": 120, "s": [1080], "h": 0}
                    ]
                },
                "p": {"a": 0, "k": [50, 50, 0]},
                "a": {"a": 0, "k": [0, 10, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "ao": 0,
            "shapes": [
                {"ty": "rc", "nm": "r", "d": 1,
                 "p": {"a": 0, "k": [0, -10]}, "s": {"a": 0, "k": [3, 20]}, "r": {"a": 0, "k": 2}},
                {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                 "c": {"a": 0, "k": accent}, "r": 1},
                {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
            ],
            "ip": 0, "op": 120, "st": 0, "bm": 0
        },
        # ── center dot ──────────────────────────────────────────────────────
        {
            "ddd": 0, "ind": 7, "ty": 4, "nm": "center",
            "sr": 1, "ks": {
                "o": {"a": 0, "k": 100}, "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [50, 50, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {"a": 0, "k": [100, 100, 100]}
            },
            "ao": 0,
            "shapes": [
                {"ty": "el", "nm": "e", "d": 1,
                 "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [6, 6]}},
                {"ty": "fl", "nm": "f", "o": {"a": 0, "k": 100},
                 "c": {"a": 0, "k": accent}, "r": 1},
                {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
            ],
            "ip": 0, "op": 120, "st": 0, "bm": 0
        },
    ]

    if beat:
        # Pulsing ring around case
        layers.append({
            "ddd": 0, "ind": 8, "ty": 4, "nm": "beat_ring",
            "sr": 1, "ks": {
                "o": {
                    "a": 1,
                    "k": [
                        {"t": 0,  "s": [80], "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                        {"t": 15, "s": [0],  "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                        {"t": 30, "s": [80], "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                        {"t": 45, "s": [0],  "h": 0, "i": {"x": [0.42], "y": [0]}, "o": {"x": [0.58], "y": [1]}},
                        {"t": 120,"s": [0],  "h": 0}
                    ]
                },
                "r": {"a": 0, "k": 0},
                "p": {"a": 0, "k": [50, 50, 0]},
                "a": {"a": 0, "k": [0, 0, 0]},
                "s": {
                    "a": 1,
                    "k": [
                        {"t": 0,  "s": [100, 100, 100], "h": 0, "i": {"x": [0.42, 0.42, 0.42], "y": [0, 0, 0]}, "o": {"x": [0.58, 0.58, 0.58], "y": [1, 1, 1]}},
                        {"t": 15, "s": [140, 140, 100], "h": 0, "i": {"x": [0.42, 0.42, 0.42], "y": [0, 0, 0]}, "o": {"x": [0.58, 0.58, 0.58], "y": [1, 1, 1]}},
                        {"t": 30, "s": [100, 100, 100], "h": 0, "i": {"x": [0.42, 0.42, 0.42], "y": [0, 0, 0]}, "o": {"x": [0.58, 0.58, 0.58], "y": [1, 1, 1]}},
                        {"t": 45, "s": [140, 140, 100], "h": 0, "i": {"x": [0.42, 0.42, 0.42], "y": [0, 0, 0]}, "o": {"x": [0.58, 0.58, 0.58], "y": [1, 1, 1]}},
                        {"t": 120,"s": [100, 100, 100], "h": 0}
                    ]
                }
            },
            "ao": 0,
            "shapes": [
                {"ty": "el", "nm": "e", "d": 1,
                 "p": {"a": 0, "k": [0, 0]}, "s": {"a": 0, "k": [58, 58]}},
                {"ty": "st", "nm": "s", "o": {"a": 0, "k": 100},
                 "c": {"a": 0, "k": accent},
                 "w": {"a": 0, "k": 2}, "lc": 2, "lj": 2},
                {"ty": "tr", "p": {"a": 0, "k": [0, 0]}, "a": {"a": 0, "k": [0, 0]},
                 "s": {"a": 0, "k": [100, 100]}, "r": {"a": 0, "k": 0}, "o": {"a": 0, "k": 100}}
            ],
            "ip": 0, "op": 120, "st": 0, "bm": 0
        })

    return {
        "v": "5.7.4", "fr": 30, "ip": 0, "op": 120, "w": 100, "h": 100,
        "nm": nm, "ddd": 0, "assets": [], "layers": layers
    }


# ── 15 distinct watch styles ──────────────────────────────────────────────────
def watch_violet_pulse():
    return _watch_base([0.20, 0.12, 0.40, 1], [0.80, 0.70, 1.0, 1], [0.55, 0.30, 1.0, 1], "Watch Violet Pulse", beat=True)

def watch_cyan_sport():
    return _watch_base([0.05, 0.20, 0.35, 1], [0.50, 0.90, 1.0, 1], [0.0, 0.75, 1.0, 1], "Watch Cyan Sport", beat=False)

def watch_gold_luxury():
    return _watch_base([0.18, 0.14, 0.05, 1], [0.95, 0.80, 0.30, 1], [1.0, 0.85, 0.20, 1], "Watch Gold Luxury", beat=False)

def watch_rose_fitness():
    return _watch_base([0.30, 0.08, 0.16, 1], [1.0, 0.75, 0.85, 1], [0.95, 0.25, 0.55, 1], "Watch Rose Fitness", beat=True)

def watch_green_eco():
    return _watch_base([0.05, 0.18, 0.08, 1], [0.50, 1.0, 0.55, 1], [0.10, 0.85, 0.30, 1], "Watch Green Eco", beat=False)

def watch_orange_fire():
    return _watch_base([0.20, 0.08, 0.00, 1], [1.0, 0.75, 0.30, 1], [1.0, 0.45, 0.05, 1], "Watch Orange Fire", beat=True)

def watch_ice_minimal():
    return _watch_base([0.12, 0.18, 0.25, 1], [0.85, 0.95, 1.0, 1], [0.60, 0.85, 1.0, 1], "Watch Ice Minimal", beat=False)

def watch_red_alert():
    return _watch_base([0.22, 0.04, 0.04, 1], [1.0, 0.60, 0.60, 1], [0.90, 0.10, 0.10, 1], "Watch Red Alert", beat=True)

def watch_teal_zen():
    return _watch_base([0.04, 0.18, 0.18, 1], [0.50, 0.95, 0.90, 1], [0.10, 0.80, 0.75, 1], "Watch Teal Zen", beat=False)

def watch_amber_retro():
    return _watch_base([0.20, 0.14, 0.02, 1], [1.0, 0.88, 0.55, 1], [0.90, 0.65, 0.10, 1], "Watch Amber Retro", beat=False)

def watch_indigo_night():
    return _watch_base([0.08, 0.08, 0.22, 1], [0.70, 0.70, 1.0, 1], [0.35, 0.35, 0.90, 1], "Watch Indigo Night", beat=True)

def watch_lime_energy():
    return _watch_base([0.10, 0.18, 0.02, 1], [0.85, 1.0, 0.30, 1], [0.65, 0.90, 0.05, 1], "Watch Lime Energy", beat=True)

def watch_silver_pro():
    return _watch_base([0.18, 0.18, 0.20, 1], [0.90, 0.90, 0.92, 1], [0.70, 0.70, 0.75, 1], "Watch Silver Pro", beat=False)

def watch_coral_wellness():
    return _watch_base([0.22, 0.10, 0.08, 1], [1.0, 0.72, 0.55, 1], [0.95, 0.40, 0.25, 1], "Watch Coral Wellness", beat=True)

def watch_midnight_ultra():
    return _watch_base([0.06, 0.06, 0.10, 1], [0.55, 0.55, 0.65, 1], [0.40, 0.40, 0.55, 1], "Watch Midnight Ultra", beat=False)


# ─── Export map ──────────────────────────────────────────────────────────────
LAPTOP_LOTTIES = {
    "laptop_violet":  laptop_violet,
    "laptop_cyan":    laptop_cyan,
    "laptop_orange":  laptop_orange,
    "laptop_green":   laptop_green,
    "laptop_pink":    laptop_pink,
}

WATCH_LOTTIES = {
    "watch_violet_pulse":   watch_violet_pulse,
    "watch_cyan_sport":     watch_cyan_sport,
    "watch_gold_luxury":    watch_gold_luxury,
    "watch_rose_fitness":   watch_rose_fitness,
    "watch_green_eco":      watch_green_eco,
    "watch_orange_fire":    watch_orange_fire,
    "watch_ice_minimal":    watch_ice_minimal,
    "watch_red_alert":      watch_red_alert,
    "watch_teal_zen":       watch_teal_zen,
    "watch_amber_retro":    watch_amber_retro,
    "watch_indigo_night":   watch_indigo_night,
    "watch_lime_energy":    watch_lime_energy,
    "watch_silver_pro":     watch_silver_pro,
    "watch_coral_wellness": watch_coral_wellness,
    "watch_midnight_ultra": watch_midnight_ultra,
}


st.set_page_config(
    page_title="TechBanner Studio",
    page_icon="💻",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
    background: #07070f;
    color: #eeeef5;
}
[data-testid="stAppViewContainer"] { padding: 0 !important; }
[data-testid="block-container"] {
    padding: 0.5rem 0.75rem 3rem !important;
    max-width: 460px !important;
    margin: 0 auto;
}
div[data-testid="column"] { padding: 0 3px !important; }
footer, #MainMenu, header { display: none !important; }

.page-header { text-align: center; padding: 20px 0 6px; }
.page-title {
    font-family: 'Syne', sans-serif;
    font-size: 24px; font-weight: 800;
    background: linear-gradient(100deg, #a78bfa 0%, #60a5fa 50%, #34d399 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0;
}
.page-sub {
    font-size: 11px; letter-spacing: 1.5px;
    text-transform: uppercase; opacity: 0.4; margin: 3px 0 0;
}

.banner-wrap {
    border-radius: 24px; padding: 18px 16px 14px;
    margin-bottom: 6px; position: relative; overflow: hidden;
}
.banner-tag {
    font-family: 'Syne', sans-serif; font-size: 9px; font-weight: 700;
    letter-spacing: 2.5px; text-transform: uppercase; opacity: 0.55; margin-bottom: 3px;
}
.banner-title {
    font-family: 'Syne', sans-serif; font-size: 24px;
    font-weight: 800; line-height: 1.12; margin: 0 0 4px;
}
.banner-desc { font-size: 12px; opacity: 0.65; margin: 0 0 12px; font-style: italic; }
.pill {
    display: inline-block; font-family: 'Syne', sans-serif;
    font-size: 11px; font-weight: 700;
    padding: 6px 14px; border-radius: 30px; margin-top: 2px;
}
.divider { border: none; border-top: 1px solid rgba(255,255,255,0.06); margin: 10px 0 20px; }

.v1 { background: linear-gradient(140deg,#0d0820,#160c30,#0a0618);
      box-shadow: 0 6px 40px rgba(110,70,240,0.30); border: 1px solid rgba(120,80,255,0.22); }
.v1 .banner-title { color: #c8b8ff; }
.v1 .pill { background: linear-gradient(90deg,#6c3de8,#a78bfa); color: #fff; }

.v2 { background: linear-gradient(140deg,#140800,#251200,#110600);
      box-shadow: 0 6px 40px rgba(255,110,0,0.25); border: 1px solid rgba(255,130,30,0.22); }
.v2 .banner-title { color: #ffb860; }
.v2 .pill { background: linear-gradient(90deg,#e85a00,#ffb347); color: #fff; }

.v3 { background: linear-gradient(140deg,#040e1a,#071828,#030c16);
      box-shadow: 0 6px 40px rgba(0,180,255,0.22); border: 1px solid rgba(60,190,255,0.18); }
.v3 .banner-title { color: #7ee8fa; }
.v3 .pill { background: linear-gradient(90deg,#0060d0,#00d4ff); color: #fff; }

.v4 { background: linear-gradient(140deg,#041008,#071e0e,#030c06);
      box-shadow: 0 6px 40px rgba(20,210,80,0.20); border: 1px solid rgba(40,210,90,0.18); }
.v4 .banner-title { color: #6effa0; }
.v4 .pill { background: linear-gradient(90deg,#00a83a,#6effa0); color: #000; }

.v5 { background: linear-gradient(140deg,#140810,#220c18,#100608);
      box-shadow: 0 6px 40px rgba(220,50,120,0.25); border: 1px solid rgba(230,80,140,0.22); }
.v5 .banner-title { color: #ffaad4; }
.v5 .pill { background: linear-gradient(90deg,#d40f6a,#ff6fa8); color: #fff; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="page-header">
  <p class="page-title">TechBanner Studio</p>
  <p class="page-sub">5 animated banner variants · mobile optimised</p>
</div>
""", unsafe_allow_html=True)

BANNERS = [
    {
        "cls": "v1", "tag": "Collection · 01",
        "title": "Pro Work\nEssentials",
        "desc": "Power meets precision — built for makers",
        "pill": "Shop Now →",
        "laptop": laptop_violet,
        "watches": [watch_violet_pulse, watch_indigo_night, watch_midnight_ultra],
    },
    {
        "cls": "v2", "tag": "Hot Deals",
        "title": "Ignite Your\nProductivity",
        "desc": "Blazing-fast devices for creators & hustlers",
        "pill": "Explore Deals →",
        "laptop": laptop_orange,
        "watches": [watch_orange_fire, watch_amber_retro, watch_gold_luxury],
    },
    {
        "cls": "v3", "tag": "New Arrivals",
        "title": "Arctic Tech\nSeries",
        "desc": "Crystal-cool performance gear",
        "pill": "Discover →",
        "laptop": laptop_cyan,
        "watches": [watch_cyan_sport, watch_ice_minimal, watch_teal_zen],
    },
    {
        "cls": "v4", "tag": "Eco Edition",
        "title": "Sustainable\nSmarter Life",
        "desc": "Green tech. Zero compromise.",
        "pill": "Go Green →",
        "laptop": laptop_green,
        "watches": [watch_green_eco, watch_lime_energy, watch_silver_pro],
    },
    {
        "cls": "v5", "tag": "Limited Drop",
        "title": "Chrome Rose\nLuxury Set",
        "desc": "Premium devices, refined taste",
        "pill": "Claim Now →",
        "laptop": laptop_pink,
        "watches": [watch_rose_fitness, watch_coral_wellness, watch_red_alert],
    },
]

for b in BANNERS:
    st.markdown(f"""
    <div class="banner-wrap {b['cls']}">
      <div class="banner-tag">{b['tag']}</div>
      <div class="banner-title">{b['title'].replace(chr(10), '<br>')}</div>
      <div class="banner-desc">{b['desc']}</div>
      <span class="pill">{b['pill']}</span>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_w1, col_w2, col_w3 = st.columns([2.2, 1, 1, 1])
    with col_l:
        st_lottie(b["laptop"](), height=115, width=115, loop=True, quality="high", key=f"lp_{b['cls']}")
    with col_w1:
        st_lottie(b["watches"][0](), height=80, width=80, loop=True, quality="high", key=f"w1_{b['cls']}")
    with col_w2:
        st_lottie(b["watches"][1](), height=80, width=80, loop=True, quality="high", key=f"w2_{b['cls']}")
    with col_w3:
        st_lottie(b["watches"][2](), height=80, width=80, loop=True, quality="high", key=f"w3_{b['cls']}")

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
