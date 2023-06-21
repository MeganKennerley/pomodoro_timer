from tkinter import *
import math
import beepy
# ---------------------------- CONSTANTS ------------------------------- #
TAN = "#FFD3B0"
RED = "#FF6969"
BLUE = "#A6D0DD"
YELLOW = "#FFF9DE"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
my_timer = None
count_min = 0
count_sec = 0


def window_to_front():

    window.lift()
    window.focus_force()
    beepy.beep(sound=1)
    beepy.beep(sound='coin')


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():

    window.after_cancel(my_timer)
    canvas.itemconfig(timer_text, text="00:00")
    timer.config(text="Timer")
    check_mark.config(text="")
    global reps
    reps = 0


def pause():
    global my_timer
    window.after_cancel(my_timer)
    start_button.config(text='Resume', command=resume)


def resume():

    global reps
    reps -= 1
    if count_min < 0:
        count_down(count_sec)
    else:
        count_down(count_min * 60 + count_sec)
    start_button.config(text='Pause', command=pause)


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():

    global reps
    reps += 1

    start_button.config(text="Pause", command=pause)

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        window_to_front()
        count_down(long_break_sec)
        timer.config(text="Long Break", fg=RED)
    elif reps % 2 == 0:
        window_to_front()
        count_down(short_break_sec)
        timer.config(text="Break", fg=TAN)
    else:
        if reps != 1:
            window_to_front()
        count_down(work_sec)
        timer.config(text="Work", fg=YELLOW)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):

    global count_min
    global count_sec
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global my_timer
        my_timer = window.after(1000, count_down, count - 1)
    else:
        start_timer()
        if (reps % 2) == 0:
            check_mark.config(text="✔")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=BLUE)

# Tomato and Background
canvas = Canvas(width=200, height=224, bg=BLUE, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)

# Labels
timer = Label(text="Timer", fg=YELLOW, bg=BLUE, font=(FONT_NAME, 58))
timer.grid(row=0, column=1)

start_button = Button(text="Start", bg=BLUE, highlightthickness=2, highlightcolor=BLUE,
                      highlightbackground=BLUE, command=start_timer, width=7)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", bg=BLUE, highlightthickness=2, highlightcolor=BLUE,
                      highlightbackground=BLUE, command=reset_timer, width=7)
reset_button.grid(row=2, column=2)

check_mark = Label(fg=BLUE, bg=BLUE)
check_mark.grid(row=3, column=1)


window.mainloop()