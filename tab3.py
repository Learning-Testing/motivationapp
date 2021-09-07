from tkinter import ttk
import tkinter as tk

import db_manage


class Frame3(ttk.Frame):
    def __init__(self, container):
        super().__init__()
        # quiz entry, tab4 can be actual quiz
        # choose a dropdown "set"

        """self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        # self.pack(pady=100, padx=100)
        self.pack(expand=True, fill="both")"""

        self.add_button = tk.Button(self, text="Add", command=lambda: self.add_data_to_db())
        self.add_button.grid(row=0, column=0, padx=50)

        self.quiz_label_text = ["question",
                                "answer",
                                "incorrect1",
                                "incorrect2",
                                "incorrect3",
                                "answer reason",
                                "resources"]
        self.quiz_label_data = []
        self.sets_options = {}
        self.dropdown_choice = tk.StringVar(self.master)

        self.selected_subject = ""
        self.selected_subtopic = ""
        self.selected_project = ""

        self.handle_sets()
        self.fill_quiz_label_data()
        self.display_page()

    def handle_sets(self):
        for i in db_manage.get_distinct_sets():
            stringed_version = f"{i[0]} {i[1]} {i[2]}"
            self.sets_options[stringed_version] = [i[0], i[1], i[2]]

    @staticmethod
    def focus_next_widget(event):
        event.widget.tk_focusNext().focus()
        return "break"

    def enter_button_press(self, event=None):
        self.add_data_to_db()
        self.quiz_label_data[0][2].focus()
        return "break"

    def fill_quiz_label_data(self):
        last_item = self.quiz_label_text[-1]
        for i in self.quiz_label_text:
            str_stringvar = tk.StringVar()
            str_stringvar.set(i)
            label = ttk.Label(self, textvariable=str_stringvar)
            textbox = tk.Text(self, height=3, width=72, wrap=tk.WORD)
            if i == last_item:
                textbox.bind("<Return>", self.enter_button_press)  # finish this
            else:
                textbox.bind("<Tab>", self.focus_next_widget)
            self.quiz_label_data.append([label, str_stringvar, textbox])

    def display_page(self):
        options = list(self.sets_options.keys())
        self.dropdown_choice.set(options[0])
        set_dropdown = tk.OptionMenu(self, self.dropdown_choice, *options)
        # len(options)/2-1
        set_dropdown.grid(row=0, column=1)

        iterator = 1
        for i in self.quiz_label_data:
            i[0].grid(row=iterator, column=1, padx=50, pady=10)
            i[2].grid(row=iterator + 1, column=1, padx=50, pady=10)
            iterator += 2

    def add_data_to_db(self):
        db_data = []
        for i in self.quiz_label_data:
            text_data = i[2].get("1.0", "end-1c")
            if text_data is None or text_data == "":
                text_data = "None"
            db_data.append(text_data)
            i[2].delete("1.0", "end-1c")

        question = db_data[0]
        answer = db_data[1]
        incorrect1 = db_data[2]
        incorrect2 = db_data[3]
        incorrect3 = db_data[4]
        answer_reason = db_data[5]
        resources = db_data[6]

        option_set = self.dropdown_choice.get()
        subject = self.sets_options[option_set][0]
        subtopic = self.sets_options[option_set][1]
        project = self.sets_options[option_set][2]

        db_manage.add_quiz_question_data(question=question,
                                         answer=answer,
                                         incorrect1=incorrect1,
                                         incorrect2=incorrect2,
                                         incorrect3=incorrect3,
                                         subject=subject,
                                         subtopic=subtopic,
                                         project=project,
                                         answer_reason=answer_reason,
                                         resources=resources)

    # need to make a dropdown to choose what project/subtopic/subject, and create an add button (but can use enter key
    # as well), add subject, subtopic, and project to DB table
