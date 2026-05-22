# ============================================================
# UNITY APP - aid.py
# Part 5 of 6 | Written by: [Miracle Nnadike] | Matric: [25120113034]
# Responsibilities: Aid Screen 1 & 2, Kind donation form,
#                   Cash donation form & confirmation,
#                   Donation Completed screen
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


def _entry_field(parent, label, var, show=""):
    tk.Label(parent, text=label, bg=PURPLE, fg=WHITE,
             font=FONT_SM, anchor="w").pack(fill="x")
    e = tk.Entry(parent, textvariable=var, show=show,
                 bg=LIGHT_BG, fg=WHITE, insertbackground=WHITE,
                 relief="flat", font=FONT_MD)
    e.pack(ipady=6, pady=(2, 8), fill="x")
    return e


# ╔══════════════════════════════════════════════════════════╗
# ║               AID SCREEN 1  (Unity Network)              ║
# ╚══════════════════════════════════════════════════════════╝
class AidScreen1(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        _top_bar(self, self.app, back_cmd=self.app.show_home,
                 title="Unity Network")

        tk.Label(self, bg=BG).pack(pady=20)

        row = tk.Frame(self, bg=BG)
        row.pack(padx=40)

        self._action_card(row,
                          icon="🤲",
                          title="I Want to Donate",
                          desc="Register food, medical\nsupplies or clothing at a\nlocal center.",
                          btn="Donate",
                          cmd=self.app.show_aid2)

        self._action_card(row,
                          icon="🏷️",
                          title="I Need Aid",
                          desc="Show resources and claim\nitems at local center.",
                          btn="View Aid",
                          cmd=self.app.show_claim)

    def _action_card(self, parent, icon, title, desc, btn, cmd):
        card = tk.Frame(parent, bg=PURPLE, width=320, height=240,
                        padx=24, pady=20)
        card.pack(side="left", padx=16)
        card.pack_propagate(False)

        tk.Label(card, text=icon, bg=PURPLE,
                 font=("Arial", 32)).pack(pady=(8, 6))
        tk.Label(card, text=title, bg=PURPLE, fg=WHITE,
                 font=FONT_LG).pack()
        tk.Label(card, text=desc, bg=PURPLE, fg=GRAY,
                 font=FONT_SM, justify="center").pack(pady=6)
        tk.Button(card, text=btn, bg=YELLOW, fg="#1A0030",
                  font=FONT_BOLD, relief="flat", width=14,
                  pady=6, command=cmd).pack(pady=(6, 0))


# ╔══════════════════════════════════════════════════════════╗
# ║              AID SCREEN 2  (Cash / Kind choice)          ║
# ╚══════════════════════════════════════════════════════════╝
class AidScreen2(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        _top_bar(self, self.app, back_cmd=self.app.show_aid1,
                 title="Unity Network")

        tk.Label(self, bg=BG).pack(pady=20)

        row = tk.Frame(self, bg=BG)
        row.pack(padx=40)

        self._type_card(row, icon="💵", title="Cash",
                        desc="Donate any amount.",
                        btn="Donate", cmd=self.app.show_cash)

        self._type_card(row, icon="🎁", title="Kind",
                        desc="Give: drugs, clothes,\nfood etc.",
                        btn="Donate", cmd=self.app.show_kind)

    def _type_card(self, parent, icon, title, desc, btn, cmd):
        card = tk.Frame(parent, bg=PURPLE, width=300, height=220,
                        padx=24, pady=20)
        card.pack(side="left", padx=16)
        card.pack_propagate(False)

        tk.Label(card, text=icon, bg=PURPLE,
                 font=("Arial", 34)).pack(pady=(6, 4))
        tk.Label(card, text=title, bg=PURPLE, fg=WHITE,
                 font=FONT_LG).pack()
        tk.Label(card, text=desc, bg=PURPLE, fg=GRAY,
                 font=FONT_SM, justify="center").pack(pady=4)
        tk.Button(card, text=btn, bg=YELLOW, fg="#1A0030",
                  font=FONT_BOLD, relief="flat", width=12,
                  pady=6, command=cmd).pack(pady=(8, 0))


# ╔══════════════════════════════════════════════════════════╗
# ║               KIND DONATION FORM                         ║
# ╚══════════════════════════════════════════════════════════╝
class KindScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # ── top bar (pack) ────────────────────────────────────
        _top_bar(self, self.app, back_cmd=self.app.show_aid2)

        # ── scrollable body (pack — same geometry manager) ───
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, pady=20)

        # centred card inside body
        card = tk.Frame(body, bg=PURPLE, padx=36, pady=28)
        card.pack(anchor="center", pady=10)

        tk.Label(card, text="Register a Kind Donation",
                 bg=PURPLE, fg=WHITE, font=FONT_LG).pack(pady=(0, 14))

        # form variables
        self.category_var = tk.StringVar()
        self.qty_var      = tk.StringVar()
        self.unit_var     = tk.StringVar()

        _entry_field(card, "Category (e.g. Food, Drugs, Clothes):",
                     self.category_var)

        tk.Label(card, text="Item Description:", bg=PURPLE, fg=WHITE,
                 font=FONT_SM, anchor="w").pack(fill="x")
        self.item_text = tk.Text(card, height=3, width=36,
                                 bg=LIGHT_BG, fg=WHITE,
                                 insertbackground=WHITE,
                                 relief="flat", font=FONT_MD)
        self.item_text.pack(fill="x", pady=(2, 8))

        # quantity + unit side by side
        qty_row = tk.Frame(card, bg=PURPLE)
        qty_row.pack(fill="x", pady=(0, 8))

        col1 = tk.Frame(qty_row, bg=PURPLE)
        col1.pack(side="left", fill="x", expand=True, padx=(0, 8))
        col2 = tk.Frame(qty_row, bg=PURPLE)
        col2.pack(side="left", fill="x", expand=True)

        tk.Label(col1, text="Quantity:", bg=PURPLE, fg=WHITE,
                 font=FONT_SM).pack(anchor="w")
        tk.Entry(col1, textvariable=self.qty_var, bg=LIGHT_BG,
                 fg=WHITE, insertbackground=WHITE, relief="flat",
                 font=FONT_MD).pack(ipady=5, fill="x")

        tk.Label(col2, text="Unit (e.g. kg, bags, packs):",
                 bg=PURPLE, fg=WHITE, font=FONT_SM).pack(anchor="w")
        tk.Entry(col2, textvariable=self.unit_var, bg=LIGHT_BG,
                 fg=WHITE, insertbackground=WHITE, relief="flat",
                 font=FONT_MD).pack(ipady=5, fill="x")

        tk.Button(card, text="Make Donation", bg=YELLOW,
                  fg="#1A0030", font=FONT_BOLD, relief="flat",
                  width=20, pady=7,
                  command=self._donate).pack(pady=(14, 0))

    def _donate(self):
        category = self.category_var.get().strip()
        item     = self.item_text.get("1.0", "end").strip()
        qty      = self.qty_var.get().strip()
        unit     = self.unit_var.get().strip()
        name     = self.app.current_user.get()

        if not category or not item or not qty:
            messagebox.showwarning("Unity App",
                "Please fill in Category, Item Description, and Quantity.")
            return

        # format: "Category: item (qty unit)"
        full_item = f"{category}: {item}"
        full_qty  = f"{qty} {unit}".strip()

        self.app.data.add_donation(name, full_item, full_qty)
        messagebox.showinfo("Unity App", "Donation recorded successfully!")
        self.app.show_donation_done()


# ╔══════════════════════════════════════════════════════════╗
# ║               CASH DONATION FORM                         ║
# ╚══════════════════════════════════════════════════════════╝
class CashScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        # ── top bar (pack) ────────────────────────────────────
        _top_bar(self, self.app, back_cmd=self.app.show_aid2)

        # ── body (pack — same geometry manager) ──────────────
        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, pady=20)

        card = tk.Frame(body, bg=PURPLE, padx=36, pady=28)
        card.pack(anchor="center", pady=10)

        tk.Label(card, text="Register a Cash Donation",
                 bg=PURPLE, fg=WHITE, font=FONT_LG).pack(pady=(0, 14))

        self.amount_var = tk.StringVar()
        self.ref_var    = tk.StringVar()
        self.cause_var  = tk.StringVar()

        _entry_field(card, "Amount (₦):", self.amount_var)
        _entry_field(card, "Transaction Reference:", self.ref_var)
        _entry_field(card, "Cause (e.g. Education, Food):",
                     self.cause_var)

        tk.Button(card, text="Proceed to Donate", bg=YELLOW,
                  fg="#1A0030", font=FONT_BOLD, relief="flat",
                  width=22, pady=7,
                  command=self._proceed).pack(pady=(10, 0))

    def _proceed(self):
        amount = self.amount_var.get().strip()
        ref    = self.ref_var.get().strip()
        cause  = self.cause_var.get().strip()

        if not amount or not ref:
            messagebox.showwarning("Unity App",
                "Amount and Transaction Reference are required.")
            return

        if not cause:
            cause = "General Aid"

        self.app.show_cash_confirm(amount, ref, cause)


