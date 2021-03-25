# Sophia Chang, CIS345 10:30, Project
from tkinter import *
from tkinter import ttk
from difflib import get_close_matches
import random


class Question:
    """Question Builder for quiz"""
    global pts

    def __init__(self, text, pt, c1, c2, c3, c4, cf, inc_f, correct_ans):
        self.question_text = text
        self.points = pt
        self.choice1 = c1
        self.choice2 = c2
        self.choice3 = c3
        self.choice4 = c4
        self.correct_feedback = cf
        self.inc_feedback = inc_f
        self.correct_answer = correct_ans

    @property
    def question_text(self):
        return self.__question_text

    @question_text.setter
    def question_text(self, new_text):
        self.__question_text = new_text

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, new_pts):
        if new_pts == '1' or new_pts == '2' or new_pts == '3':
            self.__points = new_pts
        else:
            self.__points = 'Invalid'

    @property
    def choice1(self):
        return self.__choice1

    @choice1.setter
    def choice1(self, new_choice):
        self.__choice1 = new_choice

    @property
    def choice2(self):
        return self.__choice2

    @choice2.setter
    def choice2(self, new_choice):
        self.__choice2 = new_choice

    @property
    def choice3(self):
        return self.__choice3

    @choice3.setter
    def choice3(self, new_choice):
        self.__choice3 = new_choice

    @property
    def choice4(self):
        return self.__choice4

    @choice4.setter
    def choice4(self, new_choice):
        self.__choice4 = new_choice

    @property
    def correct_feedback(self):
        return self.__correct_feedback

    @correct_feedback.setter
    def correct_feedback(self, new_cfeedback):
        self.__correct_feedback = new_cfeedback

    @property
    def inc_feedback(self):
        return self.__inc_feedback

    @inc_feedback.setter
    def inc_feedback(self, new_incfeedback):
        self.__inc_feedback = new_incfeedback

    @property
    def correct_answer(self):
        return self.__correct_answer

    @correct_answer.setter
    def correct_answer(self, new_correct_ans):
        self.__correct_answer = new_correct_ans

    def __str__(self):
        return f'{self.question_text},{self.points},{self.choice1},{self.choice2},{self.choice3},' \
               f'{self.choice4},{self.correct_feedback},{self.inc_feedback},{self.correct_answer}\n'


def list_click(event):
    """Double clicking on an item in the listbox will set the entries"""
    global question, pts, choice1, choice2, choice3, choice4, \
        correct_feedback, incorrect_feedback, correct_answer, question_detail_list, index
    index = list_box.curselection()[0]
    ques = question_detail_list[index]
    question.set(ques.question_text)
    pts.set(ques.points)
    choice1.set(ques.choice1)
    choice2.set(ques.choice2)
    choice3.set(ques.choice3)
    choice4.set(ques.choice4)
    correct_feedback.set(ques.correct_feedback)
    incorrect_feedback.set(ques.inc_feedback)
    correct_answer.set(ques.correct_answer)


def get_questions(file):
    """Retrieves questions from the txt file"""
    with open(file, 'r') as fp:
        for lines in fp:
            newline = lines.strip()
            yield newline


def save_click():
    """Saves questions and updates the txt file"""
    global question_list, question, pts, choice1, choice2, choice3, choice4, \
        correct_feedback, incorrect_feedback, correct_answer, index, edit_mode
    new_question = question.get()
    new_pts = pts.get()
    new_choice1 = choice1.get()
    new_choice2 = choice2.get()
    new_choice3 = choice3.get()
    new_choice4 = choice4.get()
    new_cfeedback = correct_feedback.get()
    new_ifeedback = incorrect_feedback.get()
    new_canswer = correct_answer.get()
    try:
        new_ques = Question(new_question, new_pts, new_choice1, new_choice2, new_choice3, new_choice4,
                            new_cfeedback, new_ifeedback, new_canswer)
    except (ValueError, TypeError) as ex:
        listbox_label.config(text=ex)
        listbox_label.config(bg='yellow')
    else:
        if edit_mode:
            question_list.pop(index)
            question_list.insert(index, new_ques.question_text)
            question_detail_list.pop(index)
            question_detail_list.insert(index, new_ques)

            with open('Questions.txt', 'w') as fp:
                for q in question_detail_list:
                    fp.write(str(q))
            insert_listbox()
            edit_mode = False
        else:
            question_list.append(new_ques.question_text)
            question_detail_list.append(new_ques)
            with open('Questions.txt', 'w') as fp:
                for q in question_detail_list:
                    fp.write(str(q))
            insert_listbox()


