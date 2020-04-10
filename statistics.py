
from tkinter import *
from tkinter import messagebox
from matplotlib import pyplot as plt
import sqlite3


def display_statistics(window, results_filename, quiz_table):

    window.title("Statistics")
    window.geometry("700x600")
    window.config(background="#ffffff")
    window.resizable(0, 0)

    import pickle

    # # get questions from binary file (before database were utilised
    # try: # error check file exists
    #
    #     f = open(questions_filename, "rb")
    # except FileNotFoundError:
    #     messagebox.showerror(title="Error", message="Questions file not found - quiz has not been created yet")
    #     return
    # # if file exists:
    # f = open(questions_filename, "rb")
    # questions = pickle.load(f)
    # f.close()
    # print(questions)


    # get questions from quizzes database
    try:
        db = sqlite3.connect('quizzes.db')
        c = db.cursor()
        c.execute("SELECT question FROM " + quiz_table)
        questions = c.fetchall()
        db.commit()
        c.close()

    except sqlite3.OperationalError:
        messagebox.showerror(title="Error", message="Questions not found - make sure you have created the quiz!",
                             parent=window)
        return




    # get results
    results = []

    # error check file exists
    try:
        f = open(results_filename, "rb")
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="Results file not found - no results have been saved yet.")
        return

    # if file exists:
    f = open(results_filename, "rb")
    while True:
        try:
            result = pickle.load(f)
            results.append(result)
        except EOFError: # reached end of results file
            break
    f.close()
    print(results)

    #variables needed for statistics:

    Q1_total_answers = 0
    Q1_total_correct_answers = 0
    Q1_total_resets = 0
    Q1_perc_correct = 0

    Q2_total_answers = 0
    Q2_total_correct_answers = 0
    Q2_total_resets = 0
    Q2_perc_correct = 0

    Q3_total_answers = 0
    Q3_total_correct_answers = 0
    Q3_total_resets = 0
    Q3_perc_correct = 0

    Q4_total_answers = 0
    Q4_total_correct_answers = 0
    Q4_total_resets = 0
    Q4_perc_correct = 0

    Q5_total_answers = 0
    Q5_total_correct_answers = 0
    Q5_total_resets = 0
    Q5_perc_correct = 0

    times_quiz_completed = 0

    # populate the variables from the results list
    # each response is in the format [question index, score] for each question answered, then the last number is the
    # question that was being displayed when the quiz was reset.
    # eg [[3, 1], [0, 1], [4, 1], [1, 1], [2, 1], 6] - quiz completed
    # eg [[2, 1], [5, 1], 3] - quiz reset on the third question.
    for result in results:
        for i in range(len(result)-1):
            if result[i][0] == 0: # if q1
                Q1_total_answers+= 1
                Q1_total_correct_answers += result[i][1]
            elif result[i][0] == 1: # if q2
                Q2_total_answers+= 1
                Q2_total_correct_answers += result[i][1]
            elif result[i][0] == 2: # if q3
                Q3_total_answers+= 1
                Q3_total_correct_answers += result[i][1]
            elif result[i][0] == 3: # if q4
                Q4_total_answers+= 1
                Q4_total_correct_answers += result[i][1]
            elif result[i][0] == 4: # if q5
                Q5_total_answers+= 1
                Q5_total_correct_answers += result[i][1]

        if result[-1] == 1:
            Q1_total_resets += 1
        elif result[-1] == 2:
            Q2_total_resets += 1
        elif result[-1] == 3:
            Q3_total_resets += 1
        elif result[-1] == 4:
            Q4_total_resets += 1
        elif result[-1] == 5:
            Q5_total_resets += 1
        else:
            times_quiz_completed += 1


    # calculate % correct answers for each question

    if ((Q1_total_answers != 0) and (Q1_total_correct_answers != 0)):
        Q1_perc_correct = Q1_total_correct_answers/Q1_total_answers*100
    if ((Q2_total_answers != 0) and (Q2_total_correct_answers != 0)):
        Q2_perc_correct = Q2_total_correct_answers/Q2_total_answers*100
    if ((Q3_total_answers != 0) and (Q3_total_correct_answers != 0)):
        Q3_perc_correct = Q3_total_correct_answers/Q3_total_answers*100
    if ((Q4_total_answers != 0) and (Q4_total_correct_answers != 0)):
        Q4_perc_correct = Q4_total_correct_answers/Q4_total_answers*100
    if ((Q5_total_answers != 0) and (Q5_total_correct_answers != 0)):
        Q5_perc_correct = Q5_total_correct_answers/Q5_total_answers*100

    # work out question(s) with highest % correct answers
    highest_perc_qs = []
    perc_list = [Q1_perc_correct, Q2_perc_correct, Q3_perc_correct, Q4_perc_correct, Q5_perc_correct]
    highest_perc_correct = (max(perc_list))
    for i in range(len(perc_list)):
        if perc_list[i] == highest_perc_correct:
            highest_perc_qs.append("Q" + str(i+1))

    # work out question(s) with lowest % correct answers
    lowest_perc_qs = []
    lowest_perc_correct = (min(perc_list))
    for i in range(len(perc_list)):
        if perc_list[i] == lowest_perc_correct:
            lowest_perc_qs.append("Q" + str(i + 1))

    # work out question(s) most often given up on
    most_restarts = []
    restart_list = [Q1_total_resets, Q2_total_resets, Q3_total_resets, Q4_total_resets, Q5_total_resets]
    highest_restarts = (max(restart_list))
    if highest_restarts != 0:
        for i in range(len(restart_list)):
            if restart_list[i] == highest_restarts:
                most_restarts.append("Q" + str(i + 1))
    else:
        most_restarts.append("N/A")

    # display results in text box

    # first, set up textbox and configure tags for normal and bold font
    txtDisplay = Text(window, height=22, width=85)
    txtDisplay.tag_configure('boldfont', font=('Gill Sans', 11, 'bold'))
    txtDisplay.tag_configure('normfont', font=('Gill Sans', 11))
    txtDisplay.insert(END, "Questions: \n",'boldfont')
    txtDisplay.insert(END, "1) " + questions[0][0] + "\n", 'normfont')
    txtDisplay.insert(END, "2) " + questions[1][0] + "\n", 'normfont')
    txtDisplay.insert(END, "3) " + questions[2][0] + "\n", 'normfont')
    txtDisplay.insert(END, "4) " + questions[3][0] + "\n", 'normfont')
    txtDisplay.insert(END, "5) " + questions[4][0] + "\n", 'normfont')
    txtDisplay.insert(END, "\t \t \t \t \t \n", 'normfont')
    txtDisplay.insert(END, "\t \t \t \t \t Q1 \t Q2 \t Q3 \t Q4 \t Q5\n", 'boldfont')
    txtDisplay.insert(END, "Total number of times answered:\t \t \t \t \t " + str(Q1_total_answers) + " \t" + str(Q2_total_answers) + " \t" + str(Q3_total_answers) + "\t" + str(Q4_total_answers) + "\t" + str(Q5_total_answers) + "\n", 'normfont')
    txtDisplay.insert(END, "Total number of correct answers:\t \t \t \t \t " + str(Q1_total_correct_answers) + " \t" + str(
        Q2_total_correct_answers) + " \t" + str(Q3_total_correct_answers) + "\t" + str(Q4_total_correct_answers) + "\t" + str(Q5_total_correct_answers) + "\n", 'normfont')
    txtDisplay.insert(END,
                      "% of correct answers:\t \t \t \t \t " + str(round(Q1_perc_correct,2)) + " \t" + str(
                          round(Q2_perc_correct, 2)) + " \t" + str(round(Q3_perc_correct,2)) + "\t" + str(
                          round(Q4_perc_correct,2)) + "\t" + str(round(Q5_perc_correct,2)) + "\n", 'normfont')
    txtDisplay.insert(END,
                      "No of times question given up on:\t \t \t \t \t " + str(Q1_total_resets) + " \t" + str(
                          Q2_total_resets) + " \t" + str(Q3_total_resets) + "\t" + str(
                          Q4_total_resets) + "\t" + str(Q5_total_resets) + "\n", 'normfont')
    txtDisplay.insert(END, "\n", 'normfont')
    txtDisplay.insert(END, "\n", 'normfont')
    txtDisplay.insert(END, "Highlights\n", 'boldfont')
    txtDisplay.insert(END, "Question(s) with highest % correct answers: " + str(highest_perc_qs) + "\n", 'normfont')
    txtDisplay.insert(END, "Question(s) with lowest % correct answers: " + str(lowest_perc_qs) + "\n",
                      'normfont')
    txtDisplay.insert(END, "Question(s) most often given up on: " + str(most_restarts) + "\n", 'normfont')
    txtDisplay.insert(END, "Number of times quiz attempted: " + str(len(results)) + "\n", 'normfont')
    txtDisplay.insert(END, "Number of times quiz completed: " + str(times_quiz_completed) + "\n", 'normfont')

    # MAKE THE GRAPH --------------------------------------------------------------------------------------

    x = ["Q1", "Q2", "Q3", "Q4", "Q5"]
    y = perc_list

    plt.bar(x, y, color="green")
    plt.title("% of Correct Answers for Each Question")
    plt.xlabel("Question")
    plt.ylabel("% Correct Answers")
    plt.ylim(0, 105)
    plt.yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
    plt.gcf().canvas.set_window_title("Question Statistics - Graph")

    # DOWNLOAD STATISTICS REPORT -------------------------------------------------------------------------

    def download_stats_report():

        report_txt = txtDisplay.get('1.0', 'end')
        report_list = report_txt.split("\n")
        report_list[6] = report_list[6][0] + "\t" + "\t" + report_list[6][1:]
        report_list[8] = report_list[8][:33] + report_list[8][-11:]
        report_list[9] = report_list[9][:34] + report_list[9][-11:]
        report_list[10] = report_list[10][:23] +  report_list[10][-30:]
        report_list[11] = report_list[11][:33] + "\t " + report_list[11][-11:]


        with open("Statistics_Report.txt", "w") as txt_file:
            for line in report_list:
                txt_file.write(line + "\n")

    # WINDOW LAYOUT --------------------------------------------------------------------
    label_text = Label(window, text="Statistics", font=("Gill Sans", 26, "bold"), background="#ffffff")
    label_text.pack(pady=(20, 0))

    txtDisplay.pack(pady="20px")

    btn_stats = Button(window, text="Download Statistics Report", font=("Gill Sans", 16, "bold"), background="green",
                       command=download_stats_report)
    btn_stats.pack()

    plt.show()



# #Main
# root= Tk()
# root.title("Quizadry")
# root.geometry("700x600")
# root.config(background="#ffffff")
# root.resizable(0, 0)
#
# btn= Button(root, text="show statistics for quiz 1", command = lambda : display_statistics(root, "mcq_results.dat", "mc_quiz"))
# btn.pack()
# root.mainloop()