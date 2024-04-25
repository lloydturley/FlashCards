import os.path
import random
from tkinter import *
import pandas

BACKGROUND_COLOR = "#B1DDC6"


if os.path.exists("./data/words_to_learn.csv"):
    data = pandas.read_csv("./data/words_to_learn.csv")
    to_learn = data.to_dict(orient="records")
else:
    data = pandas.read_csv("./data/french_words.csv")
    to_learn = data.to_dict(orient="records")

current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_image)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    canvas.itemconfig(card_background, image=card_back_image)


def is_known():
    to_learn.remove(current_card)
    next_card()
    data2 = pandas.DataFrame(to_learn)
    data2.to_csv("./data/words_to_learn.csv", index=False)


window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(height="526", width="800", bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_image = PhotoImage(file="./images/card_front.png")
card_back_image = PhotoImage(file="./images/card_back.png")
card_background = canvas.create_image(405, 265, image=card_front_image)
card_title = canvas.create_text(400, 175, text="", font='Helvetica 40 italic', tags="language")
card_word = canvas.create_text(400, 350, text="", font='Helvetica 70 bold', tags="learn_word")
canvas.grid(row=0, column=0, columnspan=2)

right_image = PhotoImage(file="./images/right.png")
wrong_image = PhotoImage(file="./images/wrong.png")
right_btn = Button(image=right_image, highlightthickness=0, command=is_known)
wrong_btn = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_btn.grid(row=1, column=0)
right_btn.grid(row=1, column=1)

next_card()

window.mainloop()
