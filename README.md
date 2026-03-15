# HFLOSSK

![GitHub Actions CI status](https://github.com/FOSSRIT/hflossk/actions/workflows/ci.yml/badge.svg)

## What is this?

This repository uses Flask, Mako, and Bootstrap to make a website for the Humanitarian Free/Open Source Software Course at RIT.
The content shown here is a compilation of course materials from several different professors, who ran the course multiple semesters.
Those professors were as follows:

- D. Joe
- Dave Shein
- Justin Sherrill
- Ralph Bean
- Remy DeCausemaker
- Stephen Jacobs


## Setting up your development environment

### Fedora Linux 43

Install Python and create a virtual environment:

```bash
sudo dnf install python3 python3-pip git
```

Clone the repository and set up the project:

```bash
git clone git@github.com:FOSSRIT/hflossk.git
cd hflossk
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Running locally

With your virtual environment activated:

```bash
python app.py
```

Open [127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser.
The server runs in debug mode and will reload when you change files.

### Running the tests

Install the test dependencies and run with `pytest`:

```bash
pip install -e ".[test]"
pytest
```

Or use `tox` to run the full test suite and linter:

```bash
pip install tox
tox
```

Tests check validity of all YAML files and validate the keys in student YAML files.
The linter (`ruff`) checks code style.


## Building a static site

The site can be frozen into static HTML using Frozen-Flask:

```bash
python freeze.py
```

This generates the site in the `build/` directory.
This is what gets deployed to GitHub Pages on pushes to `main`.


## Course content

The course materials (syllabus, homework assignments, lecture notes) are kept in this repository.

Templates use [Jinja2](https://jinja.palletsprojects.com/), Flask's built-in template engine.
They can contain plain HTML mixed with Jinja2 expressions and control structures.

You should run the server locally to check that your modifications render the way you want before pushing.


## License

© 2013 Remy DeCausemaker

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
You may obtain a copy of the License at

> [www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)
>
> Unless required by applicable law or agreed to in writing, software distributed
> under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
> CONDITIONS OF ANY KIND, either express or implied. See the License for the
> specific language governing permissions and limitations under the License.
