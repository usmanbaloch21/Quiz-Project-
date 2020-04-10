"""
Quick explanation of the code:
1) Run save_qs_and_as.py to generate the files "mcq_questions.dat", "mcq_answers.dat", "true_false_questions.dat" and "true_false_answers.dat"
   containing the questions and the answers to the questions. In the final version, this file will be created by the "populate quiz with questions"
   use case(Chen's code).
2) Then run quiz.py to run the actual quiz. The code won't run if the files "mcq_questions.dat" and "mcq_answers.dat" or"true_false_questions.dat" and
   "true_false_answers.dat" aren't present in the working directory. When the restart function runs in the quiz, a file "mcq_results.dat" is
   created in the working directory which contains the results for that attempt at the quiz.
3) statistics.py needs the files "mcq_results.dat" and "mcq_questions.dat" to be present in the working directory
   before it can be run.
"""
import pickle
import random
import sqlite3
from tkinter import *
from tkinter import messagebox


# a function containing the whole code so it can be imported as a module and called from the homepage
def run_quiz(window, quiz_type):
    # format the window
    # change the title depending on the quiz type
    if quiz_type == "mcq":
        window.title("Multiple Choice Quiz")
        quiz_table = "mc_quiz"
    elif quiz_type == "true_or_false":
        window.title("True or False Quiz")
        quiz_table = "tf_quiz"

    window.geometry("700x600")
    window.config(background="#ffffff")
    window.resizable(0, 0)

    # global variables
    global questions_list
    global answers_list
    global num_of_answers_per_question
    global answers_random_orders
    global answers_list_display
    global radio_buttons_list
    global score_list
    global user_selection
    global index_list
    global q_no
    global score

    questions_list = []  # to hold questions when loaded in from binary file mcq_questions.dat
    answers_list = []  # choices of answers. correct answer is at index 0 every time. also loaded in from binary file mcq_questions.dat
    num_of_answers_per_question = 0  # to allow the code to handle either 2 answers for true or false, or 4 answers for mcq
    answers_random_orders = []  # to hold the randomised orders in which the answers will be displayed
    answers_list_display = []  # to hold the answers in the randomised order in which they will be displayed
    radio_buttons_list = []  # to hold the radio buttons that display the answers for each question
    score_list = []  # to hold the score for each question asked in the quiz, 0 if it is answered incorrectly and 1 if it is answered correctly
    user_selection = []  # to hold the indexes of the answers for the quiz, eg if option 1(0), 2(1), 3(2) or 4(3) was chosen for each question
    index_list = []  # needed to display the questions in a random order
    q_no = 1  # number of question that the quiz is showing currently
    score = 0

    # --- FUNCTIONS ------------------------------------------------------------------------------

    # # function to load the questions in from an external binary file. They will be in the form of a list [q1, q2, q3, q4, q5]
    # def get_questions(filename):
    #     global questions_list
    #     try:
    #         f = open(filename, "rb")
    #     except FileNotFoundError:
    #         messagebox.showerror(title="Error", message="Questions not found - make sure you have created the quiz!", parent=window)
    #         return
    #     f = open(filename, "rb")
    #     questions_list=pickle.load(f)
    #     f.close()
    #     print(questions_list)##
    #
    # # function to load the answers in from an external binary file. They will be in the form of a nested list [[q1a1, q1a2, q1a3, q1a4], [q2a1, q2a2...]]
    # def get_answers(filename):
    #     global answers_list
    #     f = open(filename, "rb")
    #     try:
    #         answers_list = pickle.load(f)
    #     except EOFError:
    #         messagebox.showerror(window, "No questions selected!", parent=window)
    #     f.close()
    #     print(answers_list)

    # function to load the answers in from an external database
    def get_questions_and_answers(quiz_type):
        global questions_list
        global answers_list
        if quiz_type == "mcq":
            try:
                db = sqlite3.connect('quizzes.db')
                c = db.cursor()
                c.execute("SELECT question, answer, option1, option2, option3 FROM mc_quiz")
                all_questions = c.fetchall()
                for question in all_questions:
                    questions_list.append(question[0])
                    answers_list.append([question[1], question[2], question[3], question[4]])
                db.commit()
                c.close()

            except sqlite3.OperationalError:
                messagebox.showerror(title="Error",
                                     message="Questions not found - make sure you have created the quiz!",
                                     parent=window)
                return

        elif quiz_type == "true_or_false":
            try:
                db = sqlite3.connect('quizzes.db')
                c = db.cursor()
                c.execute("SELECT question, answer FROM tf_quiz")
                all_questions = c.fetchall()
                for question in all_questions:
                    questions_list.append(question[0])
                    option2 = "True"
                    if question[1] == "True":
                        option2 = "False"
                    answers_list.append([question[1], option2])

                db.commit()
                c.close()

            except sqlite3.OperationalError:
                messagebox.showerror(title="Error",
                                     message="Questions not found - make sure you have created the quiz!",
                                     parent=window)
                return

    # function creating the the randomised orders in which the answers will be displayed for each question
    def create_answers_list_display():
        global answers_random_orders
        global num_of_answers_per_question
        num_of_answers_per_question = len(answers_list[0])
        sample_range = [i for i in range(num_of_answers_per_question)]
        # generate the random orders
        answers_random_orders = [
            random.sample(sample_range, k=num_of_answers_per_question),
            random.sample(sample_range, k=num_of_answers_per_question),
            random.sample(sample_range, k=num_of_answers_per_question),
            random.sample(sample_range, k=num_of_answers_per_question),
            random.sample(sample_range, k=num_of_answers_per_question)
        ]
        # put the answers into the generated random orders for
        global answers_list_display
        for i in range(len(answers_list)):
            answers_display = [answers_list[i][j] for j in answers_random_orders[i]]
            answers_list_display.append(answers_display)

    # function to save the current response data to the binary file mcq_results.dat and restart the quiz
    def restart():
        global q_no
        global user_selection
        global score_list
        global score
        global radio_buttons_list

        response = messagebox.askyesno("Confirm Restart", "Are you sure you want to restart the quiz?", parent=window)
        if response == 1:
            calculate()
            # print("RESULTS: score: {}, user selections: {}, q_no: {}".format(score, user_selection, q_no))
            responses = []
            for i in range(q_no - 1):  # ie for i in range(num of questions)
                responses.append([index_list[i], score_list[i]])
            responses.append(q_no)
            # eg responses = [[3, 1], [0, 1], [4, 1], [1, 1], [2, 1], 5]
            # save responses to results file
            if num_of_answers_per_question == 2:  # if it is a true or false quiz
                f = open("true_false_results.dat", "ab")
                pickle.dump(responses, f)
                f.close()
            elif num_of_answers_per_question == 4:  # if it is a multiple choice quiz
                f = open("mcq_results.dat", "ab")
                pickle.dump(responses, f)
                f.close()

            # clear the page
            for widget in window.winfo_children():
                widget.pack_forget()

            # reset the global variables
            q_no = 1
            user_selection = []
            score = 0
            score_list = []
            radio_buttons_list = []

            # go to the start page of the quiz
            load_start_page()

    def showresult(score):
        # clear all the questions and the radio buttons (pack_forget instead of destroy so they can be used again when the quiz is reset)
        label_questions.pack_forget()
        for button in radio_buttons_list:
            button.pack_forget()

        label_image = Label(window, background="#ffffff")
        label_image.pack(pady=20)
        label_score = Label(window, text="Score: {}/5".format(score), font=("Curlz MT", 22, "bold"),
                            background="#ffffff")
        label_score.pack()
        label_result = Label(window, font=("Curlz MT", 22, "bold"), background="#ffffff")
        label_result.pack()

        if score >= 4:  # ie 4 or 5
            img = PhotoImage(file="images/great.png")
            label_image.configure(image=img)
            label_image.image = img
            label_result.configure(text="Congratulations you're smart enough \n to summon dragons - great job!")
        elif (score >= 2 and score < 4):  # ie 2 or 3
            img = PhotoImage(file="images/ok.png")
            label_image.configure(image=img)
            label_image.image = img
            label_result.configure(
                text="You're good with room to improve - \n you can summon dragons \n if you work harder!")
        else:  # ie 0 or 1
            img = PhotoImage(file="images/bad.png")
            label_image.configure(image=img)
            label_image.image = img
            label_result.configure(text="You should focus more \n to become a great wizard!")

    # function to calculate the score
    def calculate():
        global score
        score = sum(score_list)
        print("score = {}".format(score))

    # function to define the selected option and change question after answer has been picked
    def select():
        global radio_var
        global user_selection
        global label_questions
        global score_list
        global q_no
        # global r_1
        # global r_2
        # global r_3
        # global r_4
        # get selected value
        selected_value = radio_var.get()
        # 1) convert selected value back to original idx (according to original answers list)
        selected_value = answers_random_orders[index_list[q_no - 1]][selected_value]
        # 2) add the converted selected value to the user_selection array
        user_selection.append(selected_value)
        # 3) check if answer is correct and add score to score_list (0 if incorrect, 1 if correct)
        if selected_value == 0:
            score_list.append(1)
            messagebox.showinfo("Feedback",
                                "Well done!\nThe correct answer is {}".format(answers_list[index_list[q_no - 1]][0]),
                                parent=window)
        else:
            score_list.append(0)
            messagebox.showinfo("Feedback",
                                "Not quite!\nThe correct answer is {}".format(answers_list[index_list[q_no - 1]][0]),
                                parent=window)
        radio_var.set(-1)
        if q_no < 5:  # if there are questions left in the quiz, display the next question
            label_questions.config(text=questions_list[index_list[q_no]])

            for i in range(len(radio_buttons_list)):
                radio_buttons_list[i]["text"] = answers_list_display[index_list[q_no]][i]
            # r_1["text"] = answers_list_display[index_list[q_no]][0]
            # r_2["text"] = answers_list_display[index_list[q_no]][1]
            # r_3["text"] = answers_list_display[index_list[q_no]][2]
            # r_4["text"] = answers_list_display[index_list[q_no]][3]
            q_no += 1
        else:
            print("Index list = {}".format(index_list))
            print("User selection = {}".format(user_selection))
            q_no += 1  # still increment this here to differentate betweenthe quiz being completed vs being restarted on the 5th question
            calculate()
            showresult(score)

    def create_radio_buttons():
        global radio_buttons_list
        for i in range(num_of_answers_per_question):  # ie 2 if true/false, 5 if mcq
            radio_buttons_list.append(
                Radiobutton(window, text=answers_list_display[index_list[0]][i], font=("Curlz MT", 16, "bold"), value=i,
                            variable=radio_var, command=select, background="#ffffff"))

    # function to initiate quiz
    def quiz_begins():
        global label_questions
        label_questions = Label(window, text=questions_list[index_list[0]], font=("Curlz MT", 18, "bold"), width=500,
                                justify="center", wraplength=400, background="#ffffff")
        label_questions.pack(pady=(80, 40))

        global radio_var
        radio_var = IntVar()
        radio_var.set(-1)

        global radio_buttons_list
        for i in range(num_of_answers_per_question):  # ie 2 if true/false, 5 if mcq
            radio_buttons_list.append(
                Radiobutton(window, text=answers_list_display[index_list[0]][i], font=("Curlz MT", 16, "bold"), value=i,
                            variable=radio_var, command=select, background="#ffffff"))

        for radio_button in radio_buttons_list:
            radio_button.pack(pady=10)

        bottom_frame.pack(side=BOTTOM, pady="40px")
        btn_restart.grid(row=0, column=1,
                         padx="60px")  # pady stops the button being aligned with the very bottom of the window

    # random generator function to display questions in random order, populates index_list
    def gen():
        global index_list
        index_list = random.sample([0, 1, 2, 3, 4], k=5)
        print(index_list)

    # function to forget when start button pressed and start the quiz
    def start():
        lbl_wand_img.pack_forget()
        lbl_title.pack_forget()
        btn_start.pack_forget()
        lbl_info_header.pack_forget()
        lbl_info_detail.pack_forget()
        gen()
        quiz_begins()

    def load_start_page():
        lbl_wand_img.pack()
        lbl_title.pack()
        btn_start.pack(pady=(20, 0))
        lbl_info_header.pack(pady=(10, 0))
        lbl_info_detail.pack()



    # --- Define labels, buttons and images ---------------------------------------------------------------------------

    global img_wand  # so that the image can be accessed in the load_start_page function
    img_wand = PhotoImage(file="images/wand1.png")
    lbl_wand_img = Label(window, image=img_wand, background="#ffffff")

    lbl_title = Label(window, text="Quizardry", font=("Curlz MT", 26, "bold"), background="#ffffff")

    btn_start = Button(window, text="START QUIZ", font=("Curlz MT", 20, "bold"), background="green", command=start)

    lbl_info_header = Label(window, text="Quiz Information:", background="#ffffff", justify="center",
                            font=("Gill Sans", 12, "bold"))

    quiz_info_text = "This Quiz consists of 5 questions. \n" \
                     "If you answer all of the questions right you're a great wizard! \n" \
                     "Clicking on an answer will submit it as your final answer, \n" \
                     "so make sure you are certain before you click! \n" \
                     "You can restart the quiz at any point. \n" \
                     "Make sure to click restart once you have finished to save your results. \n" \
                     "Click the start button when you're ready. \n" \
                     "GOOD LUCK! "

    lbl_info_detail = Label(window,
                            text=quiz_info_text,
                            width=100, font=("Gill Sans", 11, "bold"), background="#ffffff")

    # added to keep the restart button aligned to the bottom of the screen
    bottom_frame = Frame(window, background="#ffffff")

    btn_restart = Button(bottom_frame, text="RESTART", font=("Gill Sans", 20, "bold"), background="green",
                         command=restart)

    # --- MAIN -------------------------------------------------------------------------------------------------

    get_questions_and_answers(quiz_type)
    # print(questions_list)
    # print(answers_list)
    create_answers_list_display()
    load_start_page()
    # window.mainloop()

# root = Tk()
# run_quiz(root, "mcq")
