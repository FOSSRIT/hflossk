"""
Generate a static site from the Flask app using Frozen-Flask.

This freezes all discoverable routes into static HTML files
suitable for hosting on GitHub Pages. Dynamic routes like
/blog/<username> (which parse live RSS feeds) are excluded.
"""

import os

from flask_frozen import Freezer

from hflossk.site import app

freezer = Freezer(app)
base_dir = os.path.join(os.path.dirname(__file__), 'hflossk')


@freezer.register_generator
def simple_page():
    """Generate URLs for all top-level .mak templates."""
    templates_dir = os.path.join(base_dir, 'templates')
    for fname in os.listdir(templates_dir):
        if fname.endswith('.mak') and fname not in ('master.mak', 'ohno.mak',
                                                     'participant.mak',
                                                     'blogs.mak'):
            yield {'page': fname.replace('.mak', '')}


def _hw_pages():
    """Generate page values for homework templates."""
    hw_dir = os.path.join(base_dir, 'templates', 'hw')
    if os.path.isdir(hw_dir):
        yield {'page': 'index'}
        for fname in os.listdir(hw_dir):
            if fname.endswith('.mak') and fname != 'index.mak':
                yield {'page': fname.replace('.mak', '')}


def _lecture_pages():
    """Generate page values for lecture templates."""
    lectures_dir = os.path.join(base_dir, 'templates', 'lectures')
    if os.path.isdir(lectures_dir):
        yield {'page': 'index'}
        for fname in os.listdir(lectures_dir):
            if fname.endswith('.mak') and fname != 'index.mak':
                yield {'page': fname.replace('.mak', '')}


def _quiz_pages():
    """Generate quiz_num values for quiz templates."""
    quiz_dir = os.path.join(base_dir, 'templates', 'quiz')
    if os.path.isdir(quiz_dir):
        for fname in os.listdir(quiz_dir):
            if fname.endswith('.mak'):
                yield {'quiz_num': fname.replace('.mak', '')}


def _participant_pages():
    """Generate URLs for all participant profile pages."""
    people_dir = os.path.join('scripts', 'people')
    for dirpath, dirnames, files in os.walk(people_dir):
        for fname in files:
            if fname.endswith('.yaml'):
                parts = dirpath.split(os.sep)
                if len(parts) >= 4:
                    year = parts[-2]
                    term = parts[-1]
                    username = fname.replace('.yaml', '')
                    yield {'year': year, 'term': term, 'username': username}


# Register generators for each named blueprint registration.
# Flask 3.x requires unique names for duplicate blueprint registrations,
# so endpoints are namespaced as '<name>.<view_function>'.
freezer.register_generator(lambda: _hw_pages(), 'assignments.display_homework')
freezer.register_generator(lambda: _hw_pages(), 'hw.display_homework')
freezer.register_generator(lambda: _lecture_pages(), 'lectures.display_lecture')
freezer.register_generator(lambda: _quiz_pages(), 'quizzes.show_quiz')
freezer.register_generator(lambda: _quiz_pages(), 'quiz.show_quiz')
freezer.register_generator(lambda: _participant_pages(), 'participants.participant_page')
freezer.register_generator(lambda: _participant_pages(), 'blogs.participant_page')
freezer.register_generator(lambda: _participant_pages(), 'checkblogs.participant_page')


if __name__ == '__main__':
    app.config['FREEZER_DESTINATION'] = os.path.join(
        os.path.dirname(__file__), 'build')
    app.config['FREEZER_RELATIVE_URLS'] = True
    freezer.freeze()
