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

    if "quiz_qa" not in table_list:
        c.execute("CREATE TABLE quiz_qa(id INTEGER AUTO_INCREMENT PRIMARY KEY, user_id INTEGER, "
                  "question_number INTEGER, question STRING, answer STRING)")
    if "daily_study" not in table_list:
        c.execute("CREATE TABLE daily_study(id INTEGER AUTO_INCREMENT PRIMARY KEY, user_id INTEGER, subject STRING, "
                  "subtopic STRING, project STRING, start_time DATETIME, end_time DATETIME)")
    if "quiz_data" not in table_list:
        c.execute("CREATE TABLE quiz_data(id INTEGER AUTO_INCREMENT PRIMARY KEY, user_id INTEGER, "
                  "question_number INTEGER, selected_answer STRING)")
    conn.commit()
    conn.close()


def daily_study_entry(subject, subtopic, start_time, end_time):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("INSERT INTO Daily_Study(user_id, subject, sub_topic, project, start_time, end_time)", (1,
                                                                                                      subject,
                                                                                                      subtopic,
                                                                                                      start_time,
                                                                                                      end_time))
    conn.commit()
    conn.close()


def options_from_sql(general):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_main_subjects = c.execute("SELECT DISTINCT subject FROM daily_study").fetchall()
    sql_sub_subjects = c.execute("SELECT DISTINCT subtopic FROM daily_study").fetchall()

    for i in sql_main_subjects:
        general.subject_options.append(i[0])
    for i in sql_sub_subjects:
        general.subtopic_options.append(i[0])
    conn.close()
