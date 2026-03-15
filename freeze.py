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
    """Generate URLs for all top-level .html templates."""
    templates_dir = os.path.join(base_dir, 'templates')
    for fname in os.listdir(templates_dir):
        if fname.endswith('.html') and fname not in ('master.html', 'ohno.html',
                                                      'participant.html',
                                                      'blogs.html'):
            yield {'page': fname.replace('.html', '')}


@freezer.register_generator
def blueprint_pages():
    """Generate URLs for all blueprint-served pages.

    Yields (endpoint, values) tuples for namespaced blueprint endpoints.
    Flask 3.x requires unique names for duplicate blueprint registrations,
    so endpoints are namespaced as '<name>.<view_function>'.
    """
    hw_dir = os.path.join(base_dir, 'templates', 'hw')
    if os.path.isdir(hw_dir):
        pages = ['index']
        pages.extend(f.replace('.html', '') for f in os.listdir(hw_dir)
                     if f.endswith('.html') and f != 'index.html')
        for page in pages:
            yield 'hw.display_homework', {'page': page}
            yield 'assignments.display_homework', {'page': page}

    lectures_dir = os.path.join(base_dir, 'templates', 'lectures')
    if os.path.isdir(lectures_dir):
        pages = ['index']
        pages.extend(f.replace('.html', '') for f in os.listdir(lectures_dir)
                     if f.endswith('.html') and f != 'index.html')
        for page in pages:
            yield 'lectures.display_lecture', {'page': page}

    quiz_dir = os.path.join(base_dir, 'templates', 'quiz')
    if os.path.isdir(quiz_dir):
        for fname in os.listdir(quiz_dir):
            if fname.endswith('.html'):
                quiz_num = fname.replace('.html', '')
                yield 'quizzes.show_quiz', {'quiz_num': quiz_num}
                yield 'quiz.show_quiz', {'quiz_num': quiz_num}

    people_dir = os.path.join('scripts', 'people')
    for dirpath, dirnames, files in os.walk(people_dir):
        for fname in files:
            if fname.endswith('.yaml'):
                parts = dirpath.split(os.sep)
                if len(parts) >= 4:
                    values = {
                        'year': parts[-2],
                        'term': parts[-1],
                        'username': fname.replace('.yaml', ''),
                    }
                    yield 'participant_page', values


if __name__ == '__main__':
    app.config['FREEZER_DESTINATION'] = os.path.join(
        os.path.dirname(__file__), 'build')
    app.config['FREEZER_RELATIVE_URLS'] = True
    freezer.freeze()
