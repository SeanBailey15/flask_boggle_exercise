from boggle import Boggle
from flask import Flask, request, render_template, session, jsonify
# from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']
# app.config['TESTING'] = True

boggle_game = Boggle()

@app.route('/')
def show_start():
    session['board_state'] = []
    session['board_state'] = boggle_game.make_board()
    return render_template("start.html")

@app.route('/game')
def show_game():
    
    return render_template("game.html")

@app.route('/validate-word')
def validate_word():
    word = request.args['word']
    board = session['board_state']
    response = boggle_game.check_valid_word(board, word)

    return jsonify({'result': response})