import pygame, sys, copy
from enum import Enum
from pygame.locals import *
from ai_factory import AlgorithmFactory

setFunc = list(range(1))  # 定義演算法
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
SPACESIZE = 50
BOARDWIDTH = 8
BOARDHEIGHT = 8
ANIMATIONSPEED = 400
FPS = 10

XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * SPACESIZE)) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * SPACESIZE)) / 2)

WHITE_TILE = 'WHITE_TILE'
BLACK_TILE = 'BLACK_TILE'
EMPTY_SPACE = 'EMPTY_SPACE'
HINT_TILE = 'HINT_TILE'

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 155, 0)
BRIGHTBLUE = (0, 50, 255)
BROWN = (174, 94, 0)

BACKGROUNDCOLOR = BLACK
TEXTBGCOLOR1 = BRIGHTBLUE
TEXTBGCOLOR2 = GREEN
GRIDLINECOLOR = BLACK
TEXTCOLOR = WHITE
HINTCOLOR = BROWN


# 玩家
class Role(Enum):
    PLAYER_1 = 'player1'
    PLAYER_2 = 'player2'


# 模式
class Mode(Enum):
    FIRST = 'first'
    SECOND = 'second'
    AUTO = 'auto'


def main():
    global MAINCLOCK, DISPLAYSURF, FONT, BIGFONT, BGIMAGE

    pygame.init()
    MAINCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Reversi')
    FONT = pygame.font.Font('freesansbold.ttf', 16)
    BIGFONT = pygame.font.Font('freesansbold.ttf', 24)

    boardImage = pygame.image.load('./img/board.png')
    boardImage = pygame.transform.smoothscale(boardImage, (BOARDWIDTH * SPACESIZE, BOARDHEIGHT * SPACESIZE))
    boardImageRect = boardImage.get_rect()
    boardImageRect.topleft = (XMARGIN, YMARGIN)

    BGIMAGE = pygame.image.load('./img/background.png')
    BGIMAGE = pygame.transform.smoothscale(BGIMAGE, (WINDOWWIDTH, WINDOWHEIGHT))
    BGIMAGE.blit(boardImage, boardImageRect)

    while True:
        if runGame() is False:
            break


