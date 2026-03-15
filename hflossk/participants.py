import os
from datetime import date, datetime, timedelta

import hflossk
import yaml
from flask import Blueprint, render_template


participants_bp = Blueprint('participants_bp',
                            __name__,
                            template_folder='templates')


currentYear = str(date.today().year)
currentTerm = "fall" if date.today().month > 7 else "spring"


@participants_bp.route('/')
def participants_blank():
    """
    This is the default landing
    for the participants listing page.
    It will list all of the participants
    in the current term for HFOSS
    """
    return participants_year_term(currentYear, currentTerm)


@participants_bp.route('/<year>')
def participants_year(year):
    """
    This will get all the participants
    within a given year
    """
    return participants(year + '/')


@participants_bp.route('/<year>/<term>')
def participants_year_term(year, term):
    """
    This will get all the participants
    within a given year and term
    """
    return participants(year + '/' + term + '/')


@participants_bp.route('/all')
def participants_all():
    return participants('')
"""
This will get all the participants
who have taken HFOSS
"""


def participants(root_dir):
    """
    Render the participants page,
    which shows a directory of all
    the students with their forge
    links, blog posts, assignment
    links, and etc.

    """

    yaml_dir = 'scripts/people/' + root_dir

    student_data = []
    for dirpath, dirnames, files in os.walk(yaml_dir):
        for fname in files:
            if fname.endswith('.yaml'):
                year_term_data = dirpath.split('/')
                # Skip YAML files not at the expected depth
                # (scripts/people/<year>/<term>/<name>.yaml)
                if len(year_term_data) < 4:
                    continue
                with open(dirpath + '/' + fname) as students:
                    contents = yaml.safe_load(students)
                    contents['yaml'] = dirpath + '/' + fname
                    contents['participant_page'] = "{y}/{t}/{u}".format(
                        y=year_term_data[2],
                        t=year_term_data[3],
                        u=os.path.splitext(fname)[0]
                    )
                    contents['isActive'] = (currentYear in year_term_data
                                            and currentTerm in year_term_data)
                    # Ensure hw dict exists for template iteration
                    if 'hw' not in contents:
                        contents['hw'] = {}

                    student_data.append(contents)

    assignments = ['quiz1', 'litreview1', 'bugfix', 'teamprop1', 'meetup1',
                   'commarchreport', 'commarchpreso', 'meetup2', 'curriculum',
                   'smoketest', 'vidreview1', 'vidreview2', 'teamprop2',
                   'litreview2', 'meetup3', 'quiz2', 'finalpreso']
    elapsed = (datetime.today() - hflossk.site.COURSE_START).total_seconds()
    target_number = int(elapsed / timedelta(weeks=1).total_seconds() + 1 +
                        len(assignments))

    return render_template(
        'blogs.html',
        student_data=student_data,
        gravatar=hflossk.site.gravatar,
        target_number=target_number
    )