# ╔══════════════════════════════════════════════════════════╗
# ║             CASH DONATION CONFIRMATION                   ║
# ╚══════════════════════════════════════════════════════════╝
class CashConfirmScreen(tk.Frame):
    def __init__(self, parent, app, amount="", reference="", cause=""):
        super().__init__(parent, bg=BG)
        self.app       = app
        self.amount    = amount
        self.reference = reference
        self.cause     = cause
        self._build()

    def _build(self):
        _top_bar(self, self.app, back_cmd=self.app.show_cash)

        body = tk.Frame(self, bg=BG)
        body.pack(fill="both", expand=True, pady=20)

        card = tk.Frame(body, bg=PURPLE, padx=36, pady=28)
        card.pack(anchor="center", pady=10)

        tk.Label(card, text="Register a Cash Donation",
                 bg=PURPLE, fg=WHITE, font=FONT_LG).pack(pady=(0, 16))

        details = [
            ("Amount Entered",        self.amount),
            ("Cause",                 self.cause),
            ("Transaction Reference", self.reference),
            ("Account Name",          "Unity Aid Account"),
        ]

        for label, value in details:
            row = tk.Frame(card, bg=LIGHT_BG, pady=8, padx=12)
            row.pack(fill="x", pady=4)
            tk.Label(row, text=label, bg=LIGHT_BG, fg=YELLOW,
                     font=FONT_SM).pack(anchor="w")
            tk.Label(row, text=value, bg=LIGHT_BG, fg=WHITE,
                     font=FONT_BOLD).pack(anchor="w")

        tk.Button(card, text="I Have Donated", bg=YELLOW,
                  fg="#1A0030", font=FONT_BOLD, relief="flat",
                  width=20, pady=7,
                  command=self._confirm).pack(pady=(16, 0))

    def _confirm(self):
        name = self.app.current_user.get()
        self.app.data.add_cash_donation(
            name, self.amount, self.reference, self.cause)
        messagebox.showinfo("Unity App", "Cash donation recorded!")
        self.app.show_donation_done()