def show_questions():
    """Shows the questions in the listbox"""
    global question_list, question_detail_list, existing_question, existing_pts, existing_choice1, existing_choice2, \
        existing_choice3, existing_choice4, existing_correct_feedback, existing_incorrect_feedback, \
        existing_correct_answer
    toggle()
    insert_listbox()


def add_question():
    """Allows users to add a question to the existing pool of 10 questions"""
    global edit_mode
    edit_mode = False
    toggle()
    insert_listbox()
    question_entry['state'] = NORMAL
    points_entry['state'] = NORMAL
    choice1_entry['state'] = NORMAL
    choice2_entry['state'] = NORMAL
    choice3_entry['state'] = NORMAL
    choice4_entry['state'] = NORMAL
    cfeedback_entry['state'] = NORMAL
    ifeedback_entry['state'] = NORMAL
    cchoice_entry['state'] = NORMAL
    listbox_label.config(text='', bg=color)


def edit_question():
    """Allows users to edit an existing question"""
    global existing_question, existing_pts, existing_choice1, existing_choice2, existing_choice3, existing_choice4, \
        existing_correct_feedback, existing_incorrect_feedback, existing_correct_answer, edit_mode
    edit_mode = True
    toggle()
    listbox_label.config(text='Double click on a question to edit.')
    listbox_label.config(bg='yellow')
    insert_listbox()

    question_entry['state'] = NORMAL
    points_entry['state'] = NORMAL
    choice1_entry['state'] = NORMAL
    choice2_entry['state'] = NORMAL
    choice3_entry['state'] = NORMAL
    choice4_entry['state'] = NORMAL
    cfeedback_entry['state'] = NORMAL
    ifeedback_entry['state'] = NORMAL
    cchoice_entry['state'] = NORMAL


def delete(event):
    """Deletes the question selected by the user from the txt file"""
    deleted_index = list_box.curselection()[0]
    question_detail_list.pop(deleted_index)
    question_list.pop(deleted_index)

    with open('Questions.txt', 'w') as fp:
        for q in question_detail_list:
            fp.write(str(q))
    insert_listbox()


def delete_question():
    """Tells user how to delete a question"""
    global edit_mode
    edit_mode = False
    toggle()
    listbox_label.config(text='Double click on the question to delete.')
    listbox_label.config(bg='yellow')
    insert_listbox()
    list_box.bind('<Double-Button-1>', delete)


def search_question():
    """Changes format of the program for searching"""
    global edit_mode, search_mode, search_entry_text
    edit_mode = False
    search_mode = True
    toggle()
    search_mode = False


def search():
    """Searches the user input through the question detail list"""
    global search_entry_text, question_detail_list, search_mode, string_detail_list
    search_mode = True
    text = search_entry_text.get()
    list_box.delete(0, END)

    matches = get_close_matches(text, string_detail_list, n=5, cutoff=0.23)

    for m in matches:
        m = m.split(",")
        new_matches = m[0]
        list_box.insert(END, new_matches)
    search_mode = False


def insert_listbox():
    """Displays questions in the listbox"""
    global question_list
    list_box.delete(0, END)
    for l in question_list:
        list_box.insert(END, l)


