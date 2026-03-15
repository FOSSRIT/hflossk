# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

HFLOSSK is the Humanitarian Free/Open Source Software Course website for RIT, built with Flask and Jinja2 templates. It serves course materials (lectures, homework, quizzes) and tracks student participation via YAML files and RSS blog feeds. There is no database — all data is file-based.

## Commands

### Setup (Fedora Linux 43)
```bash
sudo dnf install python3 python3-pip git
git clone git@github.com:FOSSRIT/hflossk.git
cd hflossk
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Run locally
```bash
python app.py
# Serves at http://127.0.0.1:5000/ in debug mode
```

### Run tests
```bash
pip install -e ".[test]"
pytest                 # Run tests only
pytest --tb=short      # Shorter traceback output
ruff check .           # Lint only
```

### Run full test suite via tox
```bash
pip install tox
tox                    # Tests (py314) + lint
tox -e lint            # Lint only
tox -e cover           # Tests with coverage
```

### Freeze static site
```bash
python freeze.py
# Generates static HTML in build/
```

## Architecture

### Entry Point
`app.py` imports the Flask app from `hflossk/site.py` and runs the Flask dev server in debug mode. For production, use `gunicorn hflossk.site:app`.

### Template Engine: Jinja2 (Flask native)
Templates use `.html` extension and Jinja2 syntax (`{{ variable }}`, `{% extends %}`, `{% block %}`, `{% for %}`). All templates live in `hflossk/templates/` and inherit from `master.html`.

### Core Modules
- **`hflossk/site.py`** — Flask app creation, route definitions, context processor that injects `site.yaml` config into all templates. Gravatar/Libravatar helper. Routes for pages, syllabus, blog JSON endpoint, participant profiles, resources.
- **`hflossk/blueprints.py`** — Blueprints for `/assignments/` (homework), `/lectures/`, `/quizzes/`. Each dynamically discovers and serves templates from its subdirectory.
- **`hflossk/participants.py`** — Blueprint for `/participants/`, `/blogs/`, `/checkblogs/`. Walks `scripts/people/<year>/<term>/*.yaml` to build student roster. Calculates expected blog post counts based on elapsed course weeks.
- **`hflossk/util.py`** — RSS feed parsing via feedparser. Counts blog posts since course start date.

### Data Flow
1. **Course config**: `hflossk/site.yaml` (instructor, dates, location) and `hflossk/schedule.yaml` (weekly topics, assignments, due dates) are loaded at request time and injected into templates.
2. **Student data**: `scripts/people/<year>/<term>/<username>.yaml` — each file has required keys (`blog`, `feed`, `forges`, `irc`, `name`, `rit_dce`) and optional `hw` dict mapping assignment names to blog post URLs.
3. **Blog tracking**: `/blog/<username>` endpoint parses student RSS feeds and returns JSON post count. Used via AJAX in the participants page.

### Content as Templates
Course content (lectures, homework, quizzes) are Jinja2 template files in `hflossk/templates/hw/`, `hflossk/templates/lectures/`, `hflossk/templates/quiz/`. They inherit from `master.html`.

### Static Assets
`hflossk/static/` contains Bootstrap CSS/JS, course PDFs (`books/`), slide decks (`decks/`), and challenge descriptions (`challenges/`).

### YAML Validation Tests
`hflossk/tests/test_yaml.py` validates that all student YAML files contain required fields and conform to expected schema. This is the primary test coverage.

## CI/CD

- **CI** (`.github/workflows/ci.yml`): Runs on all branches/PRs in a Fedora 43 minimal container. Installs deps, lints with ruff, runs pytest.
- **Preview** (part of CI): For non-main branches, freezes the site and uploads a downloadable artifact (retained 7 days).
- **Deploy** (`.github/workflows/deploy.yml`): On push to `main`, freezes the site via `freeze.py` and deploys to GitHub Pages.
- **Static site generation**: `freeze.py` uses Frozen-Flask to crawl the app and generate static HTML. Dynamic routes like `/blog/<username>` (live RSS parsing) are excluded.

## Key Constraints
- No database or ORM — all persistence is YAML files in the repo
- Python 3.14 on Fedora 43 is the target runtime

## Git Commit Conventions
- Subject line: emoji prefix + component prefix (e.g., `🔧 App:`, `📝 Docs:`, `🚀 CI:`, `🐛 Fix:`)
- Trailer: `Assisted-by: Claude Opus 4.6 (1M context)` for AI-assisted commits
- Trailer: `Signed-off-by:` (always last, via `--signoff`)
- GPG signed (via `-S`)
