from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

boggle_game = Boggle()

@app.route('/')
def show_start():
    """Clear the session board state, generate a new board state, and render the html"""
    session['board_state'] = []
    session['board_state'] = boggle_game.make_board()
    return render_template("index.html")

@app.route('/game')
def show_game():
    """Render the html for the game board, player HUD, and player interface"""
    return render_template("game.html")

@app.route('/validate-word')
def validate_word():
    """Retrieve player input and check if it is valid"""
    word = request.args['word']
    board = session['board_state']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})

@app.route('/track-stats', methods=["POST"])
def track_stats():
    """Record player high score and number of games played for this session"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    num_plays = session.get("num_plays", 0)

    session['num_plays'] = num_plays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(newHighScore=score > highscore)