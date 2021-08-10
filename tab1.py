import tkinter as tk
from tkinter import ttk

import datetime

import db_manage


"""class Frame1(ttk.Frame):
    def __init__(self, container):
        super().__init__()

        self.labelA = ttk.Label(self, text="This is on Frame One")
        self.labelA.grid(column=1, row=1)"""


class Frame2(ttk.Frame):
    def __init__(self, container):
        super().__init__()

        self.labelB = ttk.Label(self, text="This is on Frame Two")
        self.labelB.grid(column=1, row=1)


class Frame1(ttk.Frame):
    def __init__(self, container, general, timer):
        super().__init__()

        self.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.pack(pady=100, padx=100)

        """self.labelA = ttk.Label(self, text="This is on Frame One")
        self.labelA.grid(column=1, row=1)

        self.labelC = tk.Label(self, text="Testing 123")
        self.labelC.grid(column=1, row=2)"""

        self.call_display_bool = True
        self.show_display_on_startup = False

        self.seconds_passed = int((timer.end_time - timer.start_time).total_seconds())
        self.subject_timer = tk.StringVar()
        self.subject_timer.set("")
        self.subtopic_timer = tk.StringVar()
        self.subtopic_timer.set("")
        self.project_timer = tk.StringVar()
        self.project_timer.set("")

        self.subject_options = general.subject_options
        self.subject_textbox_label = ttk.Label(self, text="Enter a new subject")
        self.subject_textbox = tk.Text(self, height=1, width=12)
        self.subject_label = ttk.Label(self, text="Choose a subject")
        self.subject_timer_label = ttk.Label(self, textvariable=self.subject_timer)
        self.subject_choice = tk.StringVar(self.master)

        self.subtopic_options = general.subtopic_options
        self.subtopic_textbox_label = ttk.Label(self, text="Enter a new subtopic")
        self.subtopic_textbox = tk.Text(self, height=1, width=12)
        self.subtopic_label = ttk.Label(self, text="Choose a subtopic")
        self.subtopic_timer_label = ttk.Label(self, textvariable=self.subtopic_timer)
        self.subtopic_choice = tk.StringVar(self.master)

        self.project_options = general.project_options
        self.project_textbox_label = ttk.Label(self, text="Enter a new project")
        self.project_textbox = tk.Text(self, height=1, width=12)
        self.project_label = ttk.Label(self, text="Choose a project")
        self.project_timer_label = ttk.Label(self, textvariable=self.project_timer)
        self.project_choice = tk.StringVar(self.master)

        self.add_button = tk.Button(self, text="Add",
                                    command=lambda: self.add_text_to_options(general, timer))
        self.description_label = ttk.Label(self,
                                           text=f"{general.subject}, {general.subtopic}, {general.project}")

    def call_display(self, general, timer):
        self.subject_options_func(general)
        self.subtopic_options_func(general)
        self.project_options_func(general)
        # self.update_timer_button(general, timer)
        self.add_text_to_options(general, timer)

    def hide_labels(self):
        self.subject_label.grid_remove()
        self.subtopic_label.grid_remove()
        self.project_label.grid_remove()

        self.subject_textbox_label.grid_remove()
        self.subtopic_textbox_label.grid_remove()
        self.project_textbox_label.grid_remove()

        self.subject_textbox.grid_remove()
        self.subtopic_textbox.grid_remove()
        self.project_textbox.grid_remove()

        self.add_button.grid_remove()

        self.subject_timer_label.grid(row=4, column=1)
        self.subtopic_timer_label.grid(row=4, column=2)
        self.project_timer_label.grid(row=4, column=3)

        self.description_label.grid(row=2, column=2)

    def show_labels(self):
        self.subject_label.grid()
        self.subtopic_label.grid()
        self.project_label.grid()

        self.subject_textbox_label.grid()
        self.subtopic_textbox_label.grid()
        self.project_textbox_label.grid()

        self.subject_textbox.grid()
        self.subtopic_textbox.grid()
        self.project_textbox.grid()

        self.add_button.grid()

        self.subject_timer_label.grid_remove()
        self.subtopic_timer_label.grid_remove()
        self.project_timer_label.grid_remove()

        self.description_label.grid_remove()

    def subject_options_func(self, general):
        subject_column = 1

        self.subject_choice.set(self.subject_options[0])
        general.subjects_dropdown = tk.OptionMenu(self, self.subject_choice, *self.subject_options)

        self.subject_textbox_label.grid(row=2, column=subject_column)
        self.subject_textbox.grid(row=3, column=subject_column)

        self.subject_label.grid(row=4, column=subject_column)
        general.subjects_dropdown.grid(row=5, column=subject_column)

    def subtopic_options_func(self, general):
        subtopic_column = 2

        self.subtopic_choice.set(self.subtopic_options[0])
        general.subtopics_dropdown = tk.OptionMenu(self, self.subtopic_choice, *self.subtopic_options)

        self.subtopic_textbox_label.grid(row=2, column=subtopic_column)
        self.subtopic_textbox.grid(row=3, column=subtopic_column)

        self.subtopic_label.grid(row=4, column=subtopic_column)
        general.subtopics_dropdown.grid(row=5, column=subtopic_column)

    def project_options_func(self, general):
        project_column = 3

        self.project_choice.set(self.project_options[0])
        general.project_dropdown = tk.OptionMenu(self, self.project_choice, *self.project_options)

        self.project_textbox_label.grid(row=2, column=project_column)
        self.project_textbox.grid(row=3, column=project_column)

        self.project_label.grid(row=4, column=project_column)
        general.project_dropdown.grid(row=5, column=project_column)

    def add_text_to_options(self, general, timer):
        subject_text_value = self.subject_textbox.get("1.0", "end-1c")
        if len(subject_text_value) > 0:
            self.subject_options.append(subject_text_value)
            self.subject_options = sorted(self.subject_options)
            self.subject_textbox.delete("1.0", "end-1c")
            self.call_display(general, timer)

        subtopic_text_value = self.subtopic_textbox.get("1.0", "end-1c")
        if len(subtopic_text_value) > 0:
            self.subtopic_options.append(subtopic_text_value)
            self.subtopic_options = sorted(self.subtopic_options)
            self.subtopic_textbox.delete("1.0", "end-1c")
            self.call_display(general, timer)

        project_text_value = self.project_textbox.get("1.0", "end-1c")
        if len(project_text_value) > 0:
            self.project_options.append(project_text_value)
            self.project_options = sorted(self.project_options)
            self.project_textbox.delete("1.0", "end-1c")
            self.call_display(general, timer)

        self.add_button.grid(row=2, column=0)

    def update_timer_button(self, general, timer):
        def update_button():
            if general.start_button_press is False:
                general.start_button_press = True
            else:
                general.start_button_press = False

            if general.start_button_press is True:
                general.subject = str(self.subject_choice.get())
                general.subtopic = str(self.subtopic_choice.get())
                general.project = str(self.project_choice.get())

                db_manage.seconds_for_item(general)

                start_stop_button.config(text="Stop")
                timer.set_time_start()
                self.update_timers(general, timer)

                self.description_label = ttk.Label(self,
                                                   text=f"{general.subject}, {general.subtopic}, {general.project}")

                self.hide_labels()

            else:
                print(f"start_stop_button = {str(general.start_button_press)}")
                start_stop_button.config(text="Start")

                self.show_labels()
                db_manage.daily_study_entry(subject=general.subject,
                                            subtopic=general.subtopic,
                                            project=general.project,
                                            start_time=timer.start_time,
                                            end_time=timer.end_time)
                general.subject_seconds = 0
                general.subtopic_seconds = 0
                general.project_seconds = 0
                self.seconds_passed = 0
                timer.end_time = 0

        print(self.show_display_on_startup)
        if self.show_display_on_startup is False:
            # this bool ^^ is switched to true in main.py
            start_stop_button = tk.Button(self, text="Start", command=update_button)
            start_stop_button.grid(row=4, column=0)

    def update_timers(self, general, timer):
        if general.start_button_press is True:
            timer.end_time = datetime.datetime.now()

            self.seconds_passed = int((timer.end_time - timer.start_time).total_seconds())

            self.refresh_timer(general, timer)
            self.after(1000, self.update_timers, general, timer)

    def refresh_timer(self, general, timer):
        subject_hours, subject_remainder = divmod(self.seconds_passed + general.subject_seconds, 3600)
        subject_minutes, subject_seconds = divmod(subject_remainder, 60)
        self.subject_timer.set(f"{subject_hours}:{subject_minutes}:{subject_seconds}")
        print(general.subject, f"{subject_hours}:{subject_minutes}:{subject_seconds}")

        subtopic_hours, subtopic_remainder = divmod(self.seconds_passed + general.subtopic_seconds, 3600)
        subtopic_minutes, subtopic_seconds = divmod(subtopic_remainder, 60)
        self.subtopic_timer.set(f"{subject_hours}:{subtopic_minutes}:{subtopic_seconds}")
        print(general.subtopic, f"{subject_hours}:{subtopic_minutes}:{subtopic_seconds}")

        project_hours, project_remainder = divmod(self.seconds_passed + general.project_seconds, 3600)
        project_minutes, project_seconds = divmod(project_remainder, 60)
        self.project_timer.set(f"{project_hours}:{project_minutes}:{project_seconds}")
        print(general.project, f"{project_hours}:{project_minutes}:{project_seconds}")

        self.update_timer_button(general, timer)
