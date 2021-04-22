import tkinter as tk
import db_manage
import datetime


class TimeCheck:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.total_time_diff = 0
        self.subject = ''

    def set_time_start(self):
        self.start_time = datetime.datetime.now()

    def time_diff(self, end_time):
        full_time = int(end_time - self.start_time)
        self.total_time_diff += full_time


class General:
    def __init__(self):
        self.start_button_press = False
        self.start_button_text = "Start"
        self.counter = 0  # what is this counter for?

        self.subject_options = []
        self.subject = ""
        self.subject_textbox_label = ""
        self.subject_textbox = ""
        self.subjects_dropdown = ""
        self.subject_label = ""

        self.subtopic_options = []
        self.subtopic = ""
        self.subtopic_textbox_label = ""
        self.subtopic_textbox = ""
        self.subtopics_dropdown = ""
        self.subtopic_label = ""


class GuiWindow:

    def __init__(self, master, general, timer):
        self.master = master
        self.master.title("Motivation Time Tracking App")

        self.mainframe = tk.Frame(master)
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.pack(pady=100, padx=100)

        self.subject_options(general)
        self.subtopic_options(general)
        self.update_timer_button(general, timer)
        self.add_text_to_options(general)

    def subject_options(self, general):
        subject_column = 1
        subjecttype = tk.StringVar(self.master)
        if len(general.subject_options) == 0:
            subjecttype.set("")
            general.subjects_dropdown = tk.OptionMenu(self.mainframe, subjecttype, "")
        else:
            subjecttype.set(general.subject_options[0])
            general.subjects_dropdown = tk.OptionMenu(self.mainframe, subjecttype, *general.subject_options)

        general.subject_textbox_label = tk.Label(self.mainframe,
                                                 text="Enter a new subject").grid(row=2,
                                                                                  column=subject_column)
        general.subject_textbox = tk.Text(self.mainframe, height=2, width=10).grid(row=3, column=subject_column)

        general.subject_label = tk.Label(self.mainframe, text="Choose a subject").grid(row=4, column=subject_column)
        general.subjects_dropdown.grid(row=5, column=subject_column)

    def subtopic_options(self, general):
        subtopic_column = 2
        subtopictype = tk.StringVar(self.master)
        if len(general.subtopic_options) == 0:
            subtopictype.set("")
            general.subtopics_dropdown = tk.OptionMenu(self.mainframe, subtopictype, "")
        else:
            subtopictype.set(general.subtopic_options[0])
            general.subtopics_dropdown = tk.OptionMenu(self.mainframe, subtopictype, *general.subtopic_options)

        general.subtopic_textbox_label = tk.Label(self.mainframe,
                                                  text="Enter a new subtopic").grid(row=2,
                                                                                    column=subtopic_column)
        general.subtopic_textbox = tk.Text(self.mainframe, height=2, width=10).grid(row=3, column=subtopic_column)

        general.subtopic_label = tk.Label(self.mainframe, text="Choose a subtopic").grid(row=4, column=subtopic_column)
        general.subtopics_dropdown.grid(row=5, column=subtopic_column)

    def add_text_to_options(self, general):
        def get_textbox_data():
            subject_text_value = general.subject_textbox.get("1.0", "end-1c")
            if len(subject_text_value) > 0:
                general.subject_options.append(subject_text_value)
                general.subjects_dropdown.set(subject_text_value)
                general.subject_textbox.delete("1.0", "end-1c")

            subtopic_text_value = general.subtopic_textbox.get("1.0", "end-1c")
            if len(subject_text_value) > 0:
                general.subtopic_options.append(subtopic_text_value)
                general.subtopics_dropdown.set(subtopic_text_value)
                general.subtopic_textbox.delete("1.0", "end-1c")

        add_button = tk.Button(self.mainframe, text="Add", command=get_textbox_data)
        add_button.grid(row=2, column=0)

    def update_timer_button(self, general, timer):
        def change_text():
            if general.start_button_press is True:
                text = "Stop"
                timer.set_time_start()

                buttonlabel = tk.Label(self.mainframe, text=general.subject + ", " + general.subtopic)
                buttonlabel.grid(row=0, column=1)

                general.subject_textbox_label.grid_remove()
                general.subtopic_textbox_label.grid_remove()
                general.subject_textbox.grid_remove()
                general.subtopic_textbox.grid_remove()
                return text

            else:
                text = "Start"

                general.subject_textbox_label.grid()
                general.subtopic_textbox_label.grid()
                general.subject_textbox.grid()
                general.subtopic_textbox.grid()

                db_manage.daily_study_entry(subject=general.subject,
                                            subtopic=general.subtopic,
                                            start_time=timer.start_time,
                                            end_time=timer.end_time)

                return text

        b = tk.Button(self.mainframe, text=general.start_button_text, command=change_text)
        b.grid(row=4, column=0)

    def update_timer(self, general, timer):
        if general.start_button_press is True:
            timer.time_diff(datetime.datetime.now())
            subject_timer = tk.StringVar()
            subject_timer.set(timer.total_time_diff)


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
