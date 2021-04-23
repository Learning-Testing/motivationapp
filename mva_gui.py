import tkinter as tk
import db_manage
import datetime


class TimeCheck:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()
        self.total_time_diff = 0

    def set_time_start(self):
        self.start_time = datetime.datetime.now()

    def time_diff(self, end_time):
        self.end_time = end_time
        full_time = int((end_time - self.start_time).total_seconds())
        self.total_time_diff += full_time


class General:
    def __init__(self):
        self.start_button_press = False
        self.check_if_started = False
        self.subject_options = []
        self.subtopic_options = []
        self.project_options = []
        self.subject_seconds = 0
        self.subtopic_seconds = 0
        self.project_seconds = 0

        self.subject = ""
        self.subtopic = ""
        self.project = ""


class GuiWindow:

    def __init__(self, master, general, timer):
        self.master = master
        self.master.title("Motivation Time Tracking App")

        self.mainframe = tk.Frame(master)
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.pack(pady=100, padx=100)

        self.seconds_passed = int((timer.end_time - timer.start_time).total_seconds())
        self.subject_timer = tk.StringVar()
        self.subject_timer.set("")
        self.subtopic_timer = tk.StringVar()
        self.subtopic_timer.set("")
        self.project_timer = tk.StringVar()
        self.project_timer.set("")

        self.subject_options = general.subject_options
        self.subject = ""
        self.subject_textbox_label = tk.Label(self.mainframe, text="Enter a new subject")
        self.subject_textbox = tk.Text(self.mainframe, height=1, width=12)
        self.subjects_dropdown = ""
        self.subject_label = tk.Label(self.mainframe, text="Choose a subject")
        self.subject_seconds = 0
        self.subject_timer_label = tk.Label(self.mainframe, textvariable=self.subject_timer)
        self.subject_choice = tk.StringVar(self.master)

        self.subtopic_options = general.subtopic_options
        self.subtopic = ""
        self.subtopic_textbox_label = tk.Label(self.mainframe, text="Enter a new subtopic")
        self.subtopic_textbox = tk.Text(self.mainframe, height=1, width=12)
        self.subtopics_dropdown = ""
        self.subtopic_label = tk.Label(self.mainframe, text="Choose a subtopic")
        self.subtopic_seconds = 0
        self.subtopic_timer_label = tk.Label(self.mainframe, textvariable=self.subtopic_timer)
        self.subtopic_choice = tk.StringVar(self.master)

        self.project_options = general.project_options
        self.project = ""
        self.project_textbox_label = tk.Label(self.mainframe, text="Enter a new project")
        self.project_textbox = tk.Text(self.mainframe, height=1, width=12)
        self.project_dropdown = ""
        self.project_label = tk.Label(self.mainframe, text="Choose a project")
        self.project_seconds = 0
        self.project_timer_label = tk.Label(self.mainframe, textvariable=self.project_timer)
        self.project_choice = tk.StringVar(self.master)

        self.add_button = tk.Button(self.mainframe, text="Add",
                                    command=lambda: self.add_text_to_options(general, timer))
        self.description_label = tk.Label(self.mainframe,
                                          text=f"{general.subject}, {general.subtopic}, {general.project}")

        self.call_display(general, timer)
        self.update_timers(general, timer)
        # self.update_timer_button(general, timer)

    def call_display(self, general, timer):
        self.subject_options_func()
        self.subtopic_options_func()
        self.project_options_func()
        self.update_timer_button(general, timer)
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

        self.subject_timer_label.grid_remove()
        self.subtopic_timer_label.grid_remove()
        self.project_timer_label.grid_remove()

        self.add_button.grid()
        self.description_label.grid_remove()

    def subject_options_func(self):
        subject_column = 1
        print(self.subject_options)
        if self.subject_options is None or len(self.subject_options) == 0:
            self.subject_choice.set("")
            self.subjects_dropdown = tk.OptionMenu(self.mainframe, self.subject_choice, "")
        else:
            self.subject_choice.set(self.subject_options[0])
            self.subjects_dropdown = tk.OptionMenu(self.mainframe, self.subject_choice, *self.subject_options)

        self.subject_textbox_label.grid(row=2, column=subject_column)
        self.subject_textbox.grid(row=3, column=subject_column)

        self.subject_label.grid(row=4, column=subject_column)
        self.subjects_dropdown.grid(row=5, column=subject_column)

    def subtopic_options_func(self):
        subtopic_column = 2

        if len(self.subtopic_options) == 0:
            self.subtopic_choice.set("")
            self.subtopics_dropdown = tk.OptionMenu(self.mainframe, self.subtopic_choice, "")
        else:
            self.subtopic_choice.set(self.subtopic_options[0])
            self.subtopics_dropdown = tk.OptionMenu(self.mainframe, self.subtopic_choice, *self.subtopic_options)

        self.subtopic_textbox_label.grid(row=2, column=subtopic_column)
        self.subtopic_textbox.grid(row=3, column=subtopic_column)

        self.subtopic_label.grid(row=4, column=subtopic_column)
        self.subtopics_dropdown.grid(row=5, column=subtopic_column)

    def project_options_func(self):
        project_column = 3

        if len(self.project_options) == 0:
            self.project_choice.set("")
            self.project_dropdown = tk.OptionMenu(self.mainframe, self.project_choice, "")
        else:
            self.project_choice.set(self.project_options[0])
            self.project_dropdown = tk.OptionMenu(self.mainframe, self.project_choice, *self.project_options)

        self.project_textbox_label.grid(row=2, column=project_column)
        self.project_textbox.grid(row=3, column=project_column)

        self.project_label.grid(row=4, column=project_column)
        self.project_dropdown.grid(row=5, column=project_column)

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

                self.description_label = tk.Label(self.mainframe,
                                                  text=f"{general.subject}, {general.subtopic}, {general.project}")

                self.hide_labels()

            else:
                start_stop_button.config(text="Start")

                self.show_labels()
                db_manage.daily_study_entry(subject=general.subject,
                                            subtopic=general.subtopic,
                                            project=general.project,
                                            start_time=timer.start_time,
                                            end_time=timer.end_time)

        start_stop_button = tk.Button(self.mainframe, text="Start", command=update_button)
        start_stop_button.grid(row=4, column=0)

    def update_timers(self, general, timer):
        if general.start_button_press is True:

            timer.end_time = datetime.datetime.now()

            self.subject_timer_label.grid(row=4, column=1)
            self.subtopic_timer_label.grid(row=4, column=2)
            self.project_timer_label.grid(row=4, column=3)

            self.seconds_passed = int((timer.end_time - timer.start_time).total_seconds())

            self.refresh_timer(general)
            self.mainframe.after(1000, self.update_timers, general, timer)

    def refresh_timer(self, general):
        subject_hours, subject_remainder = divmod(self.seconds_passed + general.subject_seconds, 3600)
        subject_minutes, subject_seconds = divmod(subject_remainder, 60)
        self.subject_timer.set(f"{subject_hours}:{subject_minutes}:{subject_seconds}")

        subtopic_hours, subtopic_remainder = divmod(self.seconds_passed + general.subtopic_seconds, 3600)
        subtopic_minutes, subtopic_seconds = divmod(subtopic_remainder, 60)
        self.subtopic_timer.set(f"{subject_hours}:{subtopic_minutes}:{subtopic_seconds}")

        project_hours, project_remainder = divmod(self.seconds_passed + general.project_seconds, 3600)
        project_minutes, project_seconds = divmod(project_remainder, 60)
        self.project_timer.set(f"{project_hours}:{project_minutes}:{project_seconds}")


def main():
    general = General()
    timer = TimeCheck()

    db_manage.check_if_db_exists()
    db_manage.check_existing_tables()
    db_manage.options_from_sql(general)

    root = tk.Tk()
    GuiWindow(root, general, timer)
    root.mainloop()


main()
