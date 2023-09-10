from flask import Flask, request, render_template, jsonify, session
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "fdfgkjtjkkg45yfdb"
# app.config["SECRET_KEY"] = "*atvsuu@4%!.9jjqwntp"

boggle_game = Boggle()


@app.route("/")
def homepage():
    # display & generate board
    board = boggle_game.make_board()
    # assign session to board
    session["board"] = board
    # obtain highest score in session 
    high_score = session.get("high_score", 0)
    # obtain number of plays in session
    numplays = session.get("numplays", 0)

    # return board
    return render_template("index.html",
                           board=board,
                           high_score=high_score,
                           numplays=numplays)

@app.route("/check-word")
def check_word():
    # is word in the dictionary?
    word = request.args["word"]
    # board in session
    board = session["board"]
    # obtain response
    response = boggle_game.check_valid_word(board, word)
    return jsonify({ "result": "response" })


@app.route("/post-score", methods=["POST"])
def post_score():
    # receive score, update numplays, update highest score 

    # obtain score via request.json
    score = request.json["score"]
    # highest score
    high_score = session.get("high_score", 0)
    # number of plays
    numplays = session.get("numplays", 0)
    # introduce numplays & high_score to session
    session["numplays"] = numplays + 1
    session["high_score"] = max(score, high_score)
    # return json object
    return jsonify(brokeRecord = score > high_score)