def runGame():
    mainBoard = getNewBoard()
    resetBoard(mainBoard)
    isAuto = False
    showHints = False

    sel = sideSelect()
    if sel == Mode.FIRST:
        turn = Role.PLAYER_1
        playerOneTile = BLACK_TILE
        playerTwoTile = WHITE_TILE
    elif sel == Mode.SECOND:
        turn = Role.PLAYER_2
        playerOneTile = WHITE_TILE
        playerTwoTile = BLACK_TILE
    elif sel == Mode.AUTO:
        turn = Role.PLAYER_1
        playerOneTile = BLACK_TILE
        playerTwoTile = WHITE_TILE
        isAuto = True

    drawBoard(mainBoard)

    newGameSurf = FONT.render('New Game', True, TEXTCOLOR, TEXTBGCOLOR2)
    newGameRect = newGameSurf.get_rect()
    newGameRect.topright = (WINDOWWIDTH - 8, 10)
    hintsSurf = FONT.render('Hints', True, TEXTCOLOR, TEXTBGCOLOR2)
    hintsRect = hintsSurf.get_rect()
    hintsRect.topright = (WINDOWWIDTH - 8, 40)

    currentXY = None
    while True:
        if turn == Role.PLAYER_1 and not isAuto:
            if len(getValidMoves(mainBoard, playerOneTile)) == 0:
                break
            movexy = None
            while movexy is None:
                if showHints:
                    boardToDraw = getBoardWithValidMoves(mainBoard, playerOneTile)
                else:
                    boardToDraw = mainBoard

                checkForQuit()
                for event in pygame.event.get():
                    if event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        if newGameRect.collidepoint((mousex, mousey)):
                            return True
                        elif hintsRect.collidepoint((mousex, mousey)):
                            showHints = not showHints

                        movexy = getSpaceClicked(mousex, mousey)
                        if movexy is None and not isValidMove(mainBoard, playerOneTile, movexy[0], movexy[1]):
                            movexy = None
                if movexy is not None:
                    currentXY = movexy

                drawBoard(boardToDraw, currentXY)
                drawInfo(boardToDraw, playerOneTile, playerTwoTile, turn)

                DISPLAYSURF.blit(newGameSurf, newGameRect)
                DISPLAYSURF.blit(hintsSurf, hintsRect)

                MAINCLOCK.tick(FPS)
                pygame.display.update()

            makeMove(mainBoard, playerOneTile, movexy[0], movexy[1], True)
            if len(getValidMoves(mainBoard, playerTwoTile)) != 0:
                turn = Role.PLAYER_2
        else:
            if turn == Role.PLAYER_1:
                turnOther = Role.PLAYER_2
                tile = playerOneTile
            else:
                turnOther = Role.PLAYER_1
                tile = playerTwoTile

            if len(getValidMoves(mainBoard, tile)) == 0:
                break

            drawBoard(mainBoard, currentXY)
            drawInfo(mainBoard, playerOneTile, playerTwoTile, turn)

            DISPLAYSURF.blit(newGameSurf, newGameRect)
            DISPLAYSURF.blit(hintsSurf, hintsRect)

            # pauseUntil = time.time() + random.randint(5, 15) * 0.1
            # while time.time() < pauseUntil:
            #     pygame.display.update()
            pygame.display.update()

            x, y = getComputerMove(mainBoard, tile)
            currentXY = (x, y)
            makeMove(mainBoard, tile, x, y, True)
            if len(getValidMoves(mainBoard, playerOneTile)) != 0:
                turn = turnOther

    drawBoard(mainBoard)
    scores = getScoreOfBoard(mainBoard)

    if scores[playerOneTile] > scores[playerTwoTile]:
        text = 'player1 beat the player2 by %s points.' % (scores[playerOneTile] - scores[playerTwoTile])
    elif scores[playerOneTile] < scores[playerTwoTile]:
        text = 'player2 beat the player1 by %s points.' % (scores[playerTwoTile] - scores[playerOneTile])
    else:
        text = 'The game was a tie!'

    textSurf = FONT.render(text, True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))
    DISPLAYSURF.blit(textSurf, textRect)

    text2Surf = BIGFONT.render('Play again?', True, TEXTCOLOR, TEXTBGCOLOR1)
    text2Rect = text2Surf.get_rect()
    text2Rect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 50)

    yesSurf = BIGFONT.render('Yes', True, TEXTCOLOR, TEXTBGCOLOR1)
    yesRect = yesSurf.get_rect()
    yesRect.center = (int(WINDOWWIDTH / 2) - 60, int(WINDOWHEIGHT / 2) + 90)

    noSurf = BIGFONT.render('No', True, TEXTCOLOR, TEXTBGCOLOR1)
    noRect = noSurf.get_rect()
    noRect.center = (int(WINDOWWIDTH / 2) + 60, int(WINDOWHEIGHT / 2) + 90)

    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if yesRect.collidepoint((mousex, mousey)):
                    return True
                elif noRect.collidepoint((mousex, mousey)):
                    return False
        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(text2Surf, text2Rect)
        DISPLAYSURF.blit(yesSurf, yesRect)
        DISPLAYSURF.blit(noSurf, noRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


# 棋盤
def getNewBoard():
    board = []
    for i in range(BOARDWIDTH):
        board.append([EMPTY_SPACE] * BOARDHEIGHT)
    return board


# 重置棋盤
def resetBoard(board):
    board[3][3] = WHITE_TILE
    board[3][4] = BLACK_TILE
    board[4][3] = BLACK_TILE
    board[4][4] = WHITE_TILE


def sideSelect():
    textSurf = FONT.render('Do you want to be first or second?', True, TEXTCOLOR, TEXTBGCOLOR1)
    textRect = textSurf.get_rect()
    textRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2))

    # First
    xSurf = BIGFONT.render('First', True, TEXTCOLOR, TEXTBGCOLOR1)
    xRect = xSurf.get_rect()
    xRect.center = (int(WINDOWWIDTH / 2) - 100, int(WINDOWHEIGHT / 2) + 40)

    # Second
    oSurf = BIGFONT.render('Second', True, TEXTCOLOR, TEXTBGCOLOR1)
    oRect = oSurf.get_rect()
    oRect.center = (int(WINDOWWIDTH / 2), int(WINDOWHEIGHT / 2) + 40)

    # Auto
    aSurf = BIGFONT.render('Auto', True, TEXTCOLOR, TEXTBGCOLOR1)
    aRect = aSurf.get_rect()
    aRect.center = (int(WINDOWWIDTH / 2) + 100, int(WINDOWHEIGHT / 2) + 40)

    while True:
        checkForQuit()
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if xRect.collidepoint((mousex, mousey)):
                    return Mode.FIRST
                elif oRect.collidepoint((mousex, mousey)):
                    return Mode.SECOND
                elif aRect.collidepoint((mousex, mousey)):
                    return Mode.AUTO

        DISPLAYSURF.blit(textSurf, textRect)
        DISPLAYSURF.blit(xSurf, xRect)
        DISPLAYSURF.blit(oSurf, oRect)
        DISPLAYSURF.blit(aSurf, aRect)
        pygame.display.update()
        MAINCLOCK.tick(FPS)


