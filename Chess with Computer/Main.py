import pygame as p
import ChessEngine
import ComputerEngine

width = height = 512
dimension = 8
SQ_size = height // dimension
fps = 15
Images = {}
white = (255, 255, 255)
green = (0, 255, 0)
orange = (255, 69, 0)
p.display.set_caption('A bit Racey')

def text_objects(text, font):
    textSurface = font.render(text, True, orange)
    return textSurface, textSurface.get_rect()


def winner(screen, win):
    largeText = p.font.Font('freesansbold.ttf', 50)
    TextSurf, TextRect = text_objects(win, largeText)
    TextRect.center = ((width / 2), (height / 2))
    screen.blit(TextSurf, TextRect)
    p.display.flip()


def opositeColor(gs, pos):
    if gs.board[pos[0]][pos[1]][1] == "w":
        return "w"
    return "b"

def LoadImage():
    pieces = ["bR", "bB", "bN", "bK", "bQ", "wR", "wB", "wN", "wK", "wQ", "bp", "wp"]
    for piece in pieces:
        Images[piece] = p.transform.scale(p.image.load("pieces/" + piece + ".png"), (SQ_size, SQ_size))


def main():
    p.init()
    surface = p.display.set_mode((width, height))
    clock = p.time.Clock()
    LoadImage()
    running = True
    gs = ChessEngine.GameState()
    sqSelected = ()
    playerclicks = []
    win = None
    print(gs.board)
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                l = location[0] // SQ_size
                c = location[1] // SQ_size
                if sqSelected == (l, c):
                    sqSelected = ()
                    playerclicks = []
                elif not (gs.board[c][l] == "--" and len(playerclicks) == 0):
                    sqSelected = (l, c)
                    playerclicks.append(sqSelected)
            elif len(playerclicks) == 2 or gs.WhiteToMove == False:
                    move = None
                    if gs.WhiteToMove:
                        move = ChessEngine.Move(playerclicks[0], playerclicks[1], gs.board)
                    else:
                        move = ComputerEngine.best_move(gs, 3)
                    gs.makeMove(move, surface, Images)
                    print(move.pieceMoved)

                    if ChessEngine.chess_mate(gs, "b"):
                        win = "White has won"
                        running = False
                    if ChessEngine.chess_mate(gs, "w"):
                        win = "Black has won"
                        running = False
                    sqSelected = ()
                    playerclicks = []
        drawgamestate(surface, gs.board, running, win)
        clock.tick(fps)
        p.display.flip()
    while True:
        for e in p.event.get():
            if e.type == p.QUIT:
                return


def drawgamestate(surface, board, running, win):
    drawboard(surface)
    drawpieces(surface, board)
    if running == False:
        winner(surface, win)

def drawboard(surface):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(dimension):
        for c in range(dimension):
            color = colors[((r + c) % 2)]
            p.draw.rect(surface, color, p.Rect(c * SQ_size, r * SQ_size, SQ_size, SQ_size))



def drawpieces(surface, board):
    for r in range(dimension):
        for c in range(dimension):
            piece = board[r][c]
            if piece != "--":
                surface.blit(Images[piece], p.Rect(c * SQ_size, r * SQ_size, SQ_size, SQ_size))



if __name__ == "__main__":
    main()
