import time
import datetime
from motivationapp import db_manage

mva_start_stop = 'mva_start_stop.txt'

class TimeCheck:
    def __init__(self):
        self.start = 0
        self.end = 0
        self.subject = ''

    def time_start(self):
        return self.start

    def time_end(self):
        return self.end

    def time_diff(self):
        return self.end - self.start

    def subject_string(self):
        return self.subject


def what_subject():
    subject = input('What major subject are you going to be focusing on today?\n')
    checking = input('Is this the subject you would like to focus on? - ' + subject + ' (y or n)\n')
    while True:
        if checking == 'y':
            string_sub = subject
            subject = TimeCheck()
            subject.subject = string_sub
            return subject
        elif checking == 'n':
            subject = input('What major subject are you going to be focusing on today?\n')
            checking = input('Is this the subject you would like to focus on? - ' + subject + ' (y or n)\n')
        else:
            print('It looks like you gave an invalid answer, please type y for yes or n for no\n')
            checking = input('Is this the subject you would like to focus on? - ' + subject + ' (y or n)\n')


def minor_subject(main_subject):
    sub_check = input('Do you have a minor subject you want to focus on? (y/n)\n')
    while True:
        if sub_check == 'y':
            minor_sub = input('What is the minor subject?\n')
            minor_check = input('Is ' + minor_sub + ' the correct minor subject? (y/n)\n')
            if minor_check == 'y':
                subject_list = db_manage.minor_sub_belongs_to()
                print("This is your list of major subjects - " + str(subject_list))
                link_subject = main_subject
                print(link_subject)
                print(subject_list)
                if link_subject in subject_list:
                    return minor_sub
                else:
                    db_manage.check_subjects(link_subject)
                    db_manage.check_minor_major_link(minor_sub, link_subject)
                    return minor_sub
            else:
                minor_sub = input('What is the minor subject?')
        elif sub_check == 'n':
            subject_list = db_manage.minor_sub_belongs_to()
            if main_subject not in subject_list:
                db_manage.enter_subject(main_subject)
            return 'None'
        else:
            sub_check = input('You did not enter y or n please try again')


def subject_start(class_object):
    user_inp = input('Would you like to start the timer? (y or n)\n')
    while True:
        if user_inp == 'y':
            print('You have started at ' + str(datetime.datetime.now()) + '\n')
            class_object.start = time.time()
            break
        elif 'n' in user_inp:
            user_inp = input('Please enter y when ready to start\n')
        else:
            user_inp = input('Would you like to start the timer? (y for yes or n for no)\n')


def main():
    curr_date = str(datetime.datetime.now().date())
    with open(mva_start_stop, 'w') as f:
        f.write('start')
    db_manage.check_if_db_exists()
    db_manage.check_existing_tables()
    our_subject = what_subject()
    our_minor = minor_subject(our_subject.subject.lower())
    print('minor subject is - ' + str(our_minor))
    subject_start(class_object=our_subject)

    print('Would you like to finish your session? (end/n/start/stop)\n')
    finish = input()
    while True:
        if finish == 'end':
            our_subject.end = time.time()
            with open(mva_start_stop, 'r') as f:
                status = f.readline()
            if status == 'start':
                print('This is our start time', our_subject.start)
                print('This is our end time', our_subject.end)
                print('This is the time spent on the subject in hours - ', round(our_subject.time_diff()/3600, 2))
                db_manage.update_subject(subject=our_subject.subject.lower(), new_seconds=our_subject.time_diff())
                db_manage.daily_study_entry(sub_subject=our_minor.lower(), subject=str(our_subject.subject).lower(),
                                            curr_date=curr_date, session_seconds=round(our_subject.time_diff(), 2))
                break
            else:
                break
        elif finish == 'n':
            pass
        elif finish == 'start' or finish == 'stop':
            if finish == 'start':
                with open(mva_start_stop, 'r') as f:
                    status = f.readline()
                if status.strip() == 'start':
                    print('You must stop first before you can start again')
                    finish = input()
                elif status == 'stop':
                    print('Restarting')
                    our_subject.start = time.time()
                    with open(mva_start_stop, 'w') as f:
                        f.write('start')
                    finish = input()
            elif finish == 'stop':
                our_subject.end = time.time()
                print('stopcheck')
                print('This is our start time', our_subject.start)
                print('This is our end time', our_subject.end)
                print('This is the time spent on the subject in hours - ', round(our_subject.time_diff() / 3600, 2))
                db_manage.update_subject(subject=our_subject.subject.lower(), new_seconds=our_subject.time_diff())
                db_manage.daily_study_entry(sub_subject=our_minor.lower(), subject=str(our_subject.subject).lower(),
                                            curr_date=curr_date, session_seconds=round(our_subject.time_diff(), 2))
                with open(mva_start_stop, 'w') as f:
                    f.write('stop')
                finish = input()
        else:
            print('Please enter start, stop, y, or n')


main()
