import os
import sqlite3

sql_file = 'Motivation_App.sqlite'


def check_if_db_exists():
    if not os.path.exists(sql_file):
        conn = sqlite3.connect(sql_file)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE Main_Subjects (Subject STRING PRIMARY KEY, '
            'Seconds INTEGER)')
        conn.commit()
        conn.close()


def check_existing_tables():
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    string_tables = sql_tables.fetchall()
    table_list = []
    for i in string_tables:
        table_list.append(i[0])
    if "Sub_Subject" not in table_list:
        c.execute("CREATE TABLE Sub_Subject (Sub_Subject STRING PRIMARY KEY, "
                  "Link STRING)")
    if "Questions" not in table_list:
        c.execute("CREATE TABLE Questions (Question_Number INTEGER PRIMARY KEY, "
                  "Question STRING, Link STRING)")
    if "Answers" not in table_list:
        c.execute("CREATE TABLE Answers (Question_Number INTEGER PRIMARY KEY, "
                  "Answer STRING)")
    if "Incorrect_Answers" not in table_list:
        c.execute("CREATE TABLE Incorrect_Answers (Question_Number INTEGER PRIMARY KEY, "
                  "Incorrect_Answer STRING)")
    if "Daily_Study" not in table_list:
        c.execute(
            "CREATE TABLE Daily_Study (Subject STRING, Sub_Subject STRING,"
            " Date STRING, Daily_Seconds)")
    conn.commit()
    conn.close()


def check_subjects(subject):
    subject = str(subject).lower()
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_subjects = c.execute('SELECT Subject FROM Main_Subjects')
    string_subjects = sql_subjects.fetchall()
    list_subjects = []
    for i in string_subjects:
        list_subjects.append(i[0])

    if subject not in list_subjects:
        print('Your current list of subjects is: ', list_subjects, 'would you like to add', subject,
              '? (Please enter y or n)')
        yes_no = input()
        while True:
            if yes_no == 'y':
                enter_subject(subject)
                break
            elif yes_no == 'n':
                pass
            else:
                yes_no = input('Please enter y or n')
    conn.close()
    return subject


def enter_subject(subject):
    subject = str(subject).lower()
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute('INSERT INTO Main_Subjects(Subject, Seconds) Values(?, ?)', (subject, 0))
    conn.commit()
    conn.close()


def update_subject(subject, new_seconds):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_old_seconds = c.execute('SELECT Seconds FROM Main_Subjects WHERE Subject = ?', (subject,))
    string_old_seconds = sql_old_seconds.fetchone()
    if string_old_seconds is None:
        enter_subject(subject)
    else:
        old_hours = round(int(string_old_seconds[0])/3600, 2)
        new_total_seconds = int(new_seconds) + int(string_old_seconds[0])
        c.execute("UPDATE Main_Subjects Set Seconds = ? WHERE Subject = ?", (new_total_seconds, subject))
    conn.commit()
    conn.close()


def enter_minor_subject(sub_subject, link):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("INSERT INTO Sub_Subject (Sub_Subject, Link) Values(?, ?)", (sub_subject.lower(), link.lower()))
    conn.commit()
    conn.close()


def minor_sub_belongs_to():
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_major_subjects = c.execute("SELECT Subject FROM Main_Subjects")
    string_major_subjects = sql_major_subjects.fetchall()
    list_major_subjects = []
    for i in string_major_subjects:
        list_major_subjects.append(i[0])
    conn.close()
    return list_major_subjects


def check_minor_major_link(sub_subject, link):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_link_check = c.execute('SELECT Sub_Subject FROM Sub_Subject WHERE Sub_Subject = ? AND WHERE Link = ?',
                               (sub_subject, link))
    string_link_check = sql_link_check.fetchone()
    if string_link_check[0] is not None:
        pass
    else:
        enter_minor_subject(sub_subject, link)
    conn.close()


def daily_study_entry(subject, sub_subject, curr_date, session_seconds):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_day_check = c.execute('SELECT Date FROM Daily_Study WHERE Date = ? AND Subject = ? AND Sub_Subject = ?',
                              (str(curr_date), subject, sub_subject))
    string_day_check = sql_day_check.fetchone()
    if string_day_check is None:
        c.execute("INSERT INTO Daily_Study (Subject, Sub_Subject, Date, Daily_Seconds) Values(?, ?, ?, ?)",
                  (subject.lower(), sub_subject.lower(), curr_date, session_seconds))
    else:
        sql_old_daily_seconds = c.execute("SELECT Daily_Seconds FROM Daily_Study "
                                          "WHERE Date = ? AND Subject = ? AND Sub_Subject = ?",
                                          (curr_date, subject, sub_subject))
        string_old_daily_seconds = sql_old_daily_seconds.fetchone()
        added_seconds = float(string_old_daily_seconds[0]) + float(session_seconds)

        c.execute("UPDATE Daily_Study SET Daily_Seconds = ? WHERE Date = ? AND Subject = ? AND Sub_Subject = ?",
                  (str(added_seconds), curr_date, subject.lower(), sub_subject.lower()))
    conn.commit()
    conn.close()
