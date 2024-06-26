from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "oh-so-secret"
		
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

survey = satisfaction_survey

@app.route('/')
def show_survey():
    """Shows survey to start"""

    title = survey.title
    instructions = survey.instructions
    
    return render_template('home.html', 
    title = title, 
    instructions = instructions)

@app.route('/start', methods=["POST"])
def handle_start():
    """Post request that clears session data to change state"""

    session['responses'] = []
    return redirect('questions/0')


@app.route('/questions/<int:question_num>')
def show_question(question_num):
    """Shows question form based on how far the user has answered"""

    responses = session['responses']
    #prevents user from going back to questions when all have been answered
    if len(responses) == len(survey.questions):
        return redirect('/completed')  

    #prevents user from accessing other questions when they haven't answered
    if question_num != len(responses):
        flash(f"Invalid question number: {question_num}! Redirected.")
        return redirect(f'/questions/{len(responses)}')

    title = survey.title
    question = survey.questions[question_num].question
    choices = survey.questions[question_num].choices
    
    return render_template('questions.html',
    title = title,
    question = question, 
    choices = choices)


@app.route('/answer', methods=["POST"])
def handle_answer():
    """Adds answer to responses list and redirects users to the next correct page"""

    #answer is added to session data
    answer = request.form.get('answer')
    responses = session['responses']
    responses.append(answer)
    #set session to the updated list of answers
    session['responses'] = responses

    #if all questions have been answered redirect to completion confirmation page
    if len(responses) == len(survey.questions):
        return redirect('/completed')     
    return redirect(f'/questions/{len(responses)}')


@app.route('/completed')
def show_completion():
    """Shows completion confirmation page"""

    return render_template('done.html')