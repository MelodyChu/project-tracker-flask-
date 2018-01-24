"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)


@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')


    first, last, github = hackbright.get_student_by_github(github)

    student_tuple = hackbright.get_grades_by_github(github)
    # [(u'Markov', 10), (u'Blockly', 2)] --> output
    print "{acct} is the GitHub account for {first} {last}".format(
        acct=github, first=first, last=last, student_tuple=student_tuple)

    return render_template("student_info.html", first=first, last=last, github=github, student_tuple=student_tuple)

@app.route("/student-search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/add_student")
def add_student_form():
    """Shows student add form."""

    return render_template("new_student_form.html")

@app.route("/add_student", methods=['POST'])
def student_add():
    """Processing of the form"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')

    hackbright.make_new_student(first_name, last_name, github)

    return render_template("success.html", first_name=first_name, last_name=last_name, github=github)
    # #flash('Success!')
    # return redirect('/student?github=' + github)
 
@app.route('/project')
def list_project_info():
    """Listing title, description, max grade of a project"""

    title = request.args.get('project')

    project_description = hackbright.get_project_by_title(title)

    project_info = hackbright.get_student_name_grade()

    project_by_title = []

    for info in project_info:
        if info[3] == title:
            project_by_title.append(info)

    return render_template("projects.html", title=title, project_description=project_description, project_info=project_info, project_by_title=project_by_title)

# project_info = [(u'Jane', u'Hacker', u'jhacks', u'Blockly', 2), (u'Jane', u'Hacker', u'jhacks', u'Markov', 10), (u'Sarah', u'Developer', u'sdevelops', u'Markov', 50), (u'Sarah', u'Developer', u'sdevelops', u'Blockly', 100)]





if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

   


# def get_grades_by_title(title):
#     """Get a list of all student grades for a project by its title"""

#     QUERY = """
#         SELECT student_github, grade
#         FROM Grades
#         WHERE project_title = :title
#         """

#     db_cursor = db.session.execute(QUERY, {'title': title})

#     rows = db_cursor.fetchall()

#     for row in rows:
#         print "Student {acct} received grade of {grade} for {title}".format(
#             acct=row[0], grade=row[1], title=title)

#     return rows