# 獲取可落子的位置
def getValidMoves(board, tile):
    validMoves = []

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if isValidMove(board, tile, x, y):
                validMoves.append((x, y))
    return validMoves


# 是否為合法走法
def isValidMove(board, tile, xstart, ystart):
    # 檢查該位置是否出界或已有棋子
    if board[xstart][ystart] != EMPTY_SPACE or not isOnBoard(xstart, ystart):
        return False

    # 臨時將tile放到指定的位置
    board[xstart][ystart] = tile

    if tile == WHITE_TILE:
        otherTile = BLACK_TILE
    else:
        otherTile = WHITE_TILE

    # 要被翻轉的棋子
    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        # 前進方向第一格是 合法範圍 且 是對方的棋子
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            # 一直走到出界或是不是對方棋子
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            # 出界了，則没有棋子要翻轉
            if not isOnBoard(x, y):
                continue
            # 是自己的棋子
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    # 回到了起點則结束
                    if x == xstart and y == ystart:
                        break
                    # 需要翻轉的棋子
                    tilesToFlip.append([x, y])

    # 將前面臨時放上的棋子去掉，即還原棋盤
    board[xstart][ystart] = EMPTY_SPACE

    # 没有要被翻轉的棋子，則走法非法
    if len(tilesToFlip) == 0:
        return False
    return tilesToFlip


# 是否出界
def isOnBoard(x, y):
    return 0 <= x < BOARDWIDTH and 0 <= y < BOARDHEIGHT


def drawBoard(board, current=None):
    DISPLAYSURF.blit(BGIMAGE, BGIMAGE.get_rect())
    for x in range(BOARDWIDTH + 1):
        startx = (x * SPACESIZE) + XMARGIN
        starty = YMARGIN
        endx = (x * SPACESIZE) + XMARGIN
        endy = YMARGIN + (BOARDHEIGHT * SPACESIZE)
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))
    for y in range(BOARDHEIGHT + 1):
        startx = XMARGIN
        starty = (y * SPACESIZE) + YMARGIN
        endx = XMARGIN + (BOARDWIDTH * SPACESIZE)
        endy = (y * SPACESIZE) + YMARGIN
        pygame.draw.line(DISPLAYSURF, GRIDLINECOLOR, (startx, starty), (endx, endy))

    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            centerx, centery = translateBoardToPixelCoord(x, y)
            if board[x][y] == WHITE_TILE or board[x][y] == BLACK_TILE:
                if board[x][y] == WHITE_TILE:
                    tileColor = WHITE
                else:
                    tileColor = BLACK
                pygame.draw.circle(DISPLAYSURF, tileColor, (centerx, centery), int(SPACESIZE / 2) - 4)
                if current == (x, y):
                    pygame.draw.rect(DISPLAYSURF, RED, (centerx - 4, centery - 4, 8, 8))
            if board[x][y] == HINT_TILE:
                pygame.draw.rect(DISPLAYSURF, HINTCOLOR, (centerx - 4, centery - 4, 8, 8))


