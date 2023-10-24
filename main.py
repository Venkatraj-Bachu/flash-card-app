import tkinter
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
data_list = []


# ---------------------------- READ DATA ------------------------------- #
try:
    data = pandas.read_csv('data/words_to_learn.csv')
except FileNotFoundError:
    data = pandas.read_csv('data/french_words.csv')
data = data.to_dict(orient="records")
data_list = list(data)


# ---------------------------- FLIP CARD ------------------------------- #
def flip_card():
    canvas.itemconfig(card_image, image=card_back)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')


# ---------------------------- SHUFFLE CARD ------------------------------- #
def shuffle_deck():
    global current_card, flip, data_list
    window.after_cancel(flip)
    current_card = random.choice(data_list)
    canvas.itemconfig(card_image, image=card_front)
    canvas.itemconfig(card_title, text='French', fill='black')
    canvas.itemconfig(card_word, text=current_card['French'], fill='black')
    flip = window.after(3000, flip_card)


# ---------------------------- UPDATE LEARNT WORDS ------------------------------- #
def learnt_word():
    data_list.remove(current_card)
    new_data = pandas.DataFrame(data_list)
    new_data.to_csv('data/words_to_learn.csv', index=False)
    shuffle_deck()


# ---------------------------- UI SETUP ------------------------------- #
window = tkinter.Tk()
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.title("Flashy")

canvas = tkinter.Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = tkinter.PhotoImage(file='images/card_front.png')
card_back = tkinter.PhotoImage(file='images/card_back.png')
card_image = canvas.create_image(400, 263, image=card_front)
canvas.grid(column=0, row=0, columnspan=2)
card_title = canvas.create_text(400, 100, text='French', font=("Ariel", 40, "italic"), fill='black')
card_word = canvas.create_text(400, 250, text='This is the french!', font=("Cambria", 28, "bold"), fill='black')

wrong_img = tkinter.PhotoImage(file='images/wrong.png')
right_img = tkinter.PhotoImage(file='images/right.png')
wrong_button = tkinter.Button(image=wrong_img, highlightthickness=0, command=shuffle_deck)
right_button = tkinter.Button(image=right_img, highlightthickness=0, command=learnt_word)
wrong_button.grid(column=0, row=1)
right_button.grid(column=1, row=1)

flip = window.after(3000, flip_card)

shuffle_deck()

window.mainloop()
