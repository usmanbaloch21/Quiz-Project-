import tkinter
from tkinter import *
import tkinter.scrolledtext as ScTxt
from tkinter import messagebox
import sqlite3
import os

def enter_mc(window):
    global q_entry
    global op1_entry
    global op2_entry
    global op3_entry
    global ans_entry
    global th1_entry
    global th2_entry
    global q_list
    global id_entry
    # root = tkinter.Tk()
    # root.title("Multiple Choice")
    # root.geometry("700x600")
    # root.config(background="#ffffff")
    # root.resizable(0,0)

    def createDB(dbase):
        needcreate = not os.path.exists(dbase)
        conn = sqlite3.connect(dbase)
        if needcreate:
            c= conn.cursor()

            c.execute("""CREATE TABLE mcq (
                question TEXT,
                option1 TEXT,
                option2 TEXT,
                option3 TEXT,
                answer TEXT,
                theme1 TEXT,
                theme2 TEXT
            )""")

            c.execute(""" CREATE TABLE tfq (
                question TEXT,
                answer TEXT,
                theme1 TEXT,
                theme2 TEXT
            )""")

            conn.commit()
            c.close()
            return conn

    def edit():
        global editor1
        global q_entry_edit
        global op1_entry_edit
        global op2_entry_edit
        global op3_entry_edit
        global ans_entry_edit
        global th1_entry_edit
        global th2_entry_edit

        # Check 1) - has ID been entered
        if id_entry.get() == "":
            messagebox.showerror("Warning", "Please enter the Question ID")

        else:
            conn = sqlite3.connect("questions.db")
            c = conn.cursor()
            # Check 2) - Does ID exist in the table
            ##########################################################################
            c.execute("SELECT COUNT (*) FROM mcq WHERE oid = " + id_entry.get())
            id_present = c.fetchone()[0]  # get the number of records with the specified ID.

            if id_present == 0:  # if there no record with the ID
                id_error = messagebox.showerror("Error", "No question with that ID found in the table.")
                return

            else:
                editor1 = Tk()
                editor1.title("Update a Question")
                editor1.geometry("400x400")
                editor1.config(background="#ffffff")
                c.execute("SELECT * FROM mcq WHERE oid = " + id_entry.get())
                records = c.fetchall()

                q_lbl_edit = Label(editor1, text="Question", background="#ffffff", font=("Gill Sans", 12))
                q_lbl_edit.grid(row=0, column=0, padx=20, pady=(10, 5))
                q_entry_edit = Entry(editor1, width=30)
                q_entry_edit.grid(row=0, column=1, pady=(10, 5))

                op1_lbl_edit = Label(editor1, text="Option 1", background="#ffffff", font=("Gill Sans", 12))
                op1_lbl_edit.grid(row=1, column=0, padx=20, pady=5)
                op1_entry_edit = Entry(editor1, width=30)
                op1_entry_edit.grid(row=1, column=1, pady=5)

                op2_lbl_edit = Label(editor1, text="Option 2", background="#ffffff", font=("Gill Sans", 12))
                op2_lbl_edit.grid(row=2, column=0, padx=20, pady=5)
                op2_entry_edit = Entry(editor1, width=30)
                op2_entry_edit.grid(row=2, column=1, pady=5)

                op3_lbl_edit = Label(editor1, text="Option 3", background="#ffffff", font=("Gill Sans", 12))
                op3_lbl_edit.grid(row=3, column=0, padx=20, pady=5)
                op3_entry_edit = Entry(editor1, width=30)
                op3_entry_edit.grid(row=3, column=1, pady=5)

                ans_lbl_edit = Label(editor1, text="Answer", background="#ffffff", font=("Gill Sans", 12))
                ans_lbl_edit.grid(row=4, column=0, padx=20, pady=5)
                ans_entry_edit = Entry(editor1, width=30)
                ans_entry_edit.grid(row=4, column=1, pady=5)

                th1_lbl_edit = Label(editor1, text="Theme 1", background="#ffffff", font=("Gill Sans", 12))
                th1_lbl_edit.grid(row=5, column=0, padx=20, pady=5)
                th1_entry_edit = Entry(editor1, width=30)
                th1_entry_edit.grid(row=5, column=1, pady=5)

                th2_lbl_edit = Label(editor1, text="Theme 2", background="#ffffff", font=("Gill Sans", 12))
                th2_lbl_edit.grid(row=6, column=0, padx=20, pady=5)
                th2_entry_edit = Entry(editor1, width=30)
                th2_entry_edit.grid(row=6, column=1, pady=5)

                edit1_submit = Button(editor1, text="Submit", font=("Gill Sans", 12, "bold"), background="green", command=submit)
                edit1_submit.grid(row=7, column=1)

                for record in records:
                    q_entry_edit.insert(0, record[0])
                    op1_entry_edit.insert(0, record[1])
                    op2_entry_edit.insert(0, record[2])
                    op3_entry_edit.insert(0, record[3])
                    ans_entry_edit.insert(0, record[4])
                    th1_entry_edit.insert(0, record[5])
                    th2_entry_edit.insert(0, record[6])

                conn.commit()
                c.close()

    def add():
        conn = sqlite3.connect("questions.db")
        c = conn.cursor()
        ###############################################################
        # check that all compulsory options have been filled in
        if (q_entry.get() == "") or (op1_entry.get() == "") or (op2_entry.get() == "") or (op3_entry.get() == "") or(ans_entry.get() == ""):
            error_msg = messagebox.showerror("Error", "Please make sure you have entered a question, its correct answer, and 3 other answer options.")
            return
        else:
        ###############################################################
            c.execute("INSERT INTO mcq VALUES (:question, :option1, :option2, :option3, :answer, :theme1, :theme2)",
                {
                'question': q_entry.get(),
                'option1': op1_entry.get(),
                'option2': op2_entry.get(),
                'option3': op3_entry.get(),
                'answer': ans_entry.get(),
                'theme1': th1_entry.get(),
                'theme2': th2_entry.get()
                })


            q_entry.delete(0, END)
            op1_entry.delete(0, END)
            op2_entry.delete(0, END)
            op3_entry.delete(0, END)
            ans_entry.delete(0, END)
            th1_entry.delete(0, END)
            th2_entry.delete(0, END)

            conn.commit()
            c.close()
            confirm_msg = messagebox.showinfo("Success", "Question added successfully. Exit and reopen this window to see your changes.")

    def submit():
        conn = sqlite3.connect("questions.db")
        c = conn.cursor()

        ###############################################################
        # check that all compulsory options have been filled in
        if ((q_entry_edit.get() == "") or (op1_entry_edit.get() == "") or (op2_entry_edit.get() == "") or (
                op3_entry_edit.get() == "") or (ans_entry_edit.get() == "")):
            error_msg = messagebox.showerror("Error",
                                             "Please make sure you have entered a question, its correct answer, and 3 other answer options.", parent=editor1)
            return

        else:
            response = messagebox.askyesno("Update", "Are you sure you want to make these changes?", parent=editor1)
            if response == 1:
                    c.execute(""" UPDATE mcq SET
                    question = :question,
                    option1 = :op1,
                    option2 = :op2,
                    option3 = :op3,
                    answer = :ans,
                    theme1 = :th1,
                    theme2 = :th2
                    WHERE oid = :oid""",
                    {
                    'question': q_entry_edit.get(),
                    'op1': op1_entry_edit.get(),
                    'op2': op2_entry_edit.get(),
                    'op3': op3_entry_edit.get(),
                    'ans': ans_entry_edit.get(),
                    'th1': th1_entry_edit.get(),
                    'th2': th2_entry_edit.get(),
                    'oid': id_entry.get()
                    })
                    confirm_msg = messagebox.showinfo("Success",
                                                      "Question edited successfully. Exit and reopen this window to see your changes.", parent=editor1)
                    editor1.destroy()
            else:
                return

            conn.commit()
            c.close()

    def delete():
        ##########################################################################
        # check that question ID has been entered
        if id_entry.get() == "":
            messagebox.showerror("Warning", "Please enter the Question ID")
            return
        else:
            conn = sqlite3.connect("questions.db")
            c = conn.cursor()
            # check that a question exists in the table with that ID
            c.execute("SELECT COUNT (*) FROM mcq WHERE oid = " + id_entry.get())
            id_present = c.fetchone()[0]  # get the number of records with the specified ID.

            if id_present == 0:  # if there is a record with the ID
                id_error = messagebox.showerror("Error", "No question with that ID found in the table.")
                return

            else:

                response = messagebox.askyesno("Delete", "Are you sure you want to delete this question?")
                if response == 1:
                    c.execute("DELETE from mcq WHERE oid = " + id_entry.get())
                    confirm_msg = messagebox.showinfo("Success", "Question deleted successfully. Exit and reopen this window to see your changes.")
                    id_entry.delete(0, 'end')
                else:
                    return

            conn.commit()
            c.close()


    createDB("questions.db")

    q_lbl = Label(window, text="Question", background="#ffffff", font=("Gill Sans", 12))
    q_lbl.grid(row=0, column=0, padx=40, pady=(10, 5))
    q_entry = Entry(window, width=50)
    q_entry.grid(row=0, column=1, pady=(10, 5))

    op1_lbl = Label(window, text="Option 1", background="#ffffff", font=("Gill Sans", 12))
    op1_lbl.grid(row=1, column=0, padx=40, pady=5)
    op1_entry = Entry(window, width=50)
    op1_entry.grid(row=1, column=1, pady=5)

    op2_lbl = Label(window, text="Option 2", background="#ffffff", font=("Gill Sans", 12))
    op2_lbl.grid(row=2, column=0, padx=40, pady=5)
    op2_entry = Entry(window, width=50)
    op2_entry.grid(row=2, column=1, pady=5)

    op3_lbl = Label(window, text="Option 3", background="#ffffff", font=("Gill Sans", 12))
    op3_lbl.grid(row=3, column=0, padx=40, pady=5)
    op3_entry = Entry(window, width=50)
    op3_entry.grid(row=3, column=1, pady=5)

    ans_lbl = Label(window, text="Answer", background="#ffffff", font=("Gill Sans", 12))
    ans_lbl.grid(row=4, column=0, padx=40, pady=5)
    ans_entry = Entry(window, width=50)
    ans_entry.grid(row=4, column=1, pady=5)

    th1_lbl = Label(window, text="Theme 1", background="#ffffff", font=("Gill Sans", 12))
    th1_lbl.grid(row=5, column=0, padx=40, pady=5)
    th1_entry = Entry(window, width=50)
    th1_entry.grid(row=5, column=1, pady=5)

    th2_lbl = Label(window, text="Theme 2", background="#ffffff", font=("Gill Sans", 12))
    th2_lbl.grid(row=6, column=0, padx=40, pady=5)
    th2_entry = Entry(window, width=50)
    th2_entry.grid(row=6, column=1, pady=5)

    add_question = Button(window, text="Add Question", font=("Gill Sans", 12, "bold"), background="green", command=add)
    add_question.grid(row=7, column=1, pady=5)

    q_list = Listbox(window, height=5, width=65)
    scroll = Scrollbar(window, command=q_list.yview)
    q_list.configure(yscrollcommand=scroll.set)
    q_list.grid(row=8, column=0, columnspan=2, pady=10, padx=5)
    scroll.grid(row=8, column=2, pady=10)

    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM mcq")
    records = c.fetchall()
    for record in records:
        q_list.insert(END, str(record[7]) + "." + " " + str(record[0]))
    q_list.selection_set(END)

    conn.commit()
    c.close()

    edit_button = Button(window, text="Edit/View", font=("Gill Sans", 12, "bold"), background="green", command=edit)
    edit_button.grid(row=9, column=1, padx=5, pady=5, rowspan=2)
    del_button= Button(window, text="Delete", font=("Gill Sans", 12, "bold"), background="green", command=delete)
    del_button.grid(row=9, column=2, padx=5, pady=5, rowspan=2)
    id_entry = Entry(window, width=5)
    id_entry.grid(row=10, column=0, padx=5)
    id_lbl = Label(window, text="Enter Question ID:", background="#ffffff", font=("Gill Sans", 12))
    id_lbl.grid(row=9, column=0, pady=5, padx =5)