# 獲取棋盤上雙方的棋子數
def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLACK_TILE:
                xscore += 1
            if board[x][y] == WHITE_TILE:
                oscore += 1
    return {BLACK_TILE: xscore, WHITE_TILE: oscore}


# 將一個tile棋子放到(xstart, ystart)
def makeMove(board, tile, xstart, ystart, realMove=False):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip is False:
        return False

    board[xstart][ystart] = tile

    if realMove:
        animateTileChange(tilesToFlip, tile, (xstart, ystart))

    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


def animateTileChange(tilesToFlip, tileColor, additionalTile):
    if tileColor == WHITE_TILE:
        additionalTileColor = WHITE
    else:
        additionalTileColor = BLACK
    additionalTileX, additionalTileY = translateBoardToPixelCoord(additionalTile[0], additionalTile[1])
    pygame.draw.circle(DISPLAYSURF, additionalTileColor, (additionalTileX, additionalTileY), int(SPACESIZE / 2) - 4)
    pygame.display.update()

    for rgbValues in range(0, 255, int(ANIMATIONSPEED * 2.55)):
        if rgbValues > 255:
            rgbValues = 255
        elif rgbValues < 0:
            rgbValues = 0

        if tileColor == WHITE_TILE:
            color = tuple([rgbValues] * 3)
        elif tileColor == BLACK_TILE:
            color = tuple([255 - rgbValues] * 3)

        for x, y in tilesToFlip:
            centerx, centery = translateBoardToPixelCoord(x, y)
            pygame.draw.circle(DISPLAYSURF, color, (centerx, centery), int(SPACESIZE / 2) - 4)
        pygame.display.update()
        MAINCLOCK.tick(FPS)
        checkForQuit()


# 複製棋盤
def getBoardCopy(board):
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]

    return dupeBoard


# 是否在角上
def isOnCorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


# AI
def getComputerMove(board, computerTile):
    # 獲取所有合法走法
    possibleMoves = getValidMoves(board, computerTile)
    dupeBoard = getBoardCopy(board)
    bestMove = AlgorithmFactory(setFunc[0], computerTile, possibleMoves, dupeBoard).getPosition()
    return bestMove


def translateBoardToPixelCoord(x, y):
    return XMARGIN + x * SPACESIZE + int(SPACESIZE / 2), YMARGIN + y * SPACESIZE + int(SPACESIZE / 2)


def getBoardWithValidMoves(board, tile):
    dupeBoard = copy.deepcopy(board)

    for x, y in getValidMoves(dupeBoard, tile):
        dupeBoard[x][y] = HINT_TILE
    return dupeBoard


def getSpaceClicked(mousex, mousey):
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if x * SPACESIZE + XMARGIN < mousex < (x + 1) * SPACESIZE + XMARGIN and \
                    y * SPACESIZE + YMARGIN < mousey < (y + 1) * SPACESIZE + YMARGIN:
                return x, y
    return None


def drawInfo(board, playerTile, computerTile, turn):
    scores = getScoreOfBoard(board)
    scoreSurf = FONT.render("Player Score: %s    Computer Score: %s    %s's Turn" %
                            (str(scores[playerTile]), str(scores[computerTile]), turn.value), True, TEXTCOLOR)
    scoreRect = scoreSurf.get_rect()
    scoreRect.bottomleft = (10, WINDOWHEIGHT - 5)
    DISPLAYSURF.blit(scoreSurf, scoreRect)


def checkForQuit():
    for event in pygame.event.get((QUIT, KEYUP)):
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()


if __name__ == '__main__':
    main()
