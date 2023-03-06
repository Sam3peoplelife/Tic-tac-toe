from flask import Flask, render_template, request
import random

app = Flask(__name__)

# The Tic-Tac-Toe board
board = ["", "", "", "", "", "", "", "", ""]

# The current player ("X" or "O")
current_player = "X"

# The winner of the game ("X", "O", or None)
winner = None

# True if the game has ended, False otherwise
game_over = False

def check_winner():
    global winner
    if (board[0] == board[1] == board[2] and board[0] != "") or \
        (board[3] == board[4] == board[5] and board[3] != "") or \
        (board[6] == board[7] == board[8] and board[6] != "") or \
        (board[0] == board[3] == board[6] and board[0] != "") or \
        (board[1] == board[4] == board[7] and board[1] != "") or \
        (board[2] == board[5] == board[8] and board[2] != "") or \
        (board[0] == board[4] == board[8] and board[0] != "") or \
        (board[2] == board[4] == board[6] and board[2] != ""):
        winner = current_player
        return True
    elif all(cell != "" for cell in board):
        return True
    else:
        return False

def switch_player():
    global current_player
    if not check_winner():
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"

def make_bot_move():
    global current_player
    empty_cells = [i for i in range(9) if board[i] == ""]
    if empty_cells:
        cell = random.choice(empty_cells)
        board[cell] = current_player
        switch_player()

@app.route("/")
def index():
    global board, current_player, winner, game_over
    board = ["", "", "", "", "", "", "", "", ""]
    current_player = "X"
    winner = None
    game_over = False
    return render_template("board.html", board=board, current_player=current_player, winner=winner, game_over=game_over)

@app.route("/move", methods=["POST"])
def move():
    global board, current_player, game_over, winner
    cell = int(request.form["cell"])
    if board[cell] == "":
        board[cell] = current_player
        if check_winner():
            game_over = True
            if winner:
                return render_template("board.html", board=board, current_player=current_player, winner=winner, game_over=game_over)
            else:
                winner = "Tie"
                return render_template("board.html", board=board, current_player=current_player, winner=winner, game_over=game_over)
        else:
            switch_player()
            if current_player == "O" and not game_over:
                make_bot_move()
            if check_winner():
                game_over = True
                if winner:
                    return render_template("board.html", board=board, current_player=current_player, winner=winner, game_over=game_over)
                else:
                    winner = "Tie"
                    return render_template("board.html", board=board, current_player=current_player, winner=winner, game_over=game_over)
            else:
                return render_template("board.html", board=board, current_player=current_player, winner=winner, game_over=game_over)


if __name__ == "__main__":
    app.run(debug=True)
