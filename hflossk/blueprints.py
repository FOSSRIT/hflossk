import os

from flask import Blueprint, render_template

homework = Blueprint('homework', __name__, template_folder='templates')
lectures = Blueprint('lectures', __name__, template_folder='templates')
quizzes = Blueprint('quizzes', __name__, template_folder='templates')


@homework.route('/', defaults={'page': 'index'})
@homework.route('/<page>')
def display_homework(page):
    if page == 'index':
        hws = os.listdir(os.path.join(os.path.split(__file__)[0],
                                      'static', 'hw'))
        hws.extend(os.listdir(os.path.join(os.path.split(__file__)[0],
                                           'templates', 'hw')))
        hws = [hw for hw in sorted(hws) if not hw == "index.html"]
    else:
        hws = None

    return render_template('hw/{}.html'.format(page), hws=hws)


@lectures.route('/', defaults={'page': 'index'})
@lectures.route('/<page>')
def display_lecture(page):
    if page == 'index':
        lecture_notes = os.listdir(os.path.join(os.path.split(__file__)[0],
                                                'templates', 'lectures'))
        lecture_notes = [note for note in sorted(lecture_notes)
                         if not note == "index.html"]
    else:
        lecture_notes = None

    return render_template('lectures/{}.html'.format(page),
                           lectures=lecture_notes)


@quizzes.route('/<quiz_num>')
def show_quiz(quiz_num):
    return render_template('quiz/{}.html'.format(quiz_num))
