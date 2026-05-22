# learn.py
# Written by: Chifumnaya Jasper Omefe | Matric: 25120113044

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


def _top_bar(parent, app, back_cmd=None, title=""):
    bar = tk.Frame(parent, bg=LIGHT_BG, height=45)
    bar.pack(fill="x")
    bar.pack_propagate(False)

    if back_cmd:
        tk.Label(bar, text="←", bg=LIGHT_BG, fg=WHITE, font=FONT_LG,
                 cursor="hand2").pack(side="left", padx=10)
        bar.winfo_children()[-1].bind("<Button-1>", lambda e: back_cmd())

    canvas = tk.Canvas(bar, width=32, height=32, bg=LIGHT_BG, highlightthickness=0)
    canvas.pack(side="right", padx=10, pady=6)
    canvas.create_oval(0, 4, 18, 22, fill="#E63950", outline="")
    canvas.create_oval(10, 0, 28, 18, fill="#3A86FF", outline="")
    canvas.create_oval(6, 14, 24, 32, fill="#2EC4B6", outline="")

    if title:
        tk.Label(bar, text=title, bg=LIGHT_BG, fg=WHITE,
                 font=FONT_LG).pack(side="left", padx=4)
    return bar


# LEARN DASHBOARD  
class LearnDashboard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        _top_bar(self, self.app, back_cmd=self.app.show_home)

        tk.Label(self, text="Unity Cards", bg=BG, fg=WHITE,
                 font=FONT_XL).pack(pady=(24, 20))

        row = tk.Frame(self, bg=BG)
        row.pack(padx=40, fill="x")

        # Select Topic card
        self._option_card(row,
                          title="Select Topic:",
                          desc="Choose from History,\nCulture, Geography, Tech",
                          btn="Select",
                          cmd=self.app.show_cards)

        # Take Quiz card
        self._option_card(row,
                          title="Take Quiz:",
                          desc="Create Task",
                          btn="Take Quiz",
                          cmd=self.app.show_quizboard)

    def _option_card(self, parent, title, desc, btn, cmd):
        card = tk.Frame(parent, bg=PURPLE, width=320, height=180, padx=20, pady=18)
        card.pack(side="left", padx=16, pady=8)
        card.pack_propagate(False)

        tk.Label(card, text=title, bg=PURPLE, fg=WHITE, font=FONT_LG).pack(anchor="w")
        tk.Label(card, text=desc, bg=PURPLE, fg=GRAY, font=FONT_SM,
                 justify="left").pack(anchor="w", pady=6)
        tk.Button(card, text=btn, bg=YELLOW, fg="#1A0030", font=FONT_BOLD,
                  relief="flat", width=14, pady=6, command=cmd).pack(anchor="w")


# CARDS SCREEN  (topic selector)
class CardsScreen(tk.Frame):
    def __init__(self, parent, app, topic="All"):
        super().__init__(parent, bg=BG)
        self.app   = app
        self.topic = topic
        self._build()

    def _build(self):
        _top_bar(self, self.app, back_cmd=self.app.show_learn, title="Unity Cards")

        # counter label placeholder
        tk.Label(self, text="0/10", bg=BG, fg=GRAY, font=FONT_SM).pack(anchor="e", padx=20)

        tk.Label(self, text="Topic: User choose", bg=BG, fg=YELLOW,
                 font=FONT_LG).pack(pady=(8, 20))

        # topic dropdown
        topics = ["All"] + self.app.data.get_topics("flashcards")
        self.topic_var = tk.StringVar(value=self.topic)

        sel_row = tk.Frame(self, bg=BG)
        sel_row.pack()
        tk.Label(sel_row, text="Select Topic:", bg=BG, fg=WHITE, font=FONT_MD).pack(side="left", padx=(0, 10))
        menu = tk.OptionMenu(sel_row, self.topic_var, *topics)
        menu.config(bg=PURPLE, fg=WHITE, font=FONT_MD, relief="flat",
                    activebackground=BTN_DARK, activeforeground=WHITE)
        menu["menu"].config(bg=PURPLE, fg=WHITE)
        menu.pack(side="left")

        tk.Button(self, text="Start Cards", bg=YELLOW, fg="#1A0030",
                  font=FONT_BOLD, relief="flat", width=18, pady=7,
                  command=self._start).pack(pady=20)

    def _start(self):
        selected = self.topic_var.get()
        cards    = self.app.data.get_flashcards(selected)
        if not cards:
            import tkinter.messagebox as mb
            mb.showinfo("Unity App", "No cards found for that topic.")
            return
        self.app.show_card_detail(cards, index=0)


