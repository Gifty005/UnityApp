# ============================================================
# UNITY APP - home.py
# Part 2 of 6 | Written by: [Kukoyi Adedamola] | Matric: [25120113031]
# Responsibilities: Home Screen
# ============================================================

import tkinter as tk

BG       = "#1A0030"
PURPLE   = "#4B0082"
YELLOW   = "#FFD700"
WHITE    = "#FFFFFF"
GRAY     = "#CCCCCC"
LIGHT_BG = "#2D004F"
BTN_DARK = "#3A006F"

FONT_XL   = ("Arial", 20, "bold")
FONT_LG   = ("Arial", 14, "bold")
FONT_MD   = ("Arial", 11)
FONT_SM   = ("Arial", 9)
FONT_BOLD = ("Arial", 11, "bold")


def _top_bar(parent, app, title=""):
    """Reusable top navigation bar."""
    bar = tk.Frame(parent, bg=LIGHT_BG, height=45)
    bar.pack(fill="x")
    bar.pack_propagate(False)

    if title:
        tk.Label(bar, text="←", bg=LIGHT_BG, fg=WHITE, font=FONT_LG,
                 cursor="hand2").pack(side="left", padx=10)

    # logo mark
    canvas = tk.Canvas(bar, width=32, height=32, bg=LIGHT_BG, highlightthickness=0)
    canvas.pack(side="right", padx=10, pady=6)
    canvas.create_oval(0, 4, 18, 22, fill="#E63950", outline="")
    canvas.create_oval(10, 0, 28, 18, fill="#3A86FF", outline="")
    canvas.create_oval(6, 14, 24, 32, fill="#2EC4B6", outline="")

    if title:
        tk.Label(bar, text=title, bg=LIGHT_BG, fg=WHITE,
                 font=FONT_LG).pack(side="left", padx=4)
    return bar


# ╔══════════════════════════════════════════════════════════╗
# ║                      HOME SCREEN                         ║
# ╚══════════════════════════════════════════════════════════╝
class HomeScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        _top_bar(self, self.app)

        # greeting
        name = self.app.current_user.get() or "User"
        tk.Label(self, text=f"Hello, {name}!", bg=BG, fg=WHITE,
                 font=FONT_XL, anchor="w").pack(padx=30, pady=(20, 16), fill="x")

        # two hub cards side by side
        row = tk.Frame(self, bg=BG)
        row.pack(padx=30, fill="x")

        self._hub_card(row,
                       icon="🛡️",
                       title="Aid Hub",
                       desc="Give or receive essential aid\nfor you and our community.",
                       btn="Enter Hub",
                       cmd=self.app.show_aid1)

        self._hub_card(row,
                       icon="📚",
                       title="Learn Hub",
                       desc="Explore Nigerian History,\nArts, and our heritage.",
                       btn="Enter Hub",
                       cmd=self.app.show_learn)

    def _hub_card(self, parent, icon, title, desc, btn, cmd):
        card = tk.Frame(parent, bg=PURPLE, width=340, height=230,
                        padx=20, pady=20)
        card.pack(side="left", padx=12, pady=8)
        card.pack_propagate(False)

        tk.Label(card, text=icon, bg=PURPLE, font=("Arial", 34)).pack(pady=(10, 6))
        tk.Label(card, text=title, bg=PURPLE, fg=WHITE,
                 font=FONT_LG).pack()
        tk.Label(card, text=desc, bg=PURPLE, fg=GRAY, font=FONT_SM,
                 justify="center").pack(pady=6)
        tk.Button(card, text=btn, bg=YELLOW, fg="#1A0030", font=FONT_BOLD,
                  relief="flat", width=16, pady=6, command=cmd).pack(pady=(8, 0))
