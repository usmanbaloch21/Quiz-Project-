
from statistics import display_statistics
from quiz import run_quiz
from enter_mc import *
from enter_tf import *
from tkinter import *
from create_quiz import *

def open_homepage(root):
    # needed so when the homepage is re-opened using the back button, the window is cleared.
    for widget in root.winfo_children():
        if widget.winfo_class() != "Toplevel":
            widget.destroy()

    frame_btns = Frame(root, background="#ffffff") #create frame to arrange buttons with grid while using pack in the window

    # --- BUTTON STYLING --------------------------------

    btn_background = "green"
    large_btn_font = ("Gill Sans", 20, "bold")
    small_btn_font = ("Gill Sans", 12, "bold")

    # --- FUNCTIONS TO LOGIN ---------------------

    def login(function):

        def validate(function):
            username = entry_username.get()
            password = entry_password.get()
            if (username == "Admin") and (password == "Admin"):
                for widget in root.winfo_children():
                    widget.pack_forget()
                function()
            else:
                login_failed = messagebox.showerror("Login failed", "Login failed - please try again.")




            # hard coded in the user details for now. If wanting to add new users,
            # need to check how we're storing the users - database? in binary files as dictionary?
            # if username in users_dict:
            # if users_dict[username] == password
            # then return 1
            # else error message and return 0

        # --- SETTING UP THE LOGIN PAGE LAYOUT --------------------------------------

        for widget in root.winfo_children():
            widget.pack_forget()  # clear the page

        lbl_title = Label(root, text="Enter Username and Password", background="#ffffff", justify="center",
                          font=("Gill Sans", 20, "bold"))
        lbl_username = Label(root, text="Username:", background="#ffffff", justify="center",
                             font=("Gill Sans", 12, "bold"))
        lbl_password = Label(root, text="Password:", background="#ffffff", justify="center",
                             font=("Gill Sans", 12, "bold"))
        entry_username = Entry(root, bg="#ffffff", font=("Gill Sans", 12), )  # default text username
        # entry_username.insert(0, "Username")
        entry_password = Entry(root, bg="#ffffff", font=("Gill Sans", 12), show="*")  # default text password
        # entry_password.insert(0, "Password")
        btn_login = Button(root, text="Login", font=("Gill Sans", 12, "bold"), background="green",
                           command=lambda: validate(function))
        btn_back = Button(root, text="Back", font=("Gill Sans", 12, "bold"), background="green",
                          command=lambda: open_homepage(root))

        lbl_title.pack(pady=(160, 0))
        lbl_username.pack(pady=(30, 0))
        entry_username.pack(pady=(0, 5))
        lbl_password.pack(pady=(10, 5))
        entry_password.pack(pady=(0, 30))
        btn_login.pack()
        btn_back.pack(pady=(120, 0))

    # --- FUNCTIONS TO START A QUIZ ---------------------
    # completed for mcqs, still need to do for true or false quiz
    def open_quiz_window(quiz_type):
        t_start = Toplevel(root) # create a new top window
        t_start.title("Quiz")
        t_start.geometry("700x600")
        t_start.config(background="#ffffff")
        t_start.resizable(0, 0)
        run_quiz(t_start, quiz_type)

    def select_quiz_type():
        for widget in root.winfo_children():
            widget.pack_forget()
        start_text = "Please select which quiz \n you want to start:"
        select_quiz_type_label = Label(root, text=start_text, font=large_btn_font, background="#ffffff")
        btn_quiz1 = Button(root, text="Multiple Choice", font=large_btn_font, background=btn_background,
                            command=lambda: open_quiz_window("mcq"))
        btn_quiz2 = Button(root, text="True or False", font=large_btn_font, background=btn_background, command=lambda: open_quiz_window("true_or_false"))
        btn_back = Button(root, text="Back", font=small_btn_font, background=btn_background, command=lambda: open_homepage(root))
        select_quiz_type_label.pack(pady=(150, 0))
        btn_quiz1.pack(pady=(20, 5))
        btn_quiz2.pack()
        btn_back.pack(pady=(150, 0))

    # --- FUNCTIONS TO EDIT QUESTION BANK ---------------------
    # need to include actual functions in the lambda commands for both mcq and tf
    def open_qs_window(function):
        t_q = Toplevel(root)
        t_q.title("Question Bank")
        t_q.geometry("700x600")
        t_q.config(background="#ffffff")
        t_q.resizable(0, 0)
        function(t_q) #plus any extra parameters if needed

    def select_q_type():
        for widget in root.winfo_children():
            widget.pack_forget()
        qs_text = "Please select which quiz \n you want to add/edit/delete questions for:"
        select_quiz_type_label = Label(root, text=qs_text, font=large_btn_font, background="#ffffff")
        btn_qs1 = Button(root, text="Multiple Choice", font=large_btn_font, background=btn_background, command = lambda : open_qs_window(enter_mc))
        btn_qs2 = Button(root, text="True or False", font=large_btn_font, background=btn_background, command = lambda : open_qs_window(enter_tf))
        btn_back = Button(root, text="Back", font=small_btn_font, background=btn_background, command=lambda: open_homepage(root))
        select_quiz_type_label.pack(pady=(150, 0))
        btn_qs1.pack(pady=(20, 5))
        btn_qs2.pack()
        btn_back.pack(pady=(150, 0))

    # --- FUNCTIONS TO CREATE A QUIZ ---------------------
    # need to include actual functions in the lambda commands for both mcq and tf
    def open_create_window(quiz_type):
        t_create = Toplevel(root)
        t_create.title("Create Quiz")
        t_create.geometry("700x600")
        t_create.config(background="#ffffff")
        t_create.resizable(0, 0)
        create_quiz(t_create, quiz_type) #plus any extra parameters if needed

    def select_create_type():
        for widget in root.winfo_children():
            widget.pack_forget()
        create_text = "Please select which type of quiz \n you want to create:"
        select_quiz_type_label = Label(root, text=create_text, font=large_btn_font, background="#ffffff")

        btn_create1 = Button(root, text="Multiple Choice", font=large_btn_font, background=btn_background, command=lambda: open_create_window("mcq"))
        btn_create2 = Button(root, text="True or False", font=large_btn_font, background=btn_background, command = lambda: open_create_window("true_or_false"))
        btn_back = Button(root, text="Back", font=small_btn_font, background=btn_background, command=lambda: open_homepage(root))
        select_quiz_type_label.pack(pady=(150, 0))
        btn_create1.pack(pady=(20, 5))
        btn_create2.pack()
        btn_back.pack(pady=(150, 0))

    # --- FUNCTIONS TO VIEW STATS -----------------------------

    def open_stats_window(results_file, quiz_table):
        t_stats = Toplevel(root)
        t_stats.title("Statistics")
        t_stats.geometry("700x600")
        t_stats.config(background="#ffffff")
        t_stats.resizable(0, 0)
        display_statistics(t_stats, results_file, quiz_table)

    def select_stats_type():
        for widget in root.winfo_children():
            widget.pack_forget()
        stats_text = "Please select which quiz \n you want to view statistics for:"
        select_quiz_type_label = Label(root, text=stats_text, font=large_btn_font, background="#ffffff")
        btn_stats1 = Button(root, text="Multiple Choice", font=large_btn_font, background=btn_background,
                            command=lambda: open_stats_window("mcq_results.dat", "mc_quiz"))
        btn_stats2 = Button(root, text="True or False", font=large_btn_font, background=btn_background,
                            command= lambda: open_stats_window("true_false_results.dat", "tf_quiz"))
        btn_back = Button(root, text="Back", font=small_btn_font, background=btn_background,
                          command=lambda: open_homepage(root))
        select_quiz_type_label.pack(pady=(150, 0))
        btn_stats1.pack(pady=(20, 5))
        btn_stats2.pack()
        btn_back.pack(pady=(150, 0))

    # --- MAIN HOMEPAGE BUTTONS, LABELS AND IMAGES -------------------------
    # Questions button
    q_btn = Button(frame_btns, text="Question Bank", padx=32, pady=30, font = large_btn_font, background = btn_background, command = lambda: login(select_q_type))
    # Create Quiz button
    create_btn = Button(frame_btns, text="Create a Quiz", padx=41, pady=30, font = large_btn_font, background = btn_background, command = lambda: login(select_create_type))
    # Start quiz button
    start_btn = Button(frame_btns, text="Start a Quiz", padx=53, pady=30, font = large_btn_font, background = btn_background, command = select_quiz_type)
    # Statistics button
    stats_btn= Button(frame_btns, text="View Statistics", padx=30, pady=30, font = large_btn_font, background = btn_background, command = lambda: login(select_stats_type))

    title = Label(root, text="Quizardry", font=("Gill Sans", 50, "bold"), background = "#ffffff")
    welcome = Label(root, text="Welcome to Quizardry! \nTo get started, first create a quiz. \nThen once you've created the quiz, \nclick the Start Quiz button to run it!", font=("Gill Sans", 15, "bold"), background = "#ffffff")

    global img1  # so that the image can be accessed in the load_start_page function
    img1 = PhotoImage(file="images/wizard-hat.png")
    label_img = Label(root, image=img1, background="#ffffff")

    label_img.pack(side=TOP, pady=(15, 0))
    title.pack()


    welcome.pack(pady=(15, 0))
    frame_btns.pack(padx=10, pady=40)

    q_btn.grid(row=0, column=0)
    create_btn.grid(row=0, column=1)
    start_btn.grid(row=1, column=0)
    stats_btn.grid(row=1, column=1)
