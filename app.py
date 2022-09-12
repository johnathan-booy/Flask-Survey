from flask import Flask, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# Empty list to be populated with users responses to the survey
responses = []

@app.route('/')
def home_page():
    '''Renders the homepage'''
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('home.html', title=title, instructions=instructions)

@app.route('/questions/<index>')
def questions(index):
    '''Renders the questions page for given index. User is prompted submit response.'''
    index = int(index)
    question = satisfaction_survey.questions[index].question
    choices = satisfaction_survey.questions[index].choices
    return render_template('questions.html', index=index, question=question, choices=choices)