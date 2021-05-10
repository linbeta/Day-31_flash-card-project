from tkinter import *
from tkinter import messagebox
import pandas
import random
import os

BACKGROUND_COLOR = "#B1DDC6"
FONT_LANGUAGE = ("Arial", 40, "italic")
FONT_WORD = ("Arial", 60, "bold")
question = {}
flip_timer = NONE

# --- load the words to display (use pandas), click [x],[v] to show next word randomly---
# french_data = pandas.read_csv("data/french_words.csv")
try:
    french_data = pandas.read_csv("data/progress.csv")
except FileNotFoundError:
    french_data = pandas.read_csv("data/french_words.csv")
finally:
    words_to_learn = french_data.to_dict(orient="records")


# --- flip next card ---
def next_card():
    global question, flip_timer
    flashy.after_cancel(flip_timer)
    question = random.choice(words_to_learn)
    card_canvas.itemconfig(card, image=card_front_img)
    card_canvas.itemconfig(card_title, text="French", fill="black")
    card_canvas.itemconfig(word, text=question['French'], fill="black")
    flip_timer = flashy.after(3000, show_answer)
    # print(f"Q: {question['French']}, A: {question['English']}")

# --- flip the card to show answer, update progress if click [v] ---
def show_answer():
    card_canvas.itemconfig(card, image=card_back_img)
    card_canvas.itemconfig(card_title, text="English", fill="white")
    card_canvas.itemconfig(word, text=question['English'], fill="white")

# --- save to file so that user could use and review next time ---
def update_progress():
    global question
    if len(words_to_learn) > 1:
        words_to_learn.remove(question)
        # convert list back to dataframe, and to csv
        progress = pandas.DataFrame(words_to_learn)
        progress.to_csv("data/progress.csv", index=False)
    else:
        messagebox.showinfo(title="There's no word to learn",
                            message="Congratulation! You've review all the words!\nGood job, keep up the good work!")
        os.remove("data/progress.csv")
    # print(f"Que: {question}, full list: {len(words_to_learn)}")


# french_data = pandas.read_csv("data/french_words.csv")
# words_to_learn = french_data.to_dict(orient="records")

# --- The UI design layout (Tkinter) ---
flashy = Tk()
flashy.minsize(width=800, height=700)
flashy.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flashy.title("flashy")

# layout on the card canvas: 1. load image and save to variables, display. 2. show two sets of texts on the canvas.
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card = card_canvas.create_image(400, 268, image=card_front_img)
card_canvas.grid(row=0, column=0, columnspan=2)
card_title = card_canvas.create_text(400, 150, text="", font=FONT_LANGUAGE)
word = card_canvas.create_text(400, 263, text="", font=FONT_WORD)

# correct and wrong buttons layout
wrong_btn_img = PhotoImage(file="images/wrong.png")
right_btn_img = PhotoImage(file="images/right.png")
wrong_btn = Button(image=wrong_btn_img, highlightthickness=0, command=next_card)
wrong_btn.grid(row=1, column=0)
right_btn = Button(image=right_btn_img, highlightthickness=0, command=lambda: [next_card(), update_progress()])
right_btn.grid(row=1, column=1)

# Load the first card when running the program
next_card()

flashy.mainloop()
