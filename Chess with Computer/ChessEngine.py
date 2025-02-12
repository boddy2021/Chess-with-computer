import pygame as py

width = height = 512
dimension = 8
SQ_size = height // dimension
fps = 15

class GameState():
    def __init__(self):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]
        self.WhiteToMove = True

    def makeMove(self, move, screen = None, Images = None):
        if screen == None or not specialMoves(move, self, screen, Images):
            if validMove(move, self, 0):
                sboard = GameState()
                sboard.copy(self)
                sboard.copy_piece(move)
                if not chess(sboard, move.pieceMoved[0]):
                    self.copy_piece(move)
                    self.WhiteToMove = not self.WhiteToMove

    def copy(self, gs):
        for l in range(dimension):
            for c in range(dimension):
                self.board[l][c] = gs.board[l][c]
        self.WhiteToMove = gs.WhiteToMove

    def copy_piece(self, move):
        self.board[move.startl][move.startc] = "--"
        self.board[move.endl][move.endc] = move.pieceMoved

class Move():
    def __init__(self, startsq, endsq, board):
        self.startl = startsq[1]
        self.startc = startsq[0]
        self.endl = endsq[1]
        self.endc = endsq[0]
        self.pieceMoved = board[self.startl][self.startc]
        self.pieceCaptured = board[self.endl][self.endc]

def validMove(move, board, c = False):
    if (move.pieceMoved[0] == "b" and board.WhiteToMove and not c) or (not c and move.pieceMoved[0] == "w" and not board.WhiteToMove):
        return False
    if move.pieceMoved == 'bR' or move.pieceMoved == "wR":
        return rookMove(move) and  not piecesinfront(move,board.board)
    if move.pieceMoved == 'bB' or move.pieceMoved == "wB":
        return bishopMove(move) and not piecesinfront(move, board.board)
    if move.pieceMoved == 'bQ' or move.pieceMoved == "wQ":
        return quinMove(move) and not piecesinfront(move, board.board)
    if move.pieceMoved == 'bN' or move.pieceMoved == "wN":
        return knightMove(move) and takepiece(move)
    if move.pieceMoved == 'bK' or move.pieceMoved == "wK":
        return kingMove(move) and not piecesinfront(move, board.board)
    if move.pieceMoved == 'bp' or move.pieceMoved == "wp":
        return pawnMove(move) and not piecesinfront(move, board.board)


def rookMove(move):
    return move.startl == move.endl or move.startc == move.endc

def bishopMove(move):
    return abs(move.startl - move.endl) == abs(move.startc - move.endc)

def quinMove(move):
    return rookMove(move) or bishopMove(move)

def knightMove(move):
    return (abs(move.startc - move.endc) == 1 and abs(move.startl - move.endl) == 2) or (abs(move.startc - move.endc) == 2 and abs(move.startl - move.endl) == 1)

def kingMove(move):
    if abs(move.startl - move.endl) != 1 and abs(move.startl - move.endl) != 0:
        return False
    if abs(move.startc - move.endc) != 1 and abs(move.startc - move.endc) != 0:
        return False
    return True

def pawnMove(move):
    if abs(move.startc - move.endc) <= 1\
             and ((move.startl - move.endl == 1 and move.pieceMoved == "wp")  or (move.startl - move.endl == -1 and move.pieceMoved == "bp")):
        return True
    if move.startc - move.endc == 0 and abs(move.startl - move.endl) == 2 \
             and ((move.pieceMoved == "bp" and move.startl == 1) or (move.pieceMoved == "wp" and move.startl == 6)):
        return True
    return False

def chess_mate(board, color):
    for l in range(dimension):
        for c in range(dimension):
            if board.board[l][c][0] == color:
                for l1 in range(dimension):
                    for c1 in range(dimension):
                        tboard = GameState()
                        tboard.copy(board)
                        move = Move((c, l), (c1, l1), board.board)
                        tboard.makeMove(move)
                        if not chess(tboard, color):
                            return False
    return True


def chess(board, color):
    pos = get_king_pos(board)
    for l in range(dimension):
        for c in range(dimension):
            if board.board[l][c] != "--" and board.board[l][c][0] != color:
                move = Move((c, l), pos, board.board)
                if validMove(move, board, True):
                    return True
    return False

