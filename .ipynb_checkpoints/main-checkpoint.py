# ============================================================
# UNITY APP - main.py
# Part 1 of 6 | Written by: [Gift Attah] | Matric: [2013]
# Responsibilities: App core, DataManager class, Splash,
#                   Login, and Join screens
# ============================================================

import tkinter as tk
from tkinter import messagebox
import csv
import os

# ── colour palette (matches Figma) ──────────────────────────
BG       = "#1A0030"   # deep purple background
PURPLE   = "#4B0082"   # card / widget fill
YELLOW   = "#FFD700"   # primary action / accent
WHITE    = "#FFFFFF"
GRAY     = "#CCCCCC"
LIGHT_BG = "#2D004F"
BTN_DARK = "#3A006F"

# ── font sizes ───────────────────────────────────────────────
FONT_XL   = ("Arial", 20, "bold")
FONT_LG   = ("Arial", 14, "bold")
FONT_MD   = ("Arial", 11)
FONT_SM   = ("Arial", 9)
FONT_BOLD = ("Arial", 11, "bold")


# ╔══════════════════════════════════════════════════════════╗
# ║              DATA MANAGER  (reads/writes CSV)            ║
# ╚══════════════════════════════════════════════════════════╝
class DataManager:
    """Handles all CSV reading and writing for the Unity App."""

    def __init__(self):
        self.users_file      = "Users.csv"
        self.donations_file  = "donations.csv"
        self.flashcards_file = "flashcards.csv"
        self.quiz_file       = "quiz_questions.csv"
        self.resources_file  = "resources.csv"

    # ── users ────────────────────────────────────────────────
    def _clean(self, row):
        """Strip whitespace and carriage returns from all CSV row values."""
        return {k.strip(): v.strip() for k, v in row.items()}

    def get_users(self):
        users = {}
        try:
            with open(self.users_file, encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("username"):
                        continue
                    parts = line.split(",", 1)
                    if len(parts) == 2:
                        users[parts[0].strip()] = parts[1].strip()
        except FileNotFoundError:
            pass
        return users

    def add_user(self, username, password):
        file_exists = os.path.isfile(self.users_file)
        with open(self.users_file, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["username", "password"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"username": username.strip(),
                             "password": password.strip()})

    def validate_login(self, username, password):
        users = self.get_users()
        return username.strip() in users and users[username.strip()] == password.strip()

    def username_exists(self, username):
        return username.strip() in self.get_users()

    def get_flashcards(self, topic=None):
        cards = []
        try:
            with open(self.flashcards_file, encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row = self._clean(row)
                    if topic is None or topic == "All" or row.get("Topic") == topic:
                        cards.append(row)
        except FileNotFoundError:
            pass
        return cards

    def get_topics(self, source="flashcards"):
        topics = set()
        fname = self.flashcards_file if source == "flashcards" else self.quiz_file
        try:
            with open(fname, encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row = self._clean(row)
                    t = row.get("Topic", "").strip()
                    if t:
                        topics.add(t)
        except FileNotFoundError:
            pass
        return sorted(topics)

    def get_quiz_questions(self, topic=None):
        questions = []
        try:
            with open(self.quiz_file, encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    row = self._clean(row)
                    if topic is None or topic == "All" or row.get("Topic") == topic:
                        questions.append(row)
        except FileNotFoundError:
            pass
        return questions

    def add_donation(self, name, item, quantity):
        file_exists = os.path.isfile(self.donations_file)
        with open(self.donations_file, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "item", "quantity"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"name": name, "item": item, "quantity": quantity})

    def add_cash_donation(self, name, amount, reference, cause):
        file_exists = os.path.isfile(self.donations_file)
        with open(self.donations_file, "a", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=["name", "item", "quantity"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"name": name, "item": f"Cash({cause})",
                             "quantity": amount})

    def get_resources(self):
        resources = []
        try:
            with open(self.resources_file, encoding="utf-8-sig") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    resources.append(self._clean(row))
        except FileNotFoundError:
            pass
        return resources

    def claim_resources(self, selected_items):
        resources = self.get_resources()
        updated = []
        for res in resources:
            matched = next((s for s in selected_items
                           if s["item"] == res["item"].strip()), None)
            if matched:
                remaining = int(res["quantity"]) - int(matched["qty"])
                if remaining > 0:
                    updated.append({"item": res["item"],
                                   "quantity": remaining,
                                   "location": res["location"]})
            else:
                updated.append(res)
        with open(self.resources_file, "w", newline="",
                  encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f,
                fieldnames=["item", "quantity", "location"])
            writer.writeheader()
            writer.writerows(updated)


# ╔══════════════════════════════════════════════════════════╗
# ║                     UNITY APP SHELL                      ║
# ╚══════════════════════════════════════════════════════════╝
class UnityApp(tk.Tk):
    """Root application window — manages screen switching."""

    def __init__(self):
        super().__init__()
        self.title("Unity App")
        self.geometry("900x620")
        self.resizable(False, False)
        self.configure(bg=BG)

        self.data    = DataManager()
        self.current_user = tk.StringVar(value="")

        # container holds all screens
        self.container = tk.Frame(self, bg=BG)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self._show_splash()

    # ── internal imports (avoids circular at module level) ───
    def _import_screens(self):
        from home   import HomeScreen
        from learn  import LearnDashboard, CardsScreen, CardDetailScreen, CompletedScreen
        from quiz   import QuizBoard, QuizScreen, QuizCompletedScreen
        from aid    import AidScreen1, AidScreen2, KindScreen, CashScreen, CashConfirmScreen, DonationCompleted
        from claim  import ClaimScreen, ItemClaimedScreen
        return (HomeScreen, LearnDashboard, CardsScreen, CardDetailScreen, CompletedScreen,
                QuizBoard, QuizScreen, QuizCompletedScreen,
                AidScreen1, AidScreen2, KindScreen, CashScreen, CashConfirmScreen, DonationCompleted,
                ClaimScreen, ItemClaimedScreen)

    def _show_splash(self):
        SplashScreen(self.container, self).grid(row=0, column=0, sticky="nsew")

    def show_frame(self, frame_class, **kwargs):
        """Destroy current screen and show new one."""
        for widget in self.container.winfo_children():
            widget.destroy()
        frame = frame_class(self.container, self, **kwargs)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def show_login(self):        self.show_frame(LoginScreen)
    def show_join(self):         self.show_frame(JoinScreen)

    def show_home(self):
        screens = self._import_screens()
        self.show_frame(screens[0])   # HomeScreen

    def show_learn(self):
        screens = self._import_screens()
        self.show_frame(screens[1])   # LearnDashboard

    def show_cards(self, topic="All"):
        screens = self._import_screens()
        self.show_frame(screens[2], topic=topic)

    def show_card_detail(self, cards, index=0):
        screens = self._import_screens()
        self.show_frame(screens[3], cards=cards, index=index)

    def show_completed(self, cards):
        screens = self._import_screens()
        self.show_frame(screens[4], cards=cards)

    def show_quizboard(self):
        screens = self._import_screens()
        self.show_frame(screens[5])

    def show_quiz(self, topic="All"):
        screens = self._import_screens()
        self.show_frame(screens[6], topic=topic)

    def show_quiz_completed(self, score, total):
        screens = self._import_screens()
        self.show_frame(screens[7], score=score, total=total)

    def show_aid1(self):
        screens = self._import_screens()
        self.show_frame(screens[8])

    def show_aid2(self):
        screens = self._import_screens()
        self.show_frame(screens[9])

    def show_kind(self):
        screens = self._import_screens()
        self.show_frame(screens[10])

    def show_cash(self):
        screens = self._import_screens()
        self.show_frame(screens[11])

    def show_cash_confirm(self, amount, reference, cause):
        screens = self._import_screens()
        self.show_frame(screens[12], amount=amount, reference=reference, cause=cause)

    def show_donation_done(self):
        screens = self._import_screens()
        self.show_frame(screens[13])

    def show_claim(self):
        screens = self._import_screens()
        self.show_frame(screens[14])

    def show_item_claimed(self):
        screens = self._import_screens()
        self.show_frame(screens[15])


# ╔══════════════════════════════════════════════════════════╗
# ║                     SPLASH SCREEN                        ║
# ╚══════════════════════════════════════════════════════════╝
class SplashScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()
        self.after(2500, app.show_login)

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        center = tk.Frame(self, bg=BG)
        center.grid(row=0, column=0)

        # coloured circles (A K C)
        canvas = tk.Canvas(center, width=100, height=100, bg=BG, highlightthickness=0)
        canvas.pack(pady=(60, 8))
        canvas.create_oval(0, 10, 55, 65, fill="#E63950", outline="")   # red  – A
        canvas.create_oval(35, 0, 90, 55, fill="#3A86FF", outline="")   # blue – K
        canvas.create_oval(20, 40, 75, 95, fill="#2EC4B6", outline="")  # teal – C
        canvas.create_text(20, 37, text="A", fill=WHITE, font=("Arial", 14, "bold"))
        canvas.create_text(65, 27, text="K", fill=WHITE, font=("Arial", 14, "bold"))
        canvas.create_text(47, 68, text="C", fill=WHITE, font=("Arial", 14, "bold"))

        tk.Label(center, text="Unity App", bg=BG, fg=WHITE,
                 font=("Arial", 22, "bold")).pack()
        tk.Label(center, text='"Peace starts from sharing"', bg=BG, fg=GRAY,
                 font=("Arial", 11, "italic")).pack(pady=(4, 0))


# ╔══════════════════════════════════════════════════════════╗
# ║                      LOGIN SCREEN                        ║
# ╚══════════════════════════════════════════════════════════╝
class LoginScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = tk.Frame(self, bg=PURPLE, padx=40, pady=35)
        card.grid(row=0, column=0)

        # logo row
        logo_row = tk.Frame(card, bg=PURPLE)
        logo_row.pack(pady=(0, 12))
        canvas = tk.Canvas(logo_row, width=42, height=42, bg=PURPLE, highlightthickness=0)
        canvas.pack(side="left", padx=(0, 8))
        canvas.create_oval(0, 5, 24, 29, fill="#E63950", outline="")
        canvas.create_oval(14, 0, 38, 24, fill="#3A86FF", outline="")
        canvas.create_oval(8, 18, 32, 42, fill="#2EC4B6", outline="")
        tk.Label(logo_row, text="Unity App", bg=PURPLE, fg=WHITE,
                 font=("Arial", 13, "bold")).pack(side="left")

        tk.Label(card, text="Peace starts from sharing", bg=PURPLE, fg=GRAY,
                 font=FONT_SM).pack(pady=(0, 18))

        # fields
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self._field(card, "Username:", self.username_var)
        self._field(card, "Password:", self.password_var, show="*")

        tk.Button(card, text="Login to Account", bg=YELLOW, fg="#1A0030",
                  font=FONT_BOLD, relief="flat", width=22, pady=7,
                  command=self._login).pack(pady=(16, 6))

        tk.Button(card, text="Create New Account", bg=PURPLE, fg=YELLOW,
                  font=FONT_SM, relief="flat", cursor="hand2",
                  command=self.app.show_join).pack()

    def _field(self, parent, label, var, show=""):
        tk.Label(parent, text=label, bg=PURPLE, fg=WHITE, font=FONT_SM,
                 anchor="w").pack(fill="x")
        entry = tk.Entry(parent, textvariable=var, show=show, bg=LIGHT_BG, fg=WHITE,
                         insertbackground=WHITE, relief="flat", font=FONT_MD,
                         width=26)
        entry.pack(ipady=6, pady=(2, 10), fill="x")

    def _login(self):
        u = self.username_var.get().strip()
        p = self.password_var.get().strip()
        if not u or not p:
            messagebox.showwarning("Unity App", "Please fill in both fields.")
            return
        if self.app.data.validate_login(u, p):
            self.app.current_user.set(u)
            self.app.show_home()
        else:
            messagebox.showerror("Unity App", "Invalid username or password.")


# ╔══════════════════════════════════════════════════════════╗
# ║                       JOIN SCREEN                        ║
# ╚══════════════════════════════════════════════════════════╝
class JoinScreen(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app
        self._build()

    def _build(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        card = tk.Frame(self, bg=PURPLE, padx=40, pady=30)
        card.grid(row=0, column=0)

        tk.Label(card, text="Join Unity", bg=PURPLE, fg=WHITE,
                 font=FONT_XL).pack(pady=(0, 16))

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_var  = tk.StringVar()

        self._field(card, "Choose Username:", self.username_var)
        self._field(card, "Password:",        self.password_var, show="*")
        self._field(card, "Confirm Password:", self.confirm_var, show="*")

        tk.Button(card, text="Register Account", bg=YELLOW, fg="#1A0030",
                  font=FONT_BOLD, relief="flat", width=22, pady=7,
                  command=self._register).pack(pady=(14, 0))

    def _field(self, parent, label, var, show=""):
        tk.Label(parent, text=label, bg=PURPLE, fg=WHITE,
                 font=FONT_SM, anchor="w").pack(fill="x")
        entry = tk.Entry(parent, textvariable=var, show=show, bg=LIGHT_BG, fg=WHITE,
                         insertbackground=WHITE, relief="flat", font=FONT_MD, width=26)
        entry.pack(ipady=6, pady=(2, 10), fill="x")

    def _register(self):
        u = self.username_var.get().strip()
        p = self.password_var.get().strip()
        c = self.confirm_var.get().strip()

        if not u or not p or not c:
            messagebox.showwarning("Unity App", "Please fill in all fields.")
            return
        if p != c:
            messagebox.showerror("Unity App", "Passwords do not match.")
            return
        if self.app.data.username_exists(u):
            messagebox.showerror("Unity App", "Username already taken.")
            return

        self.app.data.add_user(u, p)
        self.app.current_user.set(u)
        messagebox.showinfo("Unity App", f"Welcome to Unity, {u}!")
        self.app.show_home()


# ── entry point ──────────────────────────────────────────────
if __name__ == "__main__":
    app = UnityApp()
    app.mainloop()
