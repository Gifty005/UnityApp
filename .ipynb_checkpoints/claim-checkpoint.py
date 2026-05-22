# ============================================================
# UNITY APP - claim.py
# Part 6 of 6 | Written by: [Gregory okon] | Matric: [25120113042]
# Responsibilities: Claim Resources screen, Item Claimed screen
# ============================================================

import tkinter as tk
from tkinter import messagebox

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
        lbl = tk.Label(bar, text="←", bg=LIGHT_BG, fg=WHITE,
                       font=FONT_LG, cursor="hand2")
        lbl.pack(side="left", padx=10)
        lbl.bind("<Button-1>", lambda e: back_cmd())

    canvas = tk.Canvas(bar, width=32, height=32, bg=LIGHT_BG,
                       highlightthickness=0)
    canvas.pack(side="right", padx=10, pady=6)
    canvas.create_oval(0, 4, 18, 22, fill="#E63950", outline="")
    canvas.create_oval(10, 0, 28, 18, fill="#3A86FF", outline="")
    canvas.create_oval(6, 14, 24, 32, fill="#2EC4B6", outline="")

    if title:
        tk.Label(bar, text=title, bg=LIGHT_BG, fg=WHITE,
                 font=FONT_LG).pack(side="left", padx=4)


class ClaimScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app       = app
        self.resources = app.data.get_resources()
        self.checks    = []
        self._build()

    def _build(self):
        # top bar — pack()
        _top_bar(self, self.app, back_cmd=self.app.show_aid1)

        # page title
        tk.Label(self, text="Claim Resources", bg=BG, fg=WHITE,
                 font=FONT_LG).pack(pady=(10, 4))

        # ── search bar ────────────────────────────────────────
        search_row = tk.Frame(self, bg=BG)
        search_row.pack(fill="x", padx=20, pady=(4, 4))
        tk.Label(search_row, text="🔍", bg=BG, fg=GRAY,
                 font=FONT_MD).pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self._filter)
        tk.Entry(search_row, textvariable=self.search_var,
                 bg=LIGHT_BG, fg=WHITE, insertbackground=WHITE,
                 relief="flat", font=FONT_MD).pack(
                 side="left", padx=6, ipady=5, fill="x", expand=True)

        # ── table header ──────────────────────────────────────
        hdr = tk.Frame(self, bg=PURPLE)
        hdr.pack(fill="x", padx=20, pady=(4, 0))
        for col, w in [("Description", 22), ("Qty", 6),
                       ("Select", 6), ("Location", 14)]:
            tk.Label(hdr, text=col, bg=PURPLE, fg=YELLOW,
                     font=FONT_BOLD, width=w,
                     anchor="w").pack(side="left", padx=6, pady=4)

        # ── rows container ────────────────────────────────────
        self.table_frame = tk.Frame(self, bg=BG)
        self.table_frame.pack(fill="both", expand=True,
                              padx=20, pady=4)
        self._populate_rows(self.resources)

        # ── claim button ──────────────────────────────────────
        tk.Button(self, text="Claim Items", bg=YELLOW,
                  fg="#1A0030", font=FONT_BOLD, relief="flat",
                  width=18, pady=7,
                  command=self._claim).pack(pady=10)

    def _populate_rows(self, resources):
        # clear old rows
        for w in self.table_frame.winfo_children():
            w.destroy()
        self.checks = []

        if not resources:
            tk.Label(self.table_frame,
                     text="No resources available at this time.",
                     bg=BG, fg=GRAY, font=FONT_MD).pack(pady=20)
            return

        for res in resources:
            bv  = tk.BooleanVar(value=False)
            qv  = tk.StringVar(value="1")

            row = tk.Frame(self.table_frame, bg=LIGHT_BG)
            row.pack(fill="x", pady=2)

            tk.Label(row, text=res["item"], bg=LIGHT_BG, fg=WHITE,
                     font=FONT_MD, width=22,
                     anchor="w").pack(side="left", padx=6, pady=5)
            tk.Label(row, text=res["quantity"], bg=LIGHT_BG,
                     fg=WHITE, font=FONT_MD,
                     width=6).pack(side="left")
            tk.Checkbutton(row, variable=bv, bg=LIGHT_BG,
                           activebackground=LIGHT_BG,
                           selectcolor=PURPLE).pack(side="left",
                                                    padx=10)
            tk.Entry(row, textvariable=qv, bg=BG, fg=WHITE,
                     insertbackground=WHITE, relief="flat",
                     font=FONT_MD, width=4).pack(side="left",
                                                 padx=4)
            tk.Label(row, text=res["location"], bg=LIGHT_BG,
                     fg=GRAY, font=FONT_SM,
                     width=14).pack(side="left", padx=10)

            self.checks.append((bv, qv, res))

    def _filter(self, *_):
        term     = self.search_var.get().lower()
        filtered = [r for r in self.resources
                    if term in r["item"].lower()]
        self._populate_rows(filtered)

    def _claim(self):
        selected = []
        for bv, qv, res in self.checks:
            if bv.get():
                try:
                    qty = int(qv.get())
                except ValueError:
                    qty = 1
                if qty > int(res["quantity"]):
                    messagebox.showwarning(
                        "Unity App",
                        f"Only {res['quantity']} unit(s) of "
                        f"'{res['item']}' available.")
                    return
                selected.append(
                    {"item": res["item"].strip(), "qty": qty})

        if not selected:
            messagebox.showinfo(
                "Unity App",
                "Please tick at least one item to claim.")
            return

        self.app.data.claim_resources(selected)
        self.app.show_item_claimed()


class ItemClaimedScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # top bar — pack()
        _top_bar(self, self.app)

        # ── centre content using pack() NOT place() ───────────
        center = tk.Frame(self, bg=BG)
        center.pack(expand=True, pady=60)   # ← fixed: was place()

        tk.Label(center, text="✅", bg=BG,
                 font=("Arial", 52)).pack()
        tk.Label(center, text="Items reserved!", bg=BG, fg=WHITE,
                 font=FONT_XL).pack(pady=(10, 6))
        tk.Label(center,
                 text="Proceed to Unity Center.\nPresent your ID to receive aid.",
                 bg=BG, fg=GRAY, font=FONT_MD,
                 justify="center").pack(pady=(0, 30))

        btn_row = tk.Frame(center, bg=BG)
        btn_row.pack()
        tk.Button(btn_row, text="Claim Again", bg=YELLOW,
                  fg="#1A0030", font=FONT_BOLD, relief="flat",
                  width=14, pady=7,
                  command=self.app.show_claim).pack(side="left",
                                                    padx=8)
        tk.Button(btn_row, text="Return to Aid", bg=BTN_DARK,
                  fg=WHITE, font=FONT_BOLD, relief="flat",
                  width=14, pady=7,
                  command=self.app.show_aid1).pack(side="left",
                                                   padx=8)