def get_king_pos(board):
    s = "b"
    if board.WhiteToMove:
        s = "w"
    for l in range(dimension):
        for c in range(dimension):
            if board.board[l][c][1] == "K" and board.board[l][c][0] == s:
                return c, l

def piecesinfront(move, board):
    x = max(abs(move.startc - move.endc), abs(move.startl - move.endl)) - 1
    col = np(move.startc, move.endc)
    row = np(move.startl, move.endl)
    sq = (move.startl, move.startc)
    for i in range(x):
        sq = (sq[0] - row, sq[1] - col)
        if(board[sq[0]][sq[1]] != "--"):
            return True
    return not takepiece(move)

def takepiece(move):
    if move.pieceMoved[0] == move.pieceCaptured[0]:
        return False
    if move.pieceMoved[1] == "p":
        if move.startc == move.endc and move.pieceCaptured != "--":
            return False
        elif move.startc != move.endc and move.pieceCaptured == "--":
            return False
    return True

def specialMoves(move, board, screen, Images):
    if move.pieceMoved[1] == "p" and (move.endl == 0 or move.endl == 7) and validMove(move, board):
        return promotion(move, board, screen, Images)
    if move.pieceMoved[1] == "K" and abs(move.startc - move.endc) == 2:
        return castle(move, board)
    return False


def smCondtions(move, board):
    if move.pieceMoved[1] == "K" and abs(move.startc - move.endc) == 2:
        color = move.pieceMoved[0]
        if move.endc == 2:
            y = 1
            x = 4
        else:
            y = 5
            x = 7
        for i in range(y, x):
            if board.board[move.startl][i] != "--":
                return False
            board.board[move.startl][i] = move.pieceMoved
            board.board[move.startl][move.startc] = "--"
            x = chess(board, color)
            board.board[move.startl][i] = "--"
            board.board[move.startl][move.startc] = move.pieceMoved
            if x:
                return False
        return True
    if move.pieceMoved[1] == "p" and (move.endl == 0 or move.endl == 7):
        return True
    return False


def promotion(move, board, screen, Images):
    pieces = ["R", "B", "N", "Q"]
    drawP(move, screen, Images)
    pos = waitClick()
    board.board[move.startl][move.startc] = "--"
    board.board[move.endl][move.endc] = move.pieceMoved[0] + pieces[pos[0] // SQ_size // 2]
    board.WhiteToMove = not board.WhiteToMove
    return True


def drawP(move, screen, Images):
    py.draw.rect(screen, py.Color("white"), py.Rect(0, SQ_size * 3, width, 100))
    pieces = ["R", "B", "N", "Q"]
    a = 0
    for piece in pieces:
        a += 1.45
        screen.blit(Images[move.pieceMoved[0] + piece], py.Rect(a * SQ_size, SQ_size * 3.3, SQ_size, SQ_size))
    py.display.flip()


def castle(move, board):
    color = move.pieceMoved[0]
    if move.endc == 2:
        y = 1
        x = 4
    else:
        y = 5
        x = 7
    for i in range(y, x):
        if board.board[move.startl][i] != "--":
            return False
        board.board[move.startl][i] = move.pieceMoved
        board.board[move.startl][move.startc] = "--"
        x = chess(board, color)
        board.board[move.startl][i] = "--"
        board.board[move.startl][move.startc] = move.pieceMoved
        if x:
            return False
    if move.endc == 1:
        board.board[move.startl][2] = board.board[move.startl][4]
        board.board[move.startl][3] = board.board[move.startl][0]
        board.board[move.startl][0] = "--"
        board.board[move.startl][1] = "--"
    else:
        board.board[move.startl][6] = board.board[move.startl][4]
        board.board[move.startl][5] = board.board[move.startl][7]
        board.board[move.startl][7] = "--"
        board.board[move.startl][4] = "--"
    board.WhiteToMove = not board.WhiteToMove
    return True


def np(a, b):
    if a - b > 0:
        return 1
    elif a - b == 0:
        return 0
    return -1

def waitClick():
    while True:
        for e in py.event.get():
            if e.type == py.MOUSEBUTTONDOWN:
                return py.mouse.get_pos()