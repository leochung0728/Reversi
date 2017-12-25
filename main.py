
# coding: utf-8

# In[1]:

import pygame, sys, random, time #載入套件
from enum import Enum #列舉
from pygame.locals import * #載入套件


# In[2]:

BACKGROUNDCOLOR = (255, 255, 255)
BLACK = (255, 255, 255)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
CELLWIDTH = 50
CELLHEIGHT = 50
PIECEWIDTH = 40
PIECEHEIGHT = 40
BOARDX = 0
BOARDY = 0
FPS = 1000
useAIBattle = False #AI自鬥

# load img
boardImage = pygame.image.load('./img/board.png')
boardRect = boardImage.get_rect()
blackImage = pygame.image.load('./img/black.png')
blackRect = blackImage.get_rect()
whiteImage = pygame.image.load('./img/white.png')
whiteRect = whiteImage.get_rect()

gameOverStr = 'Game Over Score '

#玩家 
class Role(Enum):
    PLAYER = 'player'
    COMPUTER = 'computer'

#棋子顏色
class Side(Enum):
    BLACK = 'black'
    WHITE = 'white'

#模式
class Mode(Enum):
    FIRST = '先手'
    SECOND = '後攻'
    AI = 'AI_Battle'

# 離開
def terminate():
    pygame.quit()
    sys.exit()


# 重置棋盤
def resetBoard(board):
    board[3][3] = Side.BLACK
    board[3][4] = Side.WHITE
    board[4][3] = Side.WHITE
    board[4][4] = Side.BLACK


# 棋盤
def getNewBoard():
    board = []
    for i in range(8):
        board.append([None] * 8)
    return board


# 是否為合法走法
def isValidMove(board, tile, xstart, ystart):
    # 檢查該位置是否出界或已有棋子
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] is not None:
        return False

    # 臨時將tile放到指定的位置
    board[xstart][ystart] = tile

    if tile == Side.BLACK:
        otherTile = Side.WHITE
    else:
        otherTile = Side.BLACK

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
    board[xstart][ystart] = None  # restore the empty space

    # 没有要被翻轉的棋子，則走法非法
    if len(tilesToFlip) == 0:
        return False

    return tilesToFlip


# 是否出界
def isOnBoard(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


# 獲取可落子的位置
def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y):
                validMoves.append([x, y])
    return validMoves


# 獲取棋盤上雙方的棋子數
def getScoreOfBoard(board):
    xscore = 0
    oscore = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == Side.BLACK:
                xscore += 1
            if board[x][y] == Side.WHITE:
                oscore += 1
    return {Side.BLACK: xscore, Side.WHITE: oscore}


# 決定先手後手
def whoGoesFirst():
    if random.randint(0, 1) == 0:
        return Role.COMPUTER
    else:
        return Role.PLAYER


# 將一個tile棋子放到(xstart, ystart)
def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if tilesToFlip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True


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

    # 打亂順序
    random.shuffle(possibleMoves)

    # [x, y]在角上，則優先走
    for x, y in possibleMoves:
        if isOnCorner(x, y):
            return [x, y]

    bestScore = -1
    for x, y in possibleMoves:
        dupeBoard = getBoardCopy(board)
        makeMove(dupeBoard, computerTile, x, y)
        # 按照分數選擇走法，優先選擇翻轉後分數最多的走法
        score = getScoreOfBoard(dupeBoard)[computerTile]
        if score > bestScore:
            bestMove = [x, y]
            bestScore = score
    return bestMove


# 遊戲是否結束
def isGameOver(board):
    for x in range(8):
        for y in range(8):
            if board[x][y] is None:
                return False

    if len(getValidMoves(board, Side.WHITE)) != 0 or len(getValidMoves(board, Side.BLACK)) != 0:
        return False
    return True


def drawBoard(board):
    windowSurface.blit(boardImage, boardRect, boardRect)
    for x in range(0, 8):
        for y in range(0, 8):
            rectDst = pygame.Rect(BOARDX + x * CELLWIDTH + 5, BOARDY + y * CELLHEIGHT + 5, PIECEWIDTH, PIECEHEIGHT)
            if board[x][y] == Side.BLACK:
                windowSurface.blit(blackImage, rectDst, blackRect)
            elif board[x][y] == Side.WHITE:
                windowSurface.blit(whiteImage, rectDst, whiteRect)

def sideSelect():
    # 先手
    xSurf = BIGFONT.render('black', True, WHITE, BLUE)
    xRect = xSurf.get_rect()
    xRect.center = (int(400 / 2) - 120, int(400 / 2) + 40)

    # 後手
    oSurf = BIGFONT.render('white', True, WHITE, BLUE)
    oRect = oSurf.get_rect()
    oRect.center = (int(400 / 2) , int(400 / 2) + 40)
    
     # 後手
    aSurf = BIGFONT.render('AIBattle', True, WHITE, BLUE)
    aRect = aSurf.get_rect()
    aRect.center = (int(400 / 2) + 120, int(400 / 2) + 40)

    while True:
        for event in pygame.event.get():
            #取得事件
            if event.type == QUIT:
                terminate()
            if event.type == MOUSEBUTTONUP:
                x, y = event.pos
                if xRect.collidepoint((x, y)):
                    return Mode.FIRST
                elif oRect.collidepoint((x, y)):
                    return Mode.SECOND
                elif aRect.collidepoint((x, y)):
                    return Mode.AI
        windowSurface.blit(xSurf, xRect)
        windowSurface.blit(oSurf, oRect)
        windowSurface.blit(aSurf, aRect)
        pygame.display.update()
        mainClock.tick(FPS)


if __name__ == '__main__':
    # 初始化
    pygame.init()
    mainClock = pygame.time.Clock()
    basicFont = pygame.font.SysFont(None, 48)
    FONT = pygame.font.Font(None, 16)
    BIGFONT = pygame.font.Font(None, 32)

    mainBoard = getNewBoard()
    resetBoard(mainBoard)

    # 設置窗口
    windowSurface = pygame.display.set_mode((boardRect.width, boardRect.height))
    pygame.display.set_caption('Reversi')

    sel = sideSelect()
    if sel == Mode.AI:
        useAIBattle = True
        turn = Role.PLAYER
        playerTile = Side.BLACK
        computerTile = Side.WHITE
    elif sel == Mode.FIRST:
        turn = Role.PLAYER
        playerTile = Side.BLACK
        computerTile = Side.WHITE
    elif sel == Mode.SECOND:
        turn = Role.COMPUTER
        playerTile = Side.WHITE
        computerTile = Side.BLACK
        
    # 遊戲主循環
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if isGameOver(mainBoard):
                drawBoard(mainBoard)
                scorePlayer = getScoreOfBoard(mainBoard)[playerTile]
                scoreComputer = getScoreOfBoard(mainBoard)[computerTile]
                outputStr = gameOverStr + str(scorePlayer) + ":" + str(scoreComputer)
                text = basicFont.render(outputStr, True, BLACK, BLUE)
                textRect = text.get_rect()
                textRect.centerx = windowSurface.get_rect().centerx
                textRect.centery = windowSurface.get_rect().centery
                windowSurface.blit(text, textRect)

            elif turn == Role.PLAYER:
                if useAIBattle:
                    col, row = getComputerMove(mainBoard, playerTile)
                    if makeMove(mainBoard, playerTile, col, row):
                        if len(getValidMoves(mainBoard, computerTile)) != 0:
                            turn = Role.COMPUTER
                else:
                    if event.type == MOUSEBUTTONUP:
                        x, y = event.pos
                        col = int((x - BOARDX) / CELLWIDTH)
                        row = int((y - BOARDY) / CELLHEIGHT)
                        if makeMove(mainBoard, playerTile, col, row):
                            if len(getValidMoves(mainBoard, computerTile)) != 0:
                                turn = Role.COMPUTER
                drawBoard(mainBoard)

            elif turn == Role.COMPUTER:
                # pygame.time.wait(2000)

                col, row = getComputerMove(mainBoard, computerTile)
                if makeMove(mainBoard, computerTile, col, row):
                    if len(getValidMoves(mainBoard, playerTile)) != 0:
                        turn = Role.PLAYER
                drawBoard(mainBoard)

        pygame.display.update()
        mainClock.tick(FPS)


# In[ ]:



