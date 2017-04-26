"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""
    return render_template('student_search.html')

@app.route("/student")
def get_student():
    """Show information about a student."""
    github = request.args.get('github')

    grades_list = hackbright.get_student_grades(github)
    # Checks if user entered 'user' is in DB
    if hackbright.get_student_by_github(github) == None:
        html = render_template('make_new.html', github=github)
    else:
        first_name, last_name, github = hackbright.get_student_by_github(github)
        html = render_template('student_info.html',
                           first_name=first_name,
                           last_name=last_name,
                           github=github, 
                           grades_list=grades_list)
    return html


@app.route("/student-add")
def get_student_info():
    """Show form for searching for a student."""
    github = request.args.get('github')
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    if github == None:
        github = ''
        
    return render_template('new_student.html', github=github)


@app.route("/student-added", methods=['POST'])
def student_add():
    """Add a student."""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    first_name, last_name, github = hackbright.make_new_student(first_name, last_name, github)

    return render_template('student_info.html', github=github, first_name=first_name, last_name=last_name)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)
