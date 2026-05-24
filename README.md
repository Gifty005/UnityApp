# Unity App
### COS 102 — Introduction to Problem Solving | CA3 Group Project
### Pan-Atlantic University | School of Science and Technology

---

## Theme
War and Conflict — Post-War National Unity and Community Aid

---

## About the App
Unity App is a desktop application built for Nigerian communities 
that addresses two problems that arise from conflict and division:

1. The erosion of shared historical memory and cultural knowledge
2. The breakdown of community aid networks for vulnerable people

The app brings both solutions together in one platform — a learning 
hub where users can study Nigerian history through flashcards and 
quizzes, and an aid hub where donors can register food, clothing and 
cash donations while those in need can claim available 
resources at local centers.

The name Unity App and the tagline "Peace starts from sharing" 
is inspired by the post-civil war declaration by General Yakubu Gowon "No Victor, 
No Vanquished", which called Nigerians to unity after the war.

---

## Features

### Learn Hub
- Flashcard system with topics covering Nigerian History, 
  Culture, Geography and Technology
- Users can select a topic and go through cards one by one
- Deck completion screen with option to review again

### Quiz Hub  
- Multiple choice quiz with topic selection
- Score tracking across all questions
- Correct answer highlighted in green after each submission
- Wrong answer highlighted in red
- Final score and grade message at the end

### Aid Hub — Donate
- Users can register Kind donations (food, drugs, clothes)
- Users can register Cash donations with transaction reference
- Cash confirmation screen before final submission
- All donations saved to donations.csv automatically

### Aid Hub — Claim
- Users can browse all available aid resources
- Live search to filter items by name
- Checkbox selection with quantity input
- Items reserved and quantities updated in resources.csv

### User Authentication
- Secure login with username and password
- New user registration
- All user data saved to Users.csv

---

## Tech Stack
- Language: Python 3
- GUI Library: Tkinter
- Data Storage: CSV files (csv module)
- Other modules: os, random

---

## File Structure
unity-app/
├── main.py              # App engine, DataManager, Splash, Login, Join
├── home.py              # Home Screen
├── learn.py             # Flashcard screens
├── quiz.py              # Quiz screens
├── aid.py               # Donation screens
├── claim.py             # Claim resources screens
├── Users.csv            # User login data
├── flashcards.csv       # Flashcard content
├── quiz_questions.csv   # Quiz questions and answers
├── donations.csv        # Donation records (written by app)
└── resources.csv        # Available aid items

## How to Run
1. Make sure Python 3 is installed on your computer
2. Clone this repository
3. Make sure all CSV files are in the same folder as the Python files
4. Run the app:
5. Click Create New Account to register

## Submission
- Course: COS 102 — Introduction to Problem Solving
- Department: Data Science
- Institution: Pan-Atlantic University
- Submission Deadline: Sunday May 24 2026
