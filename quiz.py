import tkinter as tk
from tkinter import messagebox
import random

BG       = "#1A0030"
PURPLE   = "#4B0082"
YELLOW   = "#FFD700"
WHITE    = "#FFFFFF"
GRAY     = "#CCCCCC"
LIGHT_BG = "#2D004F"
BTN_DARK = "#3A006F"
GREEN    = "#2EC4B6"
RED      = "#E63950"

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


def _make_options(correct, all_answers):
    wrong  = [a for a in all_answers if a.strip() != correct.strip()]
    chosen = random.sample(wrong, min(3, len(wrong)))
    opts   = chosen + [correct]
    random.shuffle(opts)
    return opts

# Making the quiz board
class QuizBoard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app            = app
        self.selected_topic = None   # set when user clicks a topic button
        self._build()

    def _build(self):
        _top_bar(self, self.app, back_cmd=self.app.show_learn)

        center = tk.Frame(self, bg=BG)
        center.pack(expand=True, pady=30)

        tk.Label(center, text="Ready to test yourself?",
                 bg=BG, fg=WHITE, font=FONT_XL).pack(pady=(0, 6))
        tk.Label(center, text="Select a topic below:",
                 bg=BG, fg=GRAY, font=FONT_MD).pack(pady=(0, 16))

        # ── load topics from CSV ──────────────────────────────
        raw = self.app.data.get_topics("quiz")
        topics = ["All"] + [t.strip() for t in raw if t.strip()]

        # ── topic buttons (more reliable than OptionMenu) ─────
        btn_frame = tk.Frame(center, bg=BG)
        btn_frame.pack(pady=(0, 16))

        self.topic_btns = {}
        for t in topics:
            btn = tk.Button(
                btn_frame, text=t,
                bg=LIGHT_BG, fg=WHITE,
                font=FONT_MD, relief="flat",
                width=12, pady=6,
                command=lambda topic=t: self._select_topic(topic)
            )
            btn.pack(side="left", padx=6)
            self.topic_btns[t] = btn

        # highlight All by default
        self._select_topic("All")

       
        self.selected_lbl = tk.Label(
            center,
            text="Selected: All",
            bg=BG, fg=YELLOW, font=FONT_BOLD)
        self.selected_lbl.pack(pady=(0, 16))

        tk.Button(center, text="Start Quiz", bg=YELLOW,
                  fg="#1A0030", font=FONT_BOLD, relief="flat",
                  width=18, pady=8,
                  command=self._start).pack()

    def _select_topic(self, topic):
        """Highlight chosen topic button and record selection."""
        self.selected_topic = topic
        for t, btn in self.topic_btns.items():
            if t == topic:
                btn.config(bg=YELLOW, fg="#1A0030",
                           font=FONT_BOLD)
            else:
                btn.config(bg=LIGHT_BG, fg=WHITE,
                           font=FONT_MD)
        
        if hasattr(self, "selected_lbl"):
            self.selected_lbl.config(text=f"Selected: {topic}")

    def _start(self):
        topic = self.selected_topic or "All"
        if topic == "All":
            qs = self.app.data.get_quiz_questions(None)
        else:
            qs = self.app.data.get_quiz_questions(topic)

        # clean every field
        qs = [{k.strip(): v.strip() for k, v in q.items()} for q in qs]

        if not qs:
            messagebox.showinfo("Unity App",
                "No questions found for that topic.")
            return

        for w in self.app.container.winfo_children():
            w.destroy()
        frame = QuizScreen(self.app.container, self.app,
                           topic=topic, questions=qs,
                           q_index=0, score=0)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

