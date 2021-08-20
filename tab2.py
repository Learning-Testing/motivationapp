from tkinter import ttk
import tkinter as tk

import db_manage


class Frame2(ttk.Frame):
    def __init__(self, container, general):
        super().__init__()

        self.label_strings = ["Total time for today is: ",
                              "Total time for this week is: ",
                              "Total time for this month is: ",
                              "Total time for this year is: "]

        self.page_labels = []
        self.first_iter = False

        self.refresh_button = ttk.Button(self, text="Refresh", command=lambda: self.display_data())
        self.refresh_button.grid(column=0, row=0)

    def display_data(self):
        db_data = collect_data()
        print(23, db_data)
        parsed_data = handle_subjects_times(db_data)
        print(26, parsed_data)
        column_counter = 0
        row_counter = 1
        curr_iter = 0
        label_iter = 0

        for sublist in parsed_data:
            for i in range(len(sublist)):
                time_data = sublist[column_counter]
                #print(33, time_data)
                if self.first_iter is False:
                    textvar = tk.StringVar()
                    if column_counter == 0:
                        textvar.set(self.label_strings[curr_iter] + time_data)
                    else:
                        textvar.set(time_data)
                    row_counter += 1

                    curr_label = tk.Label(self, textvariable=textvar)
                    curr_label.grid(column=column_counter, row=row_counter, sticky="w")

                    self.page_labels.append([curr_label, textvar])

                else:
                    if column_counter == 0:
                        self.page_labels[label_iter][1].set(self.label_strings[curr_iter] + time_data)
                    else:
                        self.page_labels[label_iter][1].set(time_data)
                    label_iter += 1
                if column_counter == 0:
                    column_counter += 1
                else:
                    column_counter -= 1

            curr_iter += 1
        self.first_iter = True


def collect_data():
    all_data = db_manage.get_times(0)
    str_day_data = all_data[0]
    str_week_data = all_data[1]
    str_month_data = all_data[2]
    str_year_data = all_data[3]
    return [str_day_data, str_week_data, str_month_data, str_year_data]


class DataTracking:
    def __init__(self, subject):
        self.subject = subject
        self.subtopics_dict = {}

    def check_subtopic(self, subtopic, project, seconds):
        if subtopic not in self.subtopics_dict:
            self.subtopics_dict[subtopic] = {project: seconds}
        elif project not in self.subtopics_dict[subtopic]:
            self.subtopics_dict[subtopic][project] = seconds
        else:
            self.subtopics_dict[subtopic][project] += seconds


def handle_subjects_times(str_data):
    subject_classes = {}
    day_week_month_year_list = []

    # it needs to be nested like this, however this is what is likely causing the problem
    print(92, str_data)
    for sublist in str_data:
        for i in sublist:
            subject = i[2]
            subtopic = i[3]
            project = i[4]
            start_time = i[5]
            end_time = i[6]
            seconds = int((end_time - start_time).total_seconds())
            #print(100, subject, subtopic, project, seconds)
            if subject not in subject_classes:
                subject_classes[subject] = DataTracking(subject)
                subject_classes[subject].check_subtopic(subtopic, project, seconds)
            else:
                subject_classes[subject].check_subtopic(subtopic, project, seconds)

        total_time = 0
        individual_data = ""

        for subject in subject_classes:
            subtopic_dict = subject_classes[subject].subtopics_dict
            for subtopic in subtopic_dict:
                for project in subject_classes[subject].subtopics_dict[subtopic]:
                    dict_seconds = subject_classes[subject].subtopics_dict[subtopic][project]
                    subject_hours, subject_remainder = divmod(dict_seconds, 3600)
                    subject_minutes, subject_seconds = divmod(subject_remainder, 60)
                    individual_data += (f"{subject} - {subtopic} - {project} = "
                                        f"{subject_hours} hours, "
                                        f"{subject_minutes} minutes, "
                                        f"{subject_seconds} seconds\n")
                    total_time += dict_seconds
        total_hours, total_remainder = divmod(total_time, 3600)
        total_minutes, total_seconds = divmod(total_remainder, 60)
        constructed_str = f"{total_hours} hours, {total_minutes} minutes"
        day_week_month_year_list.append([constructed_str, individual_data])
        subject_classes = {}
    return day_week_month_year_list