def toggle():
    """Changes the format of the application depending on the function selected"""
    global quiz_mode, search_mode, color, question, pts, choice1, choice2, choice3, ques, \
        choice4, correct_feedback, incorrect_feedback, correct_answer
    if search_mode:
        win.geometry('390x300')
        title_label.grid_forget()
        question_label.grid_forget()
        points_label.grid_forget()
        choice1_label.grid_forget()
        choice2_label.grid_forget()
        choice3_label.grid_forget()
        choice4_label.grid_forget()
        ca_label.grid_forget()
        cf_label.grid_forget()
        if_label.grid_forget()
        question_entry.grid_forget()
        points_entry.grid_forget()
        choice1_entry.grid_forget()
        choice2_entry.grid_forget()
        choice3_entry.grid_forget()
        choice4_entry.grid_forget()
        cfeedback_entry.grid_forget()
        ifeedback_entry.grid_forget()
        cchoice_entry.grid_forget()
        listbox_label.grid_forget()
        list_box.grid_forget()
        save_button.grid_forget()
        quiz_button.grid(row=3, column=0, pady=3, padx=5, sticky=W)
        submit_button.grid_forget()
        points_earned_label.grid_forget()
        question_count.grid_forget()
        correct_questions.grid_forget()
        answer_entry.grid_forget()
        answer_label.grid_forget()
        next_question.grid_forget()
        title_label.grid(row=0, column=0, columnspan=2, pady=2, padx=20)
        search_entry.grid(row=1, column=0, columnspan=2, pady=5, padx=20)
        list_box.grid(row=2, column=0, columnspan=2, pady=2, padx=20)
        search_button.grid(row=3, column=1, pady=3, sticky=E)
        list_box.delete(0, END)
    else:
        win.geometry('500x500')
        question.set('')
        pts.set('')
        choice1.set('')
        choice2.set('')
        choice3.set('')
        choice4.set('')
        correct_feedback.set('')
        incorrect_feedback.set('')
        correct_answer.set('')
        title_label.grid(row=0, column=1, columnspan=2)
        question_label.grid(row=1, column=0, sticky=W, pady=3, padx=3)
        points_label.grid(row=2, column=0, sticky=W, pady=3, padx=3)
        choice1_label.grid(row=3, column=0, sticky=W, pady=3, padx=3)
        choice2_label.grid(row=4, column=0, sticky=W, pady=3, padx=3)
        choice3_label.grid(row=5, column=0, sticky=W, pady=3, padx=3)
        choice4_label.grid(row=6, column=0, sticky=W, pady=3, padx=3)
        cf_label.grid(row=7, column=0, sticky=W, pady=3, padx=3)
        if_label.grid(row=8, column=0, sticky=W, pady=3, padx=3)
        ca_label.grid(row=9, column=0, sticky=W, pady=3, padx=3)
        question_entry.grid(row=1, column=2, sticky=E)
        question_entry.config(width=45)
        points_entry.grid(row=2, column=2, sticky=E)
        points_entry.config(width=45)
        choice1_entry.grid(row=3, column=2, sticky=E)
        choice1_entry.config(width=45)
        choice2_entry.grid(row=4, column=2, sticky=E)
        choice2_entry.config(width=45)
        choice3_entry.grid(row=5, column=2, sticky=E)
        choice3_entry.config(width=45)
        choice4_entry.grid(row=6, column=2, sticky=E)
        choice4_entry.config(width=45)
        cfeedback_entry.grid(row=7, column=2, sticky=E)
        cfeedback_entry.config(width=45)
        ifeedback_entry.grid(row=8, column=2, sticky=E)
        ifeedback_entry.config(width=45)
        cchoice_entry.grid(row=9, column=2, sticky=E)
        cchoice_entry.config(width=45)
        listbox_label.grid(row=10, column=1, columnspan=2, pady=3, sticky=W)
        list_box.grid(row=11, column=1, columnspan=2, sticky=E)
        save_button.grid(row=12, column=2, sticky=E, pady=5)
        quiz_button.grid(row=12, column=1, sticky=W, pady=5)
        search_entry.grid_forget()
        search_button.grid_forget()
        submit_button.grid_forget()
        points_earned_label.grid_forget()
        question_count.grid_forget()
        correct_questions.grid_forget()
        answer_entry.grid_forget()
        answer_label.grid_forget()
        next_question.grid_forget()


def start_quiz():
    """Starts the quiz game"""
    global quiz_mode, string_detail_list, question, pts, choice1, choice2, choice3, ques, \
        choice4, correct_feedback, incorrect_feedback, correct_answer, ans, count
    show_questions()

    win.geometry('580x400')
    title_label.config(text='Quiz Game')
    answer_label.grid(row=7, column=0, sticky=W, pady=3, padx=3)
    answer_entry.grid(row=7, column=2, sticky=E)
    answer_entry.config(width=55)
    cfeedback_entry.grid(row=8, column=2, sticky=E)
    ifeedback_entry.grid(row=9, column=2, sticky=E)
    cchoice_entry.grid(row=10, column=2, sticky=E)
    points_entry.config(state=NORMAL, width=55)
    question_entry.config(state=NORMAL, width=55)
    choice1_entry.config(state=NORMAL, width=55)
    choice2_entry.config(state=NORMAL, width=55)
    choice3_entry.config(state=NORMAL, width=55)
    choice4_entry.config(state=NORMAL, width=55)
    cf_label.grid_forget()
    if_label.grid_forget()
    ca_label.grid_forget()
    cfeedback_entry.grid_forget()
    ifeedback_entry.grid_forget()
    cchoice_entry.grid_forget()
    listbox_label.grid_forget()
    list_box.grid_forget()
    save_button.grid_forget()
    quiz_button.grid_forget()
    submit_button.grid(row=7, column=3, pady=3, padx=5, sticky=E)
    next_question.grid(row=1, column=3, pady=3, padx=5, sticky=E)

    ques = random.sample(string_detail_list, k=3)
    qu, pt, one, two, three, four, cf, ic, cc = ques[0].split(",")
    question.set(qu)
    pts.set(pt)
    choice1.set(one)
    choice2.set(two)
    choice3.set(three)
    choice4.set(four)
    correct_feedback.set(cf)
    incorrect_feedback.set(ic)
    correct_answer.set(cc)

    points_entry.config(state=DISABLED)
    question_entry.config(state=DISABLED)
    choice1_entry.config(state=DISABLED)
    choice2_entry.config(state=DISABLED)
    choice3_entry.config(state=DISABLED)
    choice4_entry.config(state=DISABLED)
    cfeedback_entry.config(state=DISABLED)
    ifeedback_entry.config(state=DISABLED)
    cchoice_entry.config(state=DISABLED)


def submit_click():
    """Checks if the user answer is correct"""
    global correct_feedback, incorrect_feedback, correct_answer, ans, correct_count, pts, pts_earned, \
        count, total_points
    user_answer = ans.get()
    ca = correct_answer.get()
    pt = pts.get()
    total_pts = pts.get()
    ca = ca[0:-1]
    total_points += int(total_pts)

    if user_answer.casefold() == ca.casefold():
        cf_label.grid(row=8, column=0, sticky=W, pady=3, padx=3)
        cfeedback_entry.grid(row=8, column=2, sticky=E)
        cfeedback_entry.config(width=55)
        pts_earned += int(pt)
        correct_count += 1

    else:
        if_label.grid(row=9, column=0, sticky=W, pady=3, padx=3)
        ifeedback_entry.grid(row=9, column=2, sticky=E)
        ifeedback_entry.config(width=55)
        ca_label.grid(row=10, column=0, sticky=W, pady=3, padx=3)
        cchoice_entry.grid(row=10, column=2, sticky=E)
        cchoice_entry.config(width=55)

    points_earned_label.grid(row=11, column=0, sticky=W, pady=3, padx=3)
    question_count.grid(row=12, column=0, sticky=W, pady=3, padx=3)
    correct_questions.grid(row=11, column=2, sticky=W)
    question_count.config(text='Question ' + str(count) + '/3')
    points_earned_label.config(text='Points Earned: ' + str(pts_earned) + '/' + str(total_points))
    correct_questions.config(text='Number of Correct Questions: ' + str(correct_count))
    count += 1