# Making the quiz screen
class QuizScreen(tk.Frame):
    def __init__(self, parent, app,
                 topic="All", questions=None,
                 q_index=0, score=0):
        super().__init__(parent, bg=BG)
        self.app       = app
        self.topic     = topic
        self.questions = questions or []
        self.q_index   = q_index
        self.score     = score
        self.selected  = tk.StringVar(value="")
        self.answered  = False
        self.option_frames = []
        self._build()

    def _build(self):
        total = len(self.questions)
        q     = self.questions[self.q_index]

        _top_bar(self, self.app, back_cmd=self.app.show_quizboard)

        # ── progress ─────────────────────────────────────────
        hdr = tk.Frame(self, bg=BG)
        hdr.pack(fill="x", padx=20, pady=(8, 0))
        tk.Label(hdr, text=f"Question {self.q_index + 1} of {total}",
                 bg=BG, fg=YELLOW, font=FONT_LG).pack(side="left")
        tk.Label(hdr, text=f"Score: {self.score}",
                 bg=BG, fg=YELLOW, font=FONT_BOLD).pack(side="right")

        # ── question box ──────────────────────────────────────
        q_box = tk.Frame(self, bg=LIGHT_BG, padx=20, pady=14)
        q_box.pack(fill="x", padx=20, pady=8)
        tk.Label(q_box, text=q["Question"], bg=LIGHT_BG,
                 fg=WHITE, font=FONT_MD,
                 wraplength=680, justify="left").pack(anchor="w")

        # ── build options ─────────────────────────────────────
        correct     = q["Answer"].strip()
        all_answers = [r["Answer"].strip() for r in self.questions]
        options     = _make_options(correct, all_answers)

        self.correct_answer = correct
        self.option_frames  = []

        opts_frame = tk.Frame(self, bg=BG)
        opts_frame.pack(fill="x", padx=30, pady=6)

        for i, opt in enumerate(options):
            row_f = tk.Frame(opts_frame, bg=BG)
            row_f.pack(anchor="w", fill="x", pady=3)
            rb = tk.Radiobutton(
                row_f,
                text=f"  {chr(65+i)}.  {opt}",
                variable=self.selected,
                value=opt,
                bg=BG, fg=WHITE,
                selectcolor=PURPLE,
                font=FONT_MD,
                activebackground=BG,
                activeforeground=WHITE,
                anchor="w"
            )
            rb.pack(side="left", fill="x")
            self.option_frames.append((row_f, rb, opt))

        # ── feedback label ────────────────────────────────────
        self.feedback_lbl = tk.Label(self, text="",
                                     bg=BG, font=FONT_BOLD)
        self.feedback_lbl.pack(pady=4)

        # ── action button ─────────────────────────────────────
        self.btn_var = tk.StringVar(value="Submit Answer")
        self.action_btn = tk.Button(
            self,
            textvariable=self.btn_var,
            bg=YELLOW, fg="#1A0030",
            font=FONT_BOLD, relief="flat",
            width=18, pady=7,
            command=self._on_button)
        self.action_btn.pack(pady=12, anchor="e", padx=30)

    def _on_button(self):
        if not self.answered:
            self._submit()
        else:
            self._next()

    def _submit(self):
        chosen = self.selected.get().strip()
        if not chosen:
            messagebox.showinfo("Unity App",
                "Please select an answer first.")
            return

        self.answered = True
        correct       = self.correct_answer
        is_correct    = (chosen == correct)
        is_last       = (self.q_index == len(self.questions) - 1)

        if is_correct:
            self.score += 1

        # colour options: green = correct, red = wrong choice
        for row_f, rb, opt_text in self.option_frames:
            opt_clean = opt_text.strip()
            if opt_clean == correct:
                row_f.config(bg="#0D3D2B")
                rb.config(bg="#0D3D2B", fg=GREEN,
                          font=("Arial", 11, "bold"))
            elif opt_clean == chosen and not is_correct:
                row_f.config(bg="#3D0D0D")
                rb.config(bg="#3D0D0D", fg=RED,
                          font=("Arial", 11, "bold"))

        # feedback message
        if is_correct:
            self.feedback_lbl.config(
                text="✅  Correct!", fg=GREEN)
        else:
            self.feedback_lbl.config(
                text=f"❌  Wrong!   Correct answer:  {correct}",
                fg=RED)

        # update button text
        self.btn_var.set(
            "See Results 🏆" if is_last else "Next Question →")

    def _next(self):
        next_index = self.q_index + 1
        if next_index >= len(self.questions):
            self.app.show_quiz_completed(
                self.score, len(self.questions))
        else:
            for w in self.app.container.winfo_children():
                w.destroy()
            frame = QuizScreen(
                self.app.container, self.app,
                topic=self.topic,
                questions=self.questions,
                q_index=next_index,
                score=self.score)
            frame.grid(row=0, column=0, sticky="nsew")
            frame.tkraise()


# Making the quiz completed screen
class QuizCompletedScreen(tk.Frame):
    def __init__(self, parent, app, score=0, total=0):
        super().__init__(parent, bg=BG)
        self.app   = app
        self.score = score
        self.total = total
        self._build()

    def _build(self):
        _top_bar(self, self.app)

        center = tk.Frame(self, bg=BG)
        center.pack(expand=True, pady=40)

        tk.Label(center, text="🏆", bg=BG,
                 font=("Arial", 52)).pack()
        tk.Label(center, text="Quiz Completed!", bg=BG, fg=WHITE,
                 font=FONT_XL).pack(pady=(8, 4))
        tk.Label(center,
                 text=f"Your Score:  {self.score} / {self.total}",
                 bg=BG, fg=YELLOW, font=FONT_LG).pack(pady=(4, 8))

        pct = (self.score / self.total * 100) if self.total else 0
        if pct == 100:
            msg = "🎉 Perfect score! Outstanding!"
        elif pct >= 70:
            msg = "Great job! You are preserving history."
        elif pct >= 50:
            msg = "Good effort. Keep studying!"
        else:
            msg = "Keep going — every attempt teaches you more."

        tk.Label(center, text=msg, bg=BG, fg=GRAY,
                 font=FONT_MD).pack(pady=(0, 30))

        btn_row = tk.Frame(center, bg=BG)
        btn_row.pack()
        tk.Button(btn_row, text="Retake Quiz", bg=YELLOW,
                  fg="#1A0030", font=FONT_BOLD, relief="flat",
                  width=14, pady=7,
                  command=self.app.show_quizboard).pack(
                  side="left", padx=8)
        tk.Button(btn_row, text="Dashboard", bg=BTN_DARK,
                  fg=WHITE, font=FONT_BOLD, relief="flat",
                  width=14, pady=7,
                  command=self.app.show_home).pack(
                  side="left", padx=8)
