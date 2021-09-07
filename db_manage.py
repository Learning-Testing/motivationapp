import os
import sqlite3

sql_file = 'testing.sqlite'


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
                  "question_number INTEGER, question STRING, answer STRING, incorrect1 STRING, incorrect2 STRING, "
                  "incorrect3 STRING, subject STRING, subtopic STRING, project STRING, "
                  "correct_answer_reason STRING, resources STRING)")
        # add , correct_answer_reason STRING and a resources? To help understand where knowledge came from/how it works
    if "daily_study" not in table_list:
        c.execute("CREATE TABLE daily_study(id INTEGER PRIMARY KEY, user_id INTEGER, subject STRING, "
                  "subtopic STRING, project STRING, start_time TIMESTAMP, end_time TIMESTAMP, event STRING)")
    if "quiz_data" not in table_list:
        c.execute("CREATE TABLE quiz_data(id INTEGER PRIMARY KEY, user_id INTEGER, "
                  "question_number INTEGER, selected_answer STRING, "
                  "session INTEGER, start_time TIMESTAMP, end_time TIMESTAMP)")
    conn.commit()
    conn.close()


def daily_study_entry(subject, subtopic, project, event, start_time, end_time):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    if subject == "None" and subtopic == "None" and project == "None" and event == "None":
        pass
    else:
        c.execute("INSERT INTO Daily_Study (user_id, subject, subtopic, project, start_time, end_time, event) "
                  "VALUES (?, ?, ?, ?, ?, ?, ?)", (1,
                                                   subject,
                                                   subtopic,
                                                   project,
                                                   start_time,
                                                   end_time,
                                                   event))
    conn.commit()
    conn.close()


def options_from_sql(general):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    sql_main_subjects = c.execute("SELECT DISTINCT subject FROM daily_study").fetchall()
    sql_sub_subjects = c.execute("SELECT DISTINCT subtopic FROM daily_study").fetchall()
    sql_projects = c.execute("SELECT DISTINCT project FROM daily_study").fetchall()
    sql_events = c.execute("SELECT DISTINCT event FROM daily_study").fetchall()
    conn.close()

    for i in sql_main_subjects:
        if i[0] != "None":
            general.subject_options.append(i[0])
    for i in sql_sub_subjects:
        if i[0] != "None":
            general.subtopic_options.append(i[0])
    for i in sql_projects:
        if i[0] != "None":
            general.project_options.append(i[0])
    for i in sql_events:
        if i[0] != "None":
            general.event_options.append(i[0])

    general.subject_options = sorted(general.subject_options)
    general.subtopic_options = sorted(general.subtopic_options)
    general.project_options = sorted(general.project_options)
    general.event_options = sorted(general.event_options)


def total_seconds_for_item(general):
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
            general.subject_seconds_dict["total_seconds"] += int((end_date - start_date).total_seconds())

    sql_subtopic_seconds = c.execute('SELECT '
                                     'start_time as "[timestamp]", '
                                     'end_time as "[timestamp]" '
                                     'FROM daily_study WHERE subtopic=?',
                                     (general.subtopic,))
    if sql_subtopic_seconds is not None:
        subtopic_seconds_list = sql_subtopic_seconds.fetchall()
        for start_date, end_date in subtopic_seconds_list:
            general.subtopic_seconds_dict["total_seconds"] += int((end_date - start_date).total_seconds())

    sql_project_seconds = c.execute('SELECT '
                                    'start_time as "[timestamp]", '
                                    'end_time as "[timestamp]" '
                                    'FROM daily_study WHERE project=?',
                                    (general.project,))

    if sql_project_seconds is not None:
        project_seconds_list = sql_project_seconds.fetchall()
        for start_date, end_date in project_seconds_list:
            general.project_seconds_dict["total_seconds"] += int((end_date - start_date).total_seconds())

    sql_event_seconds = c.execute('SELECT '
                                  'start_time as "[timestamp]", '
                                  'end_time as "[timestamp]" '
                                  'FROM daily_study WHERE event=?',
                                  (general.event,))

    if sql_event_seconds is not None:
        event_seconds_list = sql_event_seconds.fetchall()
        for start_date, end_date in event_seconds_list:
            general.event_seconds_dict["total_seconds"] += int((end_date - start_date).total_seconds())

    conn.close()


