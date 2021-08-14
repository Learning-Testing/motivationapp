import tkinter as tk
from tkinter import ttk

import datetime

import db_manage
import tab1
import tab2


class TimeCheck:
    def __init__(self):
        self.start_time = datetime.datetime.now()
        self.end_time = datetime.datetime.now()

    def set_time_start(self):
        self.start_time = datetime.datetime.now()


class General:
    def __init__(self):
        self.start_button_press = False
        self.first_iter = True

        self.subjects_dropdown = ""
        self.subtopics_dropdown = ""
        self.project_dropdown = ""

        self.subject_options = ["None"]
        self.subtopic_options = ["None"]
        self.project_options = ["None"]

        # dict = {"daily_seconds": 0, "weekly_seconds": 0, "monthly_seconds": 0}, see create_seconds_dict()
        self.subject_seconds_dict = {}
        self.create_seconds_dict(self.subject_seconds_dict)
        self.subtopic_seconds_dict = {}
        self.create_seconds_dict(self.subtopic_seconds_dict)
        self.project_seconds_dict = {}
        self.create_seconds_dict(self.project_seconds_dict)

        self.subject = ""
        self.subtopic = ""
        self.project = ""

    @staticmethod
    def create_seconds_dict(dict_name):
        dict_name["subject_seconds"] = 0
        dict_name["daily_seconds"] = 0
        dict_name["weekly_seconds"] = 0
        dict_name["monthly_seconds"] = 0
        dict_name["yearly_seconds"] = 0
        dict_name["total_seconds"] = 0

    @staticmethod
    def breakdown_time(seconds):
        hours, remainder = divmod(seconds, 3600)
        minutes, handled_seconds = divmod(remainder, 60)
        return [hours, minutes, handled_seconds]


class GuiWindow:
    def __init__(self, master, general, timer):  #
        super(GuiWindow, self).__init__()
        self.master = master
        self.master.title(f"Motivation Time Tracking App                              File={db_manage.sql_file}")

        self.notebook = ttk.Notebook(self.master)
        self.tab1 = tab1.Frame1(self.notebook, general, timer)
        self.tab2 = tab2.Frame2(self.notebook, general)
        self.notebook.add(self.tab1, text="Track Time")
        self.notebook.add(self.tab2, text="Data Display")
        self.notebook.pack()

        def handle_display():
            if self.tab1.show_display_on_startup is False:
                self.tab1.call_display(general, timer)
                self.tab1.update_timer_button(general, timer)
                self.tab1.show_display_on_startup = True  # this needs to come after update_timer_button
                self.tab2.display_data()

        handle_display()


def main():
    general = General()
    timer = TimeCheck()

    db_manage.check_if_db_exists()
    db_manage.check_existing_tables()
    db_manage.options_from_sql(general)

    root = tk.Tk()
    GuiWindow(root, general, timer)  #
    root.mainloop()


main()
