from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# Empty list to be populated with users responses to the survey
responses = [None for question in survey.questions]

@app.route('/')
def show_survey_start():
    '''Renders the homepage'''
    title = survey.title
    instructions = survey.instructions
    return render_template('survey_start.html', title=title, instructions=instructions)

@app.route('/questions/<int:index>')
def show_question(index):
    '''Renders the questions page for given index. User is prompted submit response.'''
    question = survey.questions[index].question
    choices = survey.questions[index].choices
    return render_template('questions.html', index=index, question=question, choices=choices)

@app.route('/answer/<int:index>', methods=["POST"])
def handle_answer(index):
    '''Stores the user's answer and redirects them to the next question.'''
    choice = request.form['choice']
    responses[index] = choice
    if None in responses:
        next_index = responses.index(None)
        return redirect(f'/questions/{next_index}')
