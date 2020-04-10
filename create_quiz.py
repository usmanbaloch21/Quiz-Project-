from tkinter import *
from tkinter import messagebox
import sqlite3
import os

def create_quiz(window, quiz_type):

    btn_background = "green"
    btn_font = ("Gill Sans", 14, "bold")
    cbutton_font = ("Gill Sans", 12, "bold")
    lbl_font = ("Gill Sans", 14, "bold")
    title_font = ("Gill Sans", 26, "bold")



    def get_checkbuttons_and_vars(questions_table):
        questions_db = sqlite3.connect("questions.db")
        c = questions_db.cursor()

        # get number of questions in mcq table
        c.execute("SELECT COUNT(*) FROM " + questions_table)
        no_of_qs = c.fetchone()[0]
        print(no_of_qs)

        # get all questions from mcq table
        c.execute("SELECT QUESTION, oid, theme1, theme2 FROM " + questions_table)
        questions_list = c.fetchall()
        questions_db.commit()
        c.close()

        vars_list = []
        checkbuttons_list = []

        for i in range(len(questions_list)):
            var = IntVar()
            vars_list.append(var)
            question_text = questions_list[i][0]
            cbutton = Checkbutton(window, text=question_text, variable = var, background="#ffffff", font=cbutton_font)
            checkbuttons_list.append(cbutton)

        return checkbuttons_list, vars_list, questions_list

    def create_quiz_table(quiz_table):

        # connect to quiz database (or create if doesn't yet exist)
        quiz_db = sqlite3.connect('quizzes.db')

        if quiz_table == "mc_quiz":
            try: # if table does not exist, create it
                c = quiz_db.cursor()
                c.execute("CREATE TABLE " + quiz_table + " (\
                            question TEXT,\
                            option1 TEXT,\
                            option2 TEXT,\
                            option3 TEXT,\
                            answer TEXT,\
                            theme1 TEXT,\
                            theme2 TEXT)")
                quiz_db.commit()
                c.close()

            except sqlite3.OperationalError:  # if table does exist, clear it
                print("This table already exists.")
                return
        elif quiz_table == "tf_quiz":

            try:  # if table does not exist, create it
                c = quiz_db.cursor()
                c.execute("CREATE TABLE " + quiz_table + " (\
                            question TEXT,\
                            answer TEXT,\
                            theme1 TEXT,\
                            theme2 TEXT)")
                quiz_db.commit()
                c.close()

            except sqlite3.OperationalError:  # if table does exist, clear it
                print("This table already exists.")
                return

    def get_selected_questions(vars_list, questions_list, questions_table):

        selected_qs_idxs = []

        for i in range(len(vars_list)):
            if vars_list[i].get() == 1: # if the question was selected
                selected_qs_idxs.append(questions_list[i][1]) # add the question id to the list

        if len(selected_qs_idxs) != 5: # error check that 5 questions have been selected
            messagebox.showerror("Error", "Please select 5 questions")
            return

        # at this point, 5 questions have been selected
        # get the 5 questions from the questions table as a list

        quiz_questions = []

        db = sqlite3.connect("questions.db")
        c = db.cursor()

        for i in range(5):
            c.execute("SELECT * FROM " + questions_table + " WHERE oid = {}".format(selected_qs_idxs[i]))
            question = c.fetchone()
            quiz_questions.append(question)
        db.commit()
        c.close()

        return quiz_questions

    def populate_quiz_table(vars_list, questions_list, questions_table, quiz_table, window):

        # Clear quiz table
        quiz_db = sqlite3.connect("quizzes.db")
        c = quiz_db.cursor()
        c.execute("DELETE FROM " + quiz_table)
        quiz_db.commit()
        c.close()

        quiz_questions = get_selected_questions(vars_list, questions_list, questions_table)

        for question in quiz_questions:
            quiz_db = sqlite3.connect("quizzes.db")
            c = quiz_db.cursor()
            if quiz_table == "mc_quiz":
                c.execute("INSERT INTO " + quiz_table + " VALUES (:question, :option1, :option2, :option3, :answer, :theme1, :theme2)",
                          {
                              'question': question[0],
                              'option1': question[1],
                              'option2': question[2],
                              'option3': question[3],
                              'answer': question[4],
                              'theme1': question[5],
                              'theme2': question[6]
                          })
            elif quiz_table == "tf_quiz":
                c.execute("INSERT INTO " + quiz_table + " VALUES (:question, :answer, :theme1, :theme2)",
                          {
                              'question': question[0],
                              'answer': question[1],
                              'theme1': question[2],
                              'theme2': question[3]
                          })
            quiz_db.commit()
            c.close()


        confirm_message = messagebox.showinfo("Success", "Quiz created successfully! \
                                                         \nYou can now undertake this quiz by returning to the homepage and clicking the Start Quiz button.", parent=window)
        window.destroy()

    # FUNCTION SETUP/ GET VARIABLES NEEDED -------------------------------------------------

    # Each time a new quiz is created, need to delete existing results files for previous quizzes of that type,
    # because the stats module does not know the difference between the 2 quizzes

    if quiz_type == "mcq":
        questions_table = "mcq"
        quiz_table = "mc_quiz"
        title_text = "Create a Multiple Choice Quiz"
        try:
            os.remove('mcq_results.dat') # delete previous results
        except:
            FileNotFoundError
    elif quiz_type == "true_or_false":
        questions_table = "tfq"
        quiz_table = "tf_quiz"
        title_text = "Create a True or False Quiz"
        try:
            os.remove('true_false_results.dat')  # delete previous results
        except:
            FileNotFoundError

    create_quiz_table(quiz_table)

    checkbuttons_list, vars_list, questions_list = get_checkbuttons_and_vars(questions_table)

    # WINDOW LAYOUT --------------------------------------------------------

    title_lbl = Label(window, background="#ffffff", font=title_font, text=title_text)
    title_lbl.pack(pady=20)

    info_lbl = Label(window, background="#ffffff", font=lbl_font, text="Select 5 questions from the list below to have in your quiz.\n When you are happy wth your choice, click Create Quiz. \n Please note: this will overwrite any existing version of the quiz.")
    info_lbl.pack(pady=(0, 10))

    for i in range(len(checkbuttons_list)):
        checkbuttons_list[i].pack(pady=(3))

    btn = Button(window, text='Create Quiz', background=btn_background, font=btn_font, command=lambda : populate_quiz_table(vars_list, questions_list, questions_table, quiz_table, window))
    btn.pack(pady=(10, 0))



# root = Tk()
# root.title("Quizardry")
# root.geometry("700x600")
# root.config(background="#ffffff")
# root.resizable(0, 0)
# create_quiz(root, "mcq")
# mainloop()






