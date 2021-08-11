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

        self.subjects_dropdown = ""
        self.subtopics_dropdown = ""
        self.project_dropdown = ""

        self.subject_options = ["None"]
        self.subtopic_options = ["None"]
        self.project_options = ["None"]

        self.subject_seconds = 0
        self.subtopic_seconds = 0
        self.project_seconds = 0

        self.subject = ""
        self.subtopic = ""
        self.project = ""


class GuiWindow:
    def __init__(self, master, general, timer):  #
        super(GuiWindow, self).__init__()
        self.master = master
        self.master.title("Motivation Time Tracking App")

        self.notebook = ttk.Notebook(self.master)
        # somehow now specifying that all the stuff in tab1 needs to go into Frame1
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