# CARD DETAIL (individual card) 

class CardDetailScreen(tk.Frame):
    def __init__(self, parent, app, cards=None, index=0):
        super().__init__(parent, bg=BG)
        self.app   = app
        self.cards = cards or []
        self.index = index
        self._build()

    def _build(self):
        _top_bar(self, self.app, back_cmd=self.app.show_cards, title="Unity Cards")

        total = len(self.cards)
        card  = self.cards[self.index]

        # progress
        tk.Label(self, text=f"{self.index + 1}/{total}", bg=BG, fg=GRAY,
                 font=FONT_SM).pack(anchor="e", padx=20, pady=(4, 0))
        tk.Label(self, text=f"Topic: {card['Topic']}", bg=BG, fg=YELLOW,
                 font=FONT_LG).pack(pady=(6, 14))

        # card body
        card_frame = tk.Frame(self, bg=PURPLE, padx=30, pady=24, width=660, height=200)
        card_frame.pack(padx=80)
        card_frame.pack_propagate(False)

        tk.Label(card_frame, text=card["Historical Context"], bg=PURPLE, fg=WHITE,
                 font=FONT_MD, wraplength=580, justify="left").pack(anchor="w")

        tk.Label(self, text=card["Fact"], bg=BG, fg=YELLOW,
                 font=("Arial", 10, "italic"), wraplength=640,
                 justify="center").pack(pady=(10, 20))

        # nav buttons
        nav = tk.Frame(self, bg=BG)
        nav.pack()

        if self.index > 0:
            tk.Button(nav, text="←", bg=PURPLE, fg=WHITE, font=FONT_LG,
                      relief="flat", width=4, pady=5,
                      command=self._prev).pack(side="left", padx=10)

        if self.index < total - 1:
            tk.Button(nav, text="→", bg=PURPLE, fg=WHITE, font=FONT_LG,
                      relief="flat", width=4, pady=5,
                      command=self._next).pack(side="left", padx=10)
        else:
            tk.Button(nav, text="✓ Done", bg=YELLOW, fg="#1A0030", font=FONT_BOLD,
                      relief="flat", width=10, pady=5,
                      command=self._finish).pack(side="left", padx=10)

    def _prev(self):
        self.app.show_card_detail(self.cards, self.index - 1)

    def _next(self):
        self.app.show_card_detail(self.cards, self.index + 1)

    def _finish(self):
        self.app.show_completed(self.cards)


# DECK COMPLETED

class CompletedScreen(tk.Frame):
    def __init__(self, parent, app, cards=None):
        super().__init__(parent, bg=BG)
        self.app   = app
        self.cards = cards or []
        self._build()

    def _build(self):
        _top_bar(self, self.app)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center = tk.Frame(self, bg=BG)
        center.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(center, text="🎉", bg=BG, font=("Arial", 48)).pack()
        tk.Label(center, text="Deck Completed!", bg=BG, fg=WHITE,
                 font=FONT_XL).pack(pady=(8, 4))
        tk.Label(center, text="You have completed this deck of flash cards.", bg=BG,
                 fg=GRAY, font=FONT_MD).pack(pady=(0, 24))

        btn_row = tk.Frame(center, bg=BG)
        btn_row.pack()
        tk.Button(btn_row, text="Review Again", bg=YELLOW, fg="#1A0030",
                  font=FONT_BOLD, relief="flat", width=14, pady=7,
                  command=lambda: self.app.show_card_detail(self.cards, 0)).pack(side="left", padx=8)
        tk.Button(btn_row, text="Dashboard", bg=BTN_DARK, fg=WHITE,
                  font=FONT_BOLD, relief="flat", width=14, pady=7,
                  command=self.app.show_home).pack(side="left", padx=8)