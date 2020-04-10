import tkinter
from tkinter import *
import tkinter.scrolledtext as ScTxt
from tkinter import messagebox
import sqlite3
import os


def enter_tf(window):
    global q_entry
    global drop
    global var
    global th1_entry
    global th2_entry
    global q_list
    global id_entry

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

    def editTF():
        global editor2
        global q_entry_edit
        global var_edit
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
            c.execute("SELECT COUNT (*) FROM tfq WHERE oid = " + id_entry.get())
            id_present = c.fetchone()[0]  # get the number of records with the specified ID.

            if id_present == 0:  # if there no record with the ID
                id_error = messagebox.showerror("Error", "No question with that ID found in the table.")
                return

            else:
                editor2 = Tk()
                editor2.title("Update a Question")
                editor2.geometry("400x400")
                editor2.config(background="#ffffff")
                c.execute("SELECT * FROM tfq WHERE oid = " + id_entry.get())
                records = c.fetchall()

                q_lbl_edit = Label(editor2, text="Question", background="#ffffff", font=("Gill Sans", 12))
                q_lbl_edit.grid(row=0, column=0, padx=20, pady=(10, 5))
                q_entry_edit = Entry(editor2, width=30)
                q_entry_edit.grid(row=0, column=1, pady=(10, 5))

                ##############
                var_edit = StringVar(editor2)
                ##############
                ans_edit = Label(editor2, text="Answer", background="#ffffff", font=("Gill Sans", 12))
                ans_edit.grid(row=1, column=0, pady=5)
                drop_edit = OptionMenu(editor2, var_edit, *options)
                drop_edit.grid(row=1, column=1, pady=5, ipadx=10)

                th1_lbl_edit = Label(editor2, text="Theme 1", background="#ffffff", font=("Gill Sans", 12))
                th1_lbl_edit.grid(row=3, column=0, padx=20, pady=5)
                th1_entry_edit = Entry(editor2, width=30)
                th1_entry_edit.grid(row=3, column=1, pady=5)

                th2_lbl_edit = Label(editor2, text="Theme 2", background="#ffffff", font=("Gill Sans", 12))
                th2_lbl_edit.grid(row=4, column=0, padx=20, pady=5)
                th2_entry_edit = Entry(editor2, width=30)
                th2_entry_edit.grid(row=4, column=1, pady=5)

                edit2_submit = Button(editor2, text="Submit", command=submit)
                edit2_submit.grid(row=5, column=1)

                for record in records:
                    q_entry_edit.insert(0, record[0])
                    th1_entry_edit.insert(0, record[2])
                    th2_entry_edit.insert(0, record[3])
                    if str(record[1]) == str(options[0]):
                        var_edit.set(options[0])
                    else:
                        var_edit.set(options[1])

                conn.commit()
                c.close()

    def add():

        conn = sqlite3.connect("questions.db")
        c = conn.cursor()
        ###############################################################
        # check that all compulsory options have been filled in
        if ((q_entry.get() == "") or (var.get() == "")):
            error_msg = messagebox.showerror("Error",
                                             "Please make sure you have entered a question and its correct answer.")
            return
        else:
        ###############################################################
            c.execute("INSERT INTO tfq VALUES (:question, :answer, :theme1, :theme2)",
            {
            'question': q_entry.get(),
            'answer': var.get(),
            'theme1': th1_entry.get(),
            'theme2': th2_entry.get()
            })


            q_entry.delete(0, END)
            th1_entry.delete(0, END)
            th2_entry.delete(0, END)

            conn.commit()
            c.close()
            confirm_msg = messagebox.showinfo("Success",
                                          "Question added successfully. Exit and reopen this window to see your changes.")

    def submit():
        conn = sqlite3.connect("questions.db")
        c = conn.cursor()

        ###############################################################
        # check that all compulsory options have been filled in
        if ((q_entry_edit.get() == "") or (var_edit.get() == "")):
            error_msg = messagebox.showerror("Error",
                                             "Please make sure you have entered a question and its correct answer.",
                                             parent=editor2)
            return

        else:
            response = messagebox.askyesno("Update", "Are you sure you want to make these changes?")
            if response == 1:
                c.execute(""" UPDATE tfq SET
                                question = :question,
                                answer = :ans,
                                theme1 = :th1,
                                theme2 = :th2
                                WHERE oid = :oid""",
                          {
                              'question': q_entry_edit.get(),
                              'ans': var_edit.get(),
                              'th1': th1_entry_edit.get(),
                              'th2': th2_entry_edit.get(),
                              'oid': id_entry.get()
                          })
                confirm_msg = messagebox.showinfo("Success",
                                                  "Question edited successfully. Exit and reopen this window to see your changes.", parent=editor2)
                editor2.destroy()
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
            c.execute("SELECT COUNT (*) FROM tfq WHERE oid = " + id_entry.get())
            id_present = c.fetchone()[0]  # get the number of records with the specified ID.

            if id_present == 0:  # if there is a record with the ID
                id_error = messagebox.showerror("Error", "No question with that ID found in the table.")
                return

            else:

                response = messagebox.askyesno("Delete", "Are you sure you want to delete this question?")
                if response == 1:
                    c.execute("DELETE from tfq WHERE oid = " + id_entry.get())
                    confirm_msg = messagebox.showinfo("Success",
                                                      "Question deleted successfully. Exit and reopen this window to see your changes.")
                    id_entry.delete(0, 'end')
                else:
                    return

            conn.commit()
            c.close()

    createDB("questions.db")

    q_lbl = Label(window, text="Question", background="#ffffff", font=("Gill Sans", 12))
    q_lbl.grid(row=0, column=0, padx=20, pady=(10, 5))
    q_entry = Entry(window, width=30)
    q_entry.grid(row=0, column=1, pady=(10, 5))

    val = StringVar()
    ans = Label(window, text="Answer", background="#ffffff", font=("Gill Sans", 12))
    ans.grid(row=1, column=0, padx=20, pady=5)
    options = ["True", "False"]
    var = StringVar()
    var.set(options[0])
    drop = OptionMenu(window, var, *options)
    drop.grid(row=1, column=1, pady=5)

    th1_lbl = Label(window, text="Theme 1", background="#ffffff", font=("Gill Sans", 12))
    th1_lbl.grid(row=3, column=0, padx=20, pady=5)
    th1_entry = Entry(window, width=30)
    th1_entry.grid(row=3, column=1, pady=5)

    th2_lbl = Label(window, text="Theme 2", background="#ffffff", font=("Gill Sans", 12))
    th2_lbl.grid(row=4, column=0, padx=20, pady=5)
    th2_entry = Entry(window, width=30)
    th2_entry.grid(row=4, column=1, pady=5)

    add_btn = Button(window, text="Add Question", font=("Gill Sans", 12, "bold"), background="green", command=add)
    add_btn.grid(row=5, column=1, pady=5)

    q_list = Listbox(window, height=5, width=65)
    scroll = Scrollbar(window, command=q_list.yview)
    q_list.configure(yscrollcommand=scroll.set)
    q_list.grid(row=6, column=0, columnspan=2, pady=10, padx=5)
    scroll.grid(row=6, column=2, pady=10)

    conn = sqlite3.connect("questions.db")
    c = conn.cursor()
    c.execute("SELECT *, oid FROM tfq")
    records = c.fetchall()
    for record in records:
        q_list.insert(END, str(record[4]) + "." + " " + str(record[0]) + ", ans: " +  str(record[1]))
    q_list.selection_set(END)
    conn.commit()
    c.close()

    edit_btn = Button(window, text="Edit/View", font=("Gill Sans", 12, "bold"), background="green", command=editTF)
    edit_btn.grid(row=7, column=1, padx=5, pady=5, rowspan=2)
    del_btn = Button(window, text="Delete", font=("Gill Sans", 12, "bold"), background="green", command=delete)
    del_btn.grid(row=7, column=2, padx=5, pady=5, rowspan=2)
    id_entry = Entry(window, width=5)
    id_entry.grid(row=8, column=0, padx=5)
    id_lbl = Label(window, text="Enter Question ID:", background="#ffffff", font=("Gill Sans", 12))
    id_lbl.grid(row=7, column=0, pady=5, padx =5)