def next_question():
    """Shows the next question of the quiz"""
    global count, ques, question, pts, choice1, choice2, choice3, choice4, correct_feedback, incorrect_feedback, \
        correct_answer, ans
    cf_label.grid_forget()
    if_label.grid_forget()
    ca_label.grid_forget()
    cfeedback_entry.grid_forget()
    ifeedback_entry.grid_forget()
    cchoice_entry.grid_forget()
    question.set('')
    pts.set('')
    choice1.set('')
    choice2.set('')
    choice3.set('')
    choice4.set('')
    correct_feedback.set('')
    incorrect_feedback.set('')
    correct_answer.set('')
    ans.set('')

    if count == 2:
        qu, pt, one, two, three, four, cf, ic, cc = ques[1].split(",")
        question.set(qu)
        pts.set(pt)
        choice1.set(one)
        choice2.set(two)
        choice3.set(three)
        choice4.set(four)
        correct_feedback.set(cf)
        incorrect_feedback.set(ic)
        correct_answer.set(cc)
    elif count == 3:
        qu, pt, one, two, three, four, cf, ic, cc = ques[2].split(",")
        question.set(qu)
        pts.set(pt)
        choice1.set(one)
        choice2.set(two)
        choice3.set(three)
        choice4.set(four)
        correct_feedback.set(cf)
        incorrect_feedback.set(ic)
        correct_answer.set(cc)


# Build window called win
win = Tk()
win.geometry('500x500')
win.title('Quiz Management System')
win.config(bg='CadetBlue1')

# Variables
color = 'CadetBlue1'
question_list = []
question_detail_list = []
string_detail_list = []
question = StringVar()
pts = StringVar()
choice1 = StringVar()
choice2 = StringVar()
choice3 = StringVar()
choice4 = StringVar()
correct_answer = StringVar()
correct_feedback = StringVar()
incorrect_feedback = StringVar()
existing_question = StringVar()
existing_pts = StringVar()
existing_choice1 = StringVar()
existing_choice2 = StringVar()
existing_choice3 = StringVar()
existing_choice4 = StringVar()
existing_correct_feedback = StringVar()
existing_incorrect_feedback = StringVar()
existing_correct_answer = StringVar()
search_entry_text = StringVar()
ans = StringVar()
index = None
edit_mode = False
search_mode = False
quiz_mode = False
ques = []
ques1 = StringVar()
ques2 = StringVar()
ques3 = StringVar()
num = IntVar()
answer = StringVar()
count = 1
correct_count = 0
pts_earned = 0
total_points = 0

# Menu
menu_bar = Menu(win)
win.config(menu=menu_bar)
menu = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label='Questions', menu=menu)
menu.add_command(label='View', command=show_questions)
menu.add_command(label='Add', command=add_question)
menu.add_command(label='Edit', command=edit_question)
menu.add_command(label='Delete', command=delete_question)
menu.add_command(label='Search', command=search_question)

# Labels
title_label = Label(win, text='Quiz Question Management Form', bg=color, justify=CENTER)
title_label.grid(row=0, column=1, columnspan=2)
question_label = Label(win, text='Question:', bg=color)
question_label.grid(row=1, column=0, sticky=W, pady=3, padx=3)
points_label = Label(win, text='Points (1-3):', bg=color)
points_label.grid(row=2, column=0, sticky=W, pady=3, padx=3)
choice1_label = Label(win, text='Choice 1:', bg=color)
choice1_label.grid(row=3, column=0, sticky=W, pady=3, padx=3)
choice2_label = Label(win, text='Choice 2:', bg=color)
choice2_label.grid(row=4, column=0, sticky=W, pady=3, padx=3)
choice3_label = Label(win, text='Choice 3:', bg=color)
choice3_label.grid(row=5, column=0, sticky=W, pady=3, padx=3)
choice4_label = Label(win, text='Choice 4:', bg=color)
choice4_label.grid(row=6, column=0, sticky=W, pady=3, padx=3)
answer_label = Label(win, text='Your Answer: ', bg=color)
answer_label.grid(row=7, column=0, sticky=W, pady=3, padx=3)
answer_label.grid_forget()
cf_label = Label(win, text='Correct Feedback:', bg=color)
cf_label.grid(row=8, column=0, sticky=W, pady=3, padx=3)
if_label = Label(win, text='Incorrect Feedback:', bg=color)
if_label.grid(row=9, column=0, sticky=W, pady=3, padx=3)
ca_label = Label(win, text='Correct Answer:', bg=color)
ca_label.grid(row=10, column=0, sticky=W, pady=3, padx=3)

# Entries
question_entry = Entry(win, textvariable=question, width=45, state=DISABLED)
question_entry.grid(row=1, column=2, sticky=E)
points_entry = Entry(win, textvariable=pts, width=45, state=DISABLED)
points_entry.grid(row=2, column=2, sticky=E)
choice1_entry = Entry(win, textvariable=choice1, width=45, state=DISABLED)
choice1_entry.grid(row=3, column=2, sticky=E)
choice2_entry = Entry(win, textvariable=choice2, width=45, state=DISABLED)
choice2_entry.grid(row=4, column=2, sticky=E)
choice3_entry = Entry(win, textvariable=choice3, width=45, state=DISABLED)
choice3_entry.grid(row=5, column=2, sticky=E)
choice4_entry = Entry(win, textvariable=choice4, width=45, state=DISABLED)
choice4_entry.grid(row=6, column=2, sticky=E)
answer_entry = Entry(win, textvariable=ans, width=45)
answer_entry.grid(row=7, column=2, sticky=E)
answer_entry.grid_forget()
cfeedback_entry = Entry(win, textvariable=correct_feedback, width=45, state=DISABLED)
cfeedback_entry.grid(row=8, column=2, sticky=E)
ifeedback_entry = Entry(win, textvariable=incorrect_feedback, width=45, state=DISABLED)
ifeedback_entry.grid(row=9, column=2, sticky=E)
cchoice_entry = Entry(win, textvariable=correct_answer, width=45, state=DISABLED)
cchoice_entry.grid(row=10, column=2, sticky=E)

points_earned_label = Label(win, bg=color)
points_earned_label.grid(row=11, column=0, sticky=W)
points_earned_label.grid_forget()
question_count = Label(win, bg=color)
question_count.grid(row=11, column=1, sticky=W)
question_count.grid_forget()
correct_questions = Label(win, bg=color)
correct_questions.grid(row=11, column=2, sticky=W)
correct_questions.grid_forget()

# Search Entry
search_entry = Entry(win, textvariable=search_entry_text, width=45)
search_entry.grid(row=1, column=0, columnspan=2)
search_entry.grid_forget()

# Listbox Label
listbox_label = Label(win, text='Quiz Questions', bg=color)
listbox_label.grid(row=11, column=1, columnspan=2, pady=3, sticky=W)

# Listbox
list_box = Listbox(win, width=55)
list_box.grid(row=12, column=1, columnspan=2, sticky=E)
list_box.bind('<Double-Button-1>', list_click)

# Save button
save_button = Button(win, command=save_click, text='Save Question')
save_button.grid(row=13, column=2, sticky=E, pady=5)

# Quiz button
quiz_button = Button(win, command=start_quiz, text='Take Quiz')
quiz_button.grid(row=13, column=1, sticky=W, pady=5)

# Search button
search_button = Button(win, command=search, text='Search')
search_button.grid(row=13, column=2, sticky=E, pady=5)
search_button.grid_forget()

# Submit button
submit_button = Button(win, text='Submit', command=submit_click)
submit_button.grid(row=13, column=2, pady=5)
submit_button.grid_forget()

# Next Question Button
next_question = Button(win, text='Next Question', command=next_question)
next_question.grid(row=13, column=2, pady=5)
next_question.grid_forget()

questions = get_questions('Questions.txt')
for ques in questions:
    (existing_question, existing_pts, existing_choice1, existing_choice2, existing_choice3, existing_choice4,
     existing_correct_feedback, existing_incorrect_feedback, existing_correct_answer) = ques.split(',')
    question_list.append(existing_question)
    q = Question(existing_question, existing_pts, existing_choice1, existing_choice2, existing_choice3,
                 existing_choice4, existing_correct_feedback, existing_incorrect_feedback, existing_correct_answer)
    question_detail_list.append(q)
for q in question_detail_list:
    q = str(q)
    string_detail_list.append(q)

win.mainloop()
