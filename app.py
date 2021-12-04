from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

responses = []


app = Flask(__name__)
app.config['SECRET_KEY'] = "my secert"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def starter_page():
    """shows the begin page."""

    return render_template("survey_start.html", survey=survey)


@app.route("/begin", methods=["POST"])
def starts_questions():
    """Clear the session of responses."""
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']  
    responses.append(choice)
    
    if (len(responses) == len(survey.questions)):
        
        return redirect("/done")

    else:
        return redirect(f"/questions/{len(responses)}")


@app.route("/questions/<int:qid>")
def show_question(qid):
    """shows correct question in order."""
   

    if (responses is None):
        return redirect("/")

    if (len(responses) == len(survey.questions)):
        return redirect("/done")

    if (len(responses) != qid):
        flash(f"Please do question in order.")
        return redirect(f"/questions/{len(responses)}")

    question = survey.questions[qid]
    return render_template(
        "question.html", question_num=qid, question=question)


@app.route("/done")
def fininsh_survey ():
    """Survey done page."""

    return render_template("done.html")