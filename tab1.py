import tkinter as tk
from tkinter import ttk

import datetime

import db_manage


class Frame1(ttk.Frame):
    def __init__(self, container, general, timer):
        super().__init__()

        self.call_display_bool = True
        self.show_display_on_startup = False

        self.seconds_passed = int((timer.end_time - timer.start_time).total_seconds())
        # [[label, stringvar], [label, stringvar]]
        self.subject_label_list = []
        self.subtopic_label_list = []
        self.project_label_list = []

        self.session_frame_label = ttk.Label(self, text="Session")
        self.day_frame_label = ttk.Label(self, text="Today")
        self.week_frame_label = ttk.Label(self, text="Week")
        self.month_frame_label = ttk.Label(self, text="Month")
        self.year_frame_label = ttk.Label(self, text="Year")
        self.alltime_frame_label = ttk.Label(self, text="All Time")

        self.subject_options = general.subject_options
        self.subject_textbox_label = ttk.Label(self, text="Enter a new subject")
        self.subject_textbox = tk.Text(self, height=1, width=12)
        self.subject_label = ttk.Label(self, text="Choose a subject")
        self.subject_choice = tk.StringVar(self.master)

        self.subtopic_options = general.subtopic_options
        self.subtopic_textbox_label = ttk.Label(self, text="Enter a new subtopic")
        self.subtopic_textbox = tk.Text(self, height=1, width=12)
        self.subtopic_label = ttk.Label(self, text="Choose a subtopic")
        self.subtopic_choice = tk.StringVar(self.master)

        self.project_options = general.project_options
        self.project_textbox_label = ttk.Label(self, text="Enter a new project")
        self.project_textbox = tk.Text(self, height=1, width=12)
        self.project_label = ttk.Label(self, text="Choose a project")
        self.project_choice = tk.StringVar(self.master)

        self.add_button = tk.Button(self, text="Add",
                                    command=lambda: self.add_text_to_options(general, timer))

        self.subject_timer_text_label = ttk.Label(self, text=general.subject)
        self.subtopic_timer_text_label = ttk.Label(self, text=general.subtopic)
        self.project_timer_text_label = ttk.Label(self, text=general.project)

        self.create_timer_labels(general)

        self.session_row = 1
        self.today_row = 2
        self.week_row = 3
        self.month_row = 4
        self.year_row = 5
        self.alltime_row = 6
        self.subject_column = 1
        self.subtopic_column = 2
        self.project_column = 3

    def create_timer_labels(self, general):
        # this is for the session
        session_timer_stringvar = tk.StringVar()
        session_timer_stringvar.set("")
        self.subject_label_list.append([ttk.Label(self, textvariable=session_timer_stringvar), session_timer_stringvar])

        for i in general.subject_seconds_dict.keys():
            timer_stringvar = tk.StringVar()
            timer_stringvar.set("")
            timer_label = ttk.Label(self, textvariable=timer_stringvar)
            self.subject_label_list.append([timer_label, timer_stringvar])

        for i in general.subtopic_seconds_dict.keys():
            timer_stringvar = tk.StringVar()
            timer_stringvar.set("")
            timer_label = ttk.Label(self, textvariable=timer_stringvar)
            self.subtopic_label_list.append([timer_label, timer_stringvar])

        for i in general.project_seconds_dict.keys():
            timer_stringvar = tk.StringVar()
            timer_stringvar.set("")
            timer_label = ttk.Label(self, textvariable=timer_stringvar)
            self.project_label_list.append([timer_label, timer_stringvar])

    def call_display(self, general, timer):
        self.subject_options_func(general)
        self.subtopic_options_func(general)
        self.project_options_func(general)
        self.add_text_to_options(general, timer)

        general.subjects_dropdown.grid(row=5, column=1)
        general.subtopics_dropdown.grid(row=5, column=2)
        general.project_dropdown.grid(row=5, column=3)

    def hide_labels(self, general):
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

        general.subjects_dropdown.grid_remove()
        general.subtopics_dropdown.grid_remove()
        general.project_dropdown.grid_remove()

        # the time periods
        self.session_frame_label.grid(row=self.session_row, column=0)
        self.day_frame_label.grid(row=self.today_row, column=0)
        self.week_frame_label.grid(row=self.week_row, column=0)
        self.month_frame_label.grid(row=self.month_row, column=0)
        self.year_frame_label.grid(row=self.year_row, column=0)
        self.alltime_frame_label.grid(row=self.alltime_row, column=0)

        # the timers
        iterator = 1
        for i in self.subject_label_list:
            i[0].grid(row=iterator, column=self.subject_column)
            iterator += 1
        iterator = 1
        for i in self.subtopic_label_list:
            i[0].grid(row=iterator, column=self.subtopic_column)
            iterator += 1
        iterator = 1
        for i in self.project_label_list:
            i[0].grid(row=iterator, column=self.project_column)
            iterator += 1

        # the text above them
        self.subject_timer_text_label.grid(row=0, column=1)
        self.subtopic_timer_text_label.grid(row=0, column=2)
        self.project_timer_text_label.grid(row=0, column=3)

    def show_labels(self, general):
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

        general.subjects_dropdown.grid(row=5, column=1)
        general.subtopics_dropdown.grid(row=5, column=2)
        general.project_dropdown.grid(row=5, column=3)

        self.session_frame_label.grid_remove()
        self.day_frame_label.grid_remove()
        self.week_frame_label.grid_remove()
        self.month_frame_label.grid_remove()
        self.year_frame_label.grid_remove()
        self.alltime_frame_label.grid_remove()

        for i in self.subject_label_list:
            i[0].grid_remove()
        for i in self.subtopic_label_list:
            i[0].grid_remove()
        for i in self.project_label_list:
            i[0].grid_remove()

        self.subject_timer_text_label.grid_remove()
        self.subtopic_timer_text_label.grid_remove()
        self.project_timer_text_label.grid_remove()

    def subject_options_func(self, general):
        subject_column = 1

        self.subject_choice.set(self.subject_options[0])
        general.subjects_dropdown = tk.OptionMenu(self, self.subject_choice, *self.subject_options)

        self.subject_textbox_label.grid(row=2, column=subject_column)
        self.subject_textbox.grid(row=3, column=subject_column)

        self.subject_label.grid(row=4, column=subject_column)

    def subtopic_options_func(self, general):
        subtopic_column = 2

        self.subtopic_choice.set(self.subtopic_options[0])
        general.subtopics_dropdown = tk.OptionMenu(self, self.subtopic_choice, *self.subtopic_options)

        self.subtopic_textbox_label.grid(row=2, column=subtopic_column)
        self.subtopic_textbox.grid(row=3, column=subtopic_column)

        self.subtopic_label.grid(row=4, column=subtopic_column)

    def project_options_func(self, general):
        project_column = 3

        self.project_choice.set(self.project_options[0])
        general.project_dropdown = tk.OptionMenu(self, self.project_choice, *self.project_options)

        self.project_textbox_label.grid(row=2, column=project_column)
        self.project_textbox.grid(row=3, column=project_column)

        self.project_label.grid(row=4, column=project_column)

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

        self.add_button.grid(row=3, column=0)

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

                if general.first_iter is True:
                    self.collect_time_field_seconds(general)
                    db_manage.total_seconds_for_item(general)

                start_stop_button.config(text="Stop")
                timer.set_time_start()
                self.update_timers(general, timer)

                self.subject_timer_text_label = ttk.Label(self, text=general.subject)
                self.subtopic_timer_text_label = ttk.Label(self, text=general.subtopic)
                self.project_timer_text_label = ttk.Label(self, text=general.project)

                self.hide_labels(general)
                general.first_iter = False

            else:
                # print(f"start_stop_button = {str(general.start_button_press)}")
                start_stop_button.config(text="Start")

                self.show_labels(general)
                db_manage.daily_study_entry(subject=general.subject,
                                            subtopic=general.subtopic,
                                            project=general.project,
                                            start_time=timer.start_time,
                                            end_time=timer.end_time)
                general.total_subject_seconds = 0
                general.total_subtopic_seconds = 0
                general.total_project_seconds = 0
                self.seconds_passed = 0
                timer.end_time = 0

        if self.show_display_on_startup is False:
            # this bool ^^ is switched to true in main.py
            start_stop_button = tk.Button(self, text="Start", command=update_button)
            start_stop_button.grid(row=0, column=0)

    def update_timers(self, general, timer):
        if general.start_button_press is True:
            timer.end_time = datetime.datetime.now()

            self.seconds_passed = int((timer.end_time - timer.start_time).total_seconds())

            self.refresh_timers(general, timer)
            self.after(1000, self.update_timers, general, timer)

    def refresh_timers(self, general, timer):
        def update_timer(keyword_seconds, timer_keyword):
            combined_seconds = self.seconds_passed + keyword_seconds
            hours, minutes, seconds = general.breakdown_time(combined_seconds)
            timer_keyword.set(f"{hours}:{minutes}:{seconds}")
        # print(self.subject_timer, self.subject_timer, self.project_timer)

        # iterate over the day, week, month, etc. and update them
        # iterate over the stringvars, then it
        # for label_sublist in self.subject_label_list:
        iterator = 0
        for time_key in general.subject_seconds_dict:
            update_timer(general.subject_seconds_dict[time_key], self.subject_label_list[iterator][1])
            iterator += 1

        iterator = 0
        for time_key in general.subtopic_seconds_dict:
            update_timer(general.subtopic_seconds_dict[time_key], self.subtopic_label_list[iterator][1])
            iterator += 1

        iterator = 0
        for time_key in general.project_seconds_dict:
            update_timer(general.project_seconds_dict[time_key], self.project_label_list[iterator][1])
            iterator += 1

        self.update_timer_button(general, timer)

    @staticmethod
    def collect_time_field_seconds(general):
        def get_seconds_difference():
            return int((end_time - start_time).total_seconds())

        def seperate_times(curr_dict):
            if itercount == 0:
                curr_dict["daily_seconds"] += get_seconds_difference()
            if itercount == 1:
                curr_dict["weekly_seconds"] += get_seconds_difference()
            if itercount == 2:
                curr_dict["monthly_seconds"] += get_seconds_difference()
            if itercount == 3:
                curr_dict["yearly_seconds"] += get_seconds_difference()

        all_times = db_manage.get_times()
        itercount = 0
        for sublist in all_times:
            for uid, user_id, subject, subtopic, project, start_time, end_time in sublist:
                # print(314, subject, subtopic, project, start_time, end_time)
                if subject == general.subject:
                    seperate_times(general.subject_seconds_dict)
                if subtopic == general.subtopic:
                    seperate_times(general.subtopic_seconds_dict)
                if project == general.project:
                    seperate_times(general.project_seconds_dict)
            itercount += 1
