from tkinter import ttk

import tkinter as tk
import random

import db_manage


class Frame4(ttk.Frame):
    def __init__(self, container, tab1, timer):
        super().__init__()

        self.start_button_press = False
        self.start_stop_button = tk.Button(self, text="Start", command=lambda: self.update_start_button(timer))
        self.start_stop_button.grid(row=0, column=0)

        self.submit_button_var = tk.IntVar()
        self.submit_button = tk.Button(self, text="Submit", command=lambda: [self.handle_selected_data(timer),
                                                                             self.submit_button_var.set(1)])

        self.subject_choice = tk.StringVar(self.master)
        self.subtopic_choice = tk.StringVar(self.master)
        self.project_choice = tk.StringVar(self.master)

        self.subject_dropdown = tk.OptionMenu(self, self.subject_choice, *tab1.subject_options)
        self.subtopic_dropdown = tk.OptionMenu(self, self.subtopic_choice, *tab1.subtopic_options)
        self.project_dropdown = tk.OptionMenu(self, self.project_choice, *tab1.project_options)

        self.size_label = tk.Label(self, text="How many questions would you like for your quiz?")
        self.question_size_entry = tk.Entry(self,
                                            validate="all",
                                            validatecommand=(self.register(self.test_value), "%P"))

        self.data = ()
        self.session_num = 0
        self.question_num = -1

        self.question_label = tk.Label(self, text="", wraplength=600, justify="left")
        self.question_label.grid(row=0, column=0, sticky="w")
        self.question_label.grid_remove()

        self.radio_var = tk.StringVar()
        self.sb_selected = tk.IntVar()
        r1 = tk.Radiobutton(self, text="", variable=self.radio_var, value="", wraplength=600, justify="left")
        r2 = tk.Radiobutton(self, text="", variable=self.radio_var, value="", wraplength=600, justify="left")
        r3 = tk.Radiobutton(self, text="", variable=self.radio_var, value="", wraplength=600, justify="left")
        r4 = tk.Radiobutton(self, text="", variable=self.radio_var, value="", wraplength=600, justify="left")
        self.radio_buttons = [r1, r2, r3, r4]

        self.max_page_len = 0
        self.page_var = tk.IntVar()
        self.page_var.set(0)

        self.next_page_button = tk.Button(self, text="Next",
                                          command=lambda: [self.show_results(),
                                                           self.page_var.set(self.page_var.get() + 1)])

        self.previous_page_button = tk.Button(self, text="Previous",
                                              command=lambda: [self.show_results(),
                                                               self.page_var.set(self.page_var.get() - 1)])

        self.main_screen_button = tk.Button(self, text="Home Screen", command=lambda: [self.update_start_button(timer),
                                                                                       self.hide_results_screen()])

        self.answer_correct_var = tk.StringVar()
        self.answered_correctly_label = tk.Label(self, textvariable=self.answer_correct_var, wraplength=600,
                                                 justify="left")
        self.results_question_var = tk.StringVar()
        self.results_question_label = tk.Label(self, textvariable=self.results_question_var, wraplength=600,
                                               justify="left")
        self.selected_answer_var = tk.StringVar()
        self.selected_answer_label = tk.Label(self, textvariable=self.selected_answer_var, wraplength=600,
                                              justify="left")
        self.correct_answer_var = tk.StringVar()
        self.correct_answer_label = tk.Label(self, textvariable=self.correct_answer_var, wraplength=600,
                                             justify="left")
        self.answer_reason_var = tk.StringVar()
        self.answer_reason_label = tk.Label(self, textvariable=self.answer_reason_var, wraplength=600,
                                            justify="left")
        self.resources_var = tk.StringVar()
        self.resources_label = tk.Label(self, textvariable=self.resources_var, wraplength=600,
                                        justify="left")

        self.quiz_results = []

        self.question = tk.Label(self, text="Question: ")
        self.selected_answer = tk.Label(self, text="Selected Answer: ")
        self.correct_answer = tk.Label(self, text="Correct Answer: ")
        self.reasoning = tk.Label(self, text="Reasoning: ")
        self.resources = tk.Label(self, text="Resources: ")

    @staticmethod
    def test_value(val):
        if val.isdigit() or val == "":
            return True
        return False

    def display_options(self):
        self.subject_dropdown.grid(row=1, column=1, padx=10)
        self.subtopic_dropdown.grid(row=1, column=2, padx=10)
        self.project_dropdown.grid(row=1, column=3, padx=10)
        self.size_label.grid(row=0, column=4)
        self.question_size_entry.grid(row=1, column=4)

    def hide_options(self):
        self.subject_dropdown.grid_remove()
        self.subtopic_dropdown.grid_remove()
        self.project_dropdown.grid_remove()
        self.size_label.grid_remove()
        self.question_size_entry.grid_remove()
        self.question_size_entry.delete("1.0", "end-1c")

    def update_start_button(self, timer):  # starts quiz
        if self.start_button_press is False:
            self.start_button_press = True
            self.start_stop_button.grid_remove()
            self.hide_options()

            q_size = self.question_size_entry.get()
            if len(q_size) > 0:
                q_size = int(q_size)
                if q_size > 0:
                    self.data = db_manage.get_questions(limit=q_size,
                                                        subject=str(self.subject_choice.get()),
                                                        subtopic=str(self.subtopic_choice.get()),
                                                        project=str(self.project_choice.get()))
                    self.session_num = int(db_manage.get_session_num()) + 1
                    self.submit_button.grid(row=6, column=1, pady=10)
                    self.start_test(timer)

        else:
            self.start_button_press = False
            self.display_options()
            self.start_stop_button.grid(row=0, column=0)

    def start_test(self, timer):
        self.question_label.grid(row=0, column=0)
        for sublist in self.data:
            self.get_question_data(timer, sublist)
            self.submit_button.wait_variable(self.submit_button_var)
        self.quiz_results = db_manage.get_results(self.session_num)
        self.show_results_screen()
        self.show_results()

    def get_question_data(self, timer, sublist):
        timer.set_time_start()
        self.question_num = int(sublist[0])
        question = sublist[2]
        answer = sublist[3]
        answers = [answer, sublist[4], sublist[5], sublist[6]]
        print(104, question, answer, answers)
        random.shuffle(answers)

        self.display_question(question, answer, answers)

    def display_question(self, question, answer, answers):

        self.question_label.config(text=question)

        iterator = 0
        for i in answers:
            if i != "None":
                self.radio_buttons[iterator].config(text=i, value=i)
                self.radio_buttons[iterator].grid(row=iterator + 1, column=0, sticky="w")
            else:
                self.radio_buttons[iterator].grid_remove()
            iterator += 1

    def handle_selected_data(self, timer):
        selected_answer = self.radio_var.get()
        print(121, selected_answer)

        timer.set_time_end()

        db_manage.write_to_quiz_data(self.question_num,
                                     selected_answer,
                                     self.session_num,
                                     timer.start_time,
                                     timer.end_time)

        # need a quiz complete screen to view questions and answers

    def show_results_screen(self):
        # Currently we are making a new label each time, which does not work because it will show previous information
        # underneath. Also need to have labels, such as question:, correct answer: etc. to left of results
        # lambda is being done incorrectly, currently allows list index out of range error

        self.question_label.grid_remove()
        self.submit_button.grid_remove()
        for i in self.radio_buttons:
            i.grid_remove()

        self.max_page_len = len(self.quiz_results)

        self.next_page_button.grid(row=8, column=3)
        self.previous_page_button.grid(row=8, column=0)
        self.main_screen_button.grid(row=0, column=0)

        self.question.grid(row=2, column=0, sticky="w")
        self.selected_answer.grid(row=3, column=0, sticky="w")
        self.correct_answer.grid(row=4, column=0, sticky="w")
        self.reasoning.grid(row=5, column=0, sticky="w")
        self.resources.grid(row=6, column=0, sticky="w")

        self.answered_correctly_label.grid(row=1, column=1, sticky="w")
        self.results_question_label.grid(row=2, column=1, sticky="w")
        self.selected_answer_label.grid(row=3, column=1, sticky="w")
        self.correct_answer_label.grid(row=4, column=1, sticky="w")
        self.answer_reason_label.grid(row=5, column=1, sticky="w")
        self.resources_label.grid(row=6, column=1, sticky="w")

    def show_results(self):
        num = self.page_var.get()
        print(191, num, self.max_page_len - 1)
        if num > self.max_page_len - 1:
            self.page_var.set(self.max_page_len - 1)
            print(194, self.max_page_len - 1)
        elif num < 0:
            self.page_var.set(0)
            print(197, self.page_var.get())

        sublist = self.quiz_results[self.page_var.get()]

        if sublist[1] == sublist[2]:
            answer = "Correct"
        else:
            answer = "Incorrect"

        # this is currently not being shown
        # self.answer_reason_var.set(answer)
        self.results_question_var.set(sublist[0])
        self.selected_answer_var.set(sublist[2])
        self.correct_answer_var.set(sublist[1])
        self.answer_reason_var.set(sublist[3])
        self.resources_var.set(sublist[4])

    def hide_results_screen(self):
        self.next_page_button.grid_remove()
        self.previous_page_button.grid_remove()
        self.main_screen_button.grid_remove()

        self.question.grid_remove()
        self.selected_answer.grid_remove()
        self.correct_answer.grid_remove()
        self.reasoning.grid_remove()
        self.resources.grid_remove()

        self.answered_correctly_label.grid_remove()
        self.results_question_label.grid_remove()
        self.selected_answer_label.grid_remove()
        self.correct_answer_label.grid_remove()
        self.answer_reason_label.grid_remove()
        self.resources_label.grid_remove()