# ╔══════════════════════════════════════════════════════════╗
# ║               DONATION COMPLETED                         ║
# ╚══════════════════════════════════════════════════════════╝
class DonationCompleted(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        _top_bar(self, self.app)

        center = tk.Frame(self, bg=BG)
        center.pack(expand=True, pady=80)

        tk.Label(center, text="✅", bg=BG,
                 font=("Arial", 48)).pack()
        tk.Label(center, text="Donation Logged!", bg=BG, fg=WHITE,
                 font=FONT_XL).pack(pady=(8, 4))
        tk.Label(center,
                 text="You are preserving the spirit of our community.",
                 bg=BG, fg=GRAY, font=FONT_MD).pack(pady=(0, 24))

        btn_row = tk.Frame(center, bg=BG)
        btn_row.pack()
        tk.Button(btn_row, text="Donate Again", bg=YELLOW,
                  fg="#1A0030", font=FONT_BOLD, relief="flat",
                  width=14, pady=7,
                  command=self.app.show_aid2).pack(side="left", padx=8)
        tk.Button(btn_row, text="Return to Aid", bg=BTN_DARK,
                  fg=WHITE, font=FONT_BOLD, relief="flat",
                  width=14, pady=7,
                  command=self.app.show_aid1).pack(side="left", padx=8)