def get_times(last_id):
    conn = sqlite3.connect(sql_file, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    c = conn.cursor()
    c.execute("SELECT * FROM daily_study WHERE DATE(start_time) == "
              "DATE('now', 'localtime') AND id > ?;", (last_id,))
    # -- current day
    str_day_data = c.fetchall()

    c.execute("SELECT * FROM daily_study WHERE DATE(start_time) >= "
              "DATE('now', 'localtime', 'weekday 0', '-7 days') AND id > ?;", (last_id,))
    # -- current week
    str_week_data = c.fetchall()

    c.execute("SELECT * FROM daily_study WHERE start_time BETWEEN DATE('now', 'start of month') AND "
              "DATE('now', 'localtime', 'start of month', '+1 month', '-1 day') AND id > ?;", (last_id,))
    # -- current month
    str_month_data = c.fetchall()

    c.execute("SELECT * FROM daily_study WHERE start_time BETWEEN DATE('now', 'start of year') AND "
              "DATE('now', 'localtime', 'start of year', '+12 month', '-1 day') AND id > ?;", (last_id,))
    # -- current year
    str_year_data = c.fetchall()
    conn.close()

    return [str_day_data, str_week_data, str_month_data, str_year_data]


def copy_data():
    conn_testing = sqlite3.connect(sql_file)
    c_testing = conn_testing.cursor()
    conn_live = sqlite3.connect("Motivation_App.sqlite")
    c_live = conn_live.cursor()

    c_live.execute("SELECT * FROM daily_study")
    all_data = c_live.fetchall()
    conn_live.close()

    for (num_id, user_id, subject, subtopic, project, start_time, end_time, event) in all_data:
        c_testing.execute("INSERT INTO daily_study VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                          (num_id, user_id, subject, subtopic, project, start_time, end_time, event))
    conn_testing.commit()
    conn_testing.close()


def get_distinct_sets():
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("SELECT DISTINCT subject, subtopic, project FROM daily_study")
    sets = c.fetchall()
    conn.close()

    new_sets = []
    for i in sets:
        new_sets.append([i[0], i[1], i[2]])
    return new_sets


def add_quiz_question_data(question,
                           answer,
                           incorrect1,
                           incorrect2,
                           incorrect3,
                           subject,
                           subtopic,
                           project,
                           answer_reason,
                           resources):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("INSERT INTO quiz_qa "
              "(user_id, "
              "question, "
              "answer, "
              "incorrect1, "
              "incorrect2, "
              "incorrect3, "
              "subject, "
              "subtopic, "
              "project, "
              "correct_answer_reason, "
              "resources)"
              " VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
              (1,
               question,
               answer,
               incorrect1,
               incorrect2,
               incorrect3,
               subject,
               subtopic,
               project,
               answer_reason,
               resources))
    conn.commit()
    conn.close()


def get_questions(limit, subject, subtopic, project):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    params = []
    base_select = "SELECT * FROM quiz_qa WHERE "

    joiner = False
    if subject != "None" and subtopic != "None" or \
        subject != "None" and project != "None" or \
            subtopic != "None" and project != "None":
        joiner = True

    if subject is not None:
        base_select += "subject=? "
        if joiner:
            base_select += "AND "
        params.append(subject)
    if subtopic is not None:
        base_select += "subtopic=? "
        if joiner:
            base_select += "AND "
        params.append(subtopic)
    if project is not None:
        base_select += "project=? "
        params.append(project)

    params.append(limit)
    params = tuple(params)

    last_part = "ORDER BY RANDOM() LIMIT ?"
    full_query = base_select + last_part

    c.execute(full_query, params)
    data = c.fetchall()
    conn.close()
    return data


def write_to_quiz_data(question_num, selected_answer, session_num, start_time, end_time):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("INSERT INTO quiz_data (user_id, question_number, selected_answer, session, start_time, end_time) "
              "VALUES (?, ?, ?, ?, ?, ?)", (1, question_num, selected_answer, session_num, start_time, end_time))
    conn.commit()
    conn.close()


def get_session_num():
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("SELECT IFNULL(MAX(session), 1) FROM quiz_data")
    num = c.fetchone()[0]
    conn.close()

    return num


def get_results(session_num):
    conn = sqlite3.connect(sql_file)
    c = conn.cursor()
    c.execute("""
              SELECT 
                quiz_qa.question, 
                quiz_qa.answer, 
                quiz_data.selected_answer, 
                quiz_qa.correct_answer_reason, 
                quiz_qa.resources
              FROM 
                quiz_qa
              INNER JOIN quiz_data ON quiz_qa.id = quiz_data.question_number
              WHERE quiz_data.session = ?
              """, (session_num,))
    data = c.fetchall()
    conn.close()

    return data
