from logging import debug
from flask import Flask, request, render_template, redirect, flash
from flask import session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-noo-Toby"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

responses = []

@app.route('/')
def start_survey():
    """Renders a page with title of the survey, instructions, and a button to start"""
    return render_template("start.html")

@app.route('/start', methods=['POST'])
def clear_responses():
    """Clear sessions"""

    session['responses'] = []

    return redirect('questions/0')

@app.route('/questions/<int:qid>')
def handle_question(qid):
    """Shows form with current questions, and fires POST request to /answer with user's answer"""
    
    #Need to reset responses variable by pulling from session
    responses = session.get('responses')

    if qid == len(responses):
        #If the question id matches the length of responses, proceed normally
        question_num = qid + 1
        question = survey.questions[qid].question
        choices = survey.questions[qid].choices
        return render_template("question.html", question=question, num=question_num, choices=choices)
    else: 
        #If not, redirect to the correct question and send a flash message
        flash("Trying to access an invalid question", 'error')
        return redirect(f"/questions/{len(responses)}")
    

@app.route('/answer', methods=['POST'])
def handle_answer():
    """Appends answer to responses list and then redirects to next question"""
    
    #Gets response
    answer = request.form["answer"]
    
    #Adds response to session
    responses = session['responses']
    responses.append(answer)
    session['responses'] = responses

    #Checks responses list to ensure that the question number is correct
    if len(responses) < 4:
        return redirect(f"/questions/{len(responses)}")
    elif len(responses) == len(survey.questions):
        return redirect("/complete")
    elif len(responses) == 0:
        return redirect("/")

@app.route("/complete")
def finish_survey():
    """Directs user to ending page"""

    return render_template("complete.html")