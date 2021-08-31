from flask import Flask, request, render_template, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle
from functions import make_board

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool123456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route('/')
def home_page():
    """Displays button used to start game"""

    return render_template('start.html')


@app.route('/boggle')
def boggle():
    """Displays boggle board and guess form"""

    board = make_board()
    session['board'] = board



    return render_template('boggle.html', board=board)

@app.route('/check-guess')
def check_guess():
    """
    Receives guess from submitGuess function
    Uses check_valid_word method to check validity of guess
    Sends data back to submitGuess function    
    """

    guess = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, guess)

    return jsonify({'result': response})

@app.route('/check-score', methods=['POST'])
def check_score():
    """
    Receives score from gameEnd function
    Updates highscore if needed, tells front-end if there is new highscore
    Updates times_played 
    """
    # import pdb
    # pdb.set_trace()

    score = request.json['score']

    session['times_played'] = session.get('times_played', 0) + 1

    if score > session.get('highscore', 0):
        session['highscore'] = score
        # return jsonify('highscore')
        return jsonify({'result': 'highscore'})

    # return jsonify('not-highscore')
    return jsonify({'result': 'not-highscore'}) 

        