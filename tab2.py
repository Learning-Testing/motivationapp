from datetime import datetime
from tkinter import ttk

import db_manage


class Frame2(ttk.Frame):
    def __init__(self, container, general):
        super().__init__()

        self.day_week_month_year_data = []
        self.label_strings = ["Total time for today is: ",
                              "Total time for this week is: ",
                              "Total time for this month is: ",
                              "Total time for this year is: "]

        """self.day_times = handle_subjects_times(self.base_data[0])
        self.week_times = handle_subjects_times(self.base_data[1])
        self.month_times = handle_subjects_times(self.base_data[2])
        self.year_times = handle_subjects_times(self.base_data[3])

        day_string = self.day_str + self.day_times[0]
        self.day_label = ttk.Label(self, text=day_string)
        self.day_label.grid(column=0, row=1, sticky="w")
        day_data = self.day_times[1]
        self.day_data_label = ttk.Label(self, text=day_data)
        self.day_data_label.grid(column=1, row=2, sticky="w")

        week_string = self.week_str + self.week_times[0]
        self.week_label = ttk.Label(self, text=week_string)
        self.week_label.grid(column=0, row=3, sticky="w")
        week_data = self.week_times[1]

        month_string = self.month_str + self.month_times[0]
        self.month_label = ttk.Label(self, text=month_string)
        self.month_label.grid(column=0, row=5, sticky="w")

        year_string = self.year_str + self.year_times[0]
        self.year_label = ttk.Label(self, text=year_string)
        self.year_label.grid(column=0, row=7, sticky="w")

        self.refresh_button = ttk.Button(self, text="Refresh", command=lambda: self.refresh_data(general))"""

    def display_data(self):
        handle_subjects_times(collect_data(), self.day_week_month_year_data)
        column_counter = 0
        row_counter = 0
        curr_iter = 0

        for sublist in self.day_week_month_year_data:
            for i in range(len(sublist)):
                time_data = sublist[column_counter]
                if column_counter == 0:
                    text = self.label_strings[curr_iter] + time_data
                else:
                    text = time_data

                row_counter += 1

                curr_label = ttk.Label(self, text=text)
                curr_label.grid(column=column_counter, row=row_counter, sticky="w")

                if column_counter == 0:
                    column_counter += 1
                else:
                    column_counter -= 1
            curr_iter += 1

    """def refresh_data(self, general):
        general.subject_seconds += 0"""


def collect_data():
    all_data = db_manage.get_times()
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


def handle_subjects_times(str_data, day_week_month_year_list):
    subject_classes = {}

    for sublist in str_data:
        for i in sublist:
            subject = i[2]
            subtopic = i[3]
            project = i[4]
            start_time = i[5]
            start_time_dateobject = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S.%f')
            end_time = i[6]
            end_time_dateobject = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S.%f')
            seconds = int((end_time_dateobject - start_time_dateobject).total_seconds())

            if subject not in subject_classes:
                subject_classes[subject] = DataTracking(subject)
                subject_classes[subject].check_subtopic(subtopic, project, seconds)
            else:
                subject_classes[subject].check_subtopic(subtopic, project, seconds)

        # print(172, subject_classes)
        total_time = 0
        individual_data = ""
        for subject in subject_classes:
            # print(174, i)
            for subtopic in subject_classes[subject].subtopics_dict:
                for project in subject_classes[subject].subtopics_dict[subtopic]:
                    dict_seconds = subject_classes[subject].subtopics_dict[subtopic][project]
                    subject_hours, subject_remainder = divmod(dict_seconds, 3600)
                    subject_minutes, subject_seconds = divmod(subject_remainder, 60)
                    individual_data += (f"{subject} - {subtopic} - {project} = "
                                        f"{subject_hours} hours, "
                                        f"{subject_minutes} minutes\n")
                    total_time += dict_seconds
        total_hours, total_remainder = divmod(total_time, 3600)
        total_minutes, total_seconds = divmod(total_remainder, 60)
        constructed_str = f"{total_hours} hours, {total_minutes} minutes"
        day_week_month_year_list.append([constructed_str, individual_data])

