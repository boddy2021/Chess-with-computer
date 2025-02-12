import ChessEngine as ce
import math, random
import PieceValues as pv

width = height = 512
dimension = 8
SQ_size = height // dimension
fps = 15
ab = []
m = 0

def best_move(state, depth):
    return minimax(state, depth)


def actions(board, color):
    v = []
    for l in range(dimension):
        for c in range(dimension):
            if(board.board[l][c][0] == color):
                for l1 in range(dimension):
                    for c1 in range(dimension):
                        sboard = ce.GameState()
                        sboard.copy(board)
                        move = ce.Move((c, l), (c1, l1), sboard.board)
                        if ce.validMove(move, sboard):
                            v.append(move)
    return v

def points(move):
    pc = move.pieceCaptured[1]
    pm = move.pieceMoved[1]
    color = move.pieceMoved[0]
    l = move.endl
    c = move.endc
    l1 = move.startl
    c1 = move.startc
    p = 0
    if pc == "p":
        p = 100
    elif pc == "B":
        p = 300
    elif pc == "N":
        p = 300
    elif pc == "R":
        p = 500
    elif pc == "Q":
        p = 900
    elif pc == "K":
        p = 9000
    if pm == "p":
            if color == "w":
                return p + pv.pawnEvalWhite[l][c]- pv.pawnEvalWhite[l1][c1]
            else:
                return p + pv.pawnEvalBlack[l][c] - pv.pawnEvalBlack[l1][c1]
    if pm == "N":
            return p + pv.knightEval[l][c] - pv.knightEval[l1][c1]
    if pm == "B":
            if color == "w":
                return p + pv.bishopEvalWhite[l][c] - pv.bishopEvalWhite[l1][c1]
            else:
                return p + pv.bishopEvalBlack[l][c] - pv.bishopEvalBlack[l1][c1]
    if pm == "R":
            if color == "w":
                return p + pv.rookEvalWhite[l][c] - pv.rookEvalWhite[l1][c1]
            else:
                return p + pv.rookEvalBlack[l][c] - pv.rookEvalBlack[l1][c1]
    if pm == "K":
            if color == "w":
                return p + pv.kingEvalWhite[l][c] - pv.kingEvalWhite[l1][c1]
            else:
                return p + pv.kingEvalBlack[l][c] - pv.kingEvalBlack[l1][c1]
    if pm == "Q":
            return p + pv.queenEval[l][c] - pv.queenEval[l1][c1]
    return p

def max_value(board, depth, inc):
    global ab
    global m
    m += 1
    if depth == inc:
        return 0
    v = math.inf
    for action in actions(board, "w"):
        v = min(v, (min_value(result(board, action), depth, inc + 1) - points(action)))
        if v < ab[inc - 1]:
            return ab[inc - 1]
        ab[inc] = v
    return v

def min_value(board, depth, inc):
    global ab
    global m
    m += 1
    if depth == inc:
        return 0
    v = -math.inf
    for action in actions(board, "b"):
        v = max(v, (max_value(result(board, action), depth, inc + 1) + points(action)))
        if v > ab[inc - 1]:
            return ab[inc - 1]
        ab[inc] = v
    return v


def minimax(board, depth):
    global ab
    global m
    m += 1
    p = -math.inf
    move = None
    initab(depth)
    for action in actions(board, "b"):
        q = max_value(result(board, action), depth, 1) + points(action)
        initab(depth)
        sboard = ce.GameState()
        sboard.copy(board)
        sboard.copy_piece(action)
        if q > p:
            p = q
            move = action
        if p == q:
            r = random.randint(1, 10)
            if r == 1:
                move = action
    print(move.endl, move.endc)
    print(m)
    return move


def result(board, move):
    sboard = ce.GameState()
    sboard.copy(board)
    sboard.makeMove(move)
    return sboard


def initab(depth):
    global ab
    ab.clear()
    for i in range(depth + 1):
        if i % 2 == 0:
            ab.append(-math.inf)
        else:
            ab.append(math.inf)
