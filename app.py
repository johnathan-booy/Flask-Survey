from flask import Flask, render_template, request, redirect, flash
from flask import session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# Empty list to be populated with users responses to the survey
RESPONSE_KEY = 'responses'


@app.route('/')
def show_survey_start():
    '''Renders the homepage'''
    title = survey.title
    instructions = survey.instructions
    return render_template('survey_start.html', title=title, instructions=instructions)


@app.route('/begin')
def start_survey():
    '''Clear the responses'''
    session[RESPONSE_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:index>')
def show_question(index):
    '''Renders the questions page for given index. User is prompted submit response.'''
    if len(session[RESPONSE_KEY]) == len(survey.questions):
        flash("You've already completed this survey!")
        return redirect('/thanks')
    elif index >= len(survey.questions) or index > len(session[RESPONSE_KEY]):
        flash(index)
        flash(len(session[RESPONSE_KEY]))
        flash("Oops, let's finish this question first!")
        return redirect(f'/questions/{len(session[RESPONSE_KEY])}')
    else:
        question = survey.questions[index].question
        choices = survey.questions[index].choices
        return render_template('questions.html', index=index, question=question, choices=choices)


@app.route('/answer', methods=["POST"])
def handle_answer():
    '''Stores the user's answer and redirects them to the next question.'''

    choice = request.form['choice']
    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    if len(session[RESPONSE_KEY]) < len(survey.questions):
        return redirect(f'/questions/{len(session[RESPONSE_KEY])}')
    else:
        return redirect('/thanks')


@app.route('/thanks')
def show_thanks():
    results = zip(
        [question.question for question in survey.questions], session[RESPONSE_KEY])
    return render_template('thanks.html', results=results)
