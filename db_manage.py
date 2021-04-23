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
    conn = sqlite3.connect(sql_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    sql_tables = c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    string_tables = sql_tables.fetchall()
    table_list = []
    for i in string_tables:
        table_list.append(i[0])

    if "quiz_qa" not in table_list:
        c.execute("CREATE TABLE quiz_qa(id INTEGER PRIMARY KEY, user_id INTEGER, "
                  "question_number INTEGER, question STRING, answer STRING)")
    if "daily_study" not in table_list:
        c.execute("CREATE TABLE daily_study(id INTEGER PRIMARY KEY, user_id INTEGER, subject STRING, "
                  "subtopic STRING, project STRING, start_time TIMESTAMP, end_time TIMESTAMP)")
    if "quiz_data" not in table_list:
        c.execute("CREATE TABLE quiz_data(id INTEGER PRIMARY KEY, user_id INTEGER, "
                  "question_number INTEGER, selected_answer STRING)")
    conn.commit()
    conn.close()


def daily_study_entry(subject, subtopic, project, start_time, end_time):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("INSERT INTO Daily_Study (user_id, subject, subtopic, project, start_time, end_time) "
              "VALUES (?, ?, ?, ?, ?, ?)", (1,
                                            subject,
                                            subtopic,
                                            project,
                                            start_time,
                                            end_time))
    conn.commit()
    conn.close()


def options_from_sql(general):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_main_subjects = c.execute("SELECT DISTINCT subject FROM daily_study").fetchall()
    sql_sub_subjects = c.execute("SELECT DISTINCT subtopic FROM daily_study").fetchall()
    sql_projects = c.execute("SELECT DISTINCT project FROM daily_study").fetchall()
    conn.close()

    for i in sql_main_subjects:
        general.subject_options.append(i[0])
    for i in sql_sub_subjects:
        general.subtopic_options.append(i[0])
    for i in sql_projects:
        general.project_options.append(i[0])

    sorted(general.subject_options)
    sorted(general.subtopic_options)
    sorted(general.project_options)


def seconds_for_item(general):
    conn = sqlite3.connect(sql_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    sql_subject_seconds = c.execute('SELECT '
                                    'start_time as "[timestamp]", '
                                    'end_time as "[timestamp]" '
                                    'FROM daily_study WHERE subject=?',
                                    (general.subject,))
    if sql_subject_seconds is not None:
        subject_seconds_list = sql_subject_seconds.fetchall()
        for start_date, end_date in subject_seconds_list:
            general.subject_seconds += int((end_date - start_date).total_seconds())

    sql_subtopic_seconds = c.execute('SELECT '
                                     'start_time as "[timestamp]", '
                                     'end_time as "[timestamp]" '
                                     'FROM daily_study WHERE subtopic=?',
                                     (general.subtopic,))
    if sql_subtopic_seconds is not None:
        subtopic_seconds_list = sql_subtopic_seconds.fetchall()
        for start_date, end_date in subtopic_seconds_list:
            general.subtopic_seconds += int((end_date - start_date).total_seconds())

    sql_project_seconds = c.execute('SELECT '
                                    'start_time as "[timestamp]", '
                                    'end_time as "[timestamp]" '
                                    'FROM daily_study WHERE project=?',
                                    (general.project,))
    if sql_project_seconds is not None:
        project_seconds_list = sql_project_seconds.fetchall()
        for start_date, end_date in project_seconds_list:
            general.project_seconds += int((end_date - start_date).total_seconds())

    conn.close()
