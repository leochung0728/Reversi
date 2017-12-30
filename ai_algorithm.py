import random, copy
import pandas as pd
from reversi import *


class Algorithm_1(object):

    def __init__(self, board, tile):
        self.board = board
        self.tile = tile

    def getBestMove(self):
        bestMove = None

        possibleMoves = getValidMoves(self.board, self.tile)
        random.shuffle(possibleMoves)

        for x, y in possibleMoves:
            if isOnCorner(x, y):
                return [x, y]

        bestScore = -1
        for x, y in possibleMoves:
            dupeBoard = self.board
            makeMove(dupeBoard, self.tile, x, y)
            score = getScoreOfBoard(dupeBoard)[self.tile]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
        return bestMove

source_csv = pd.read_csv('Algorithm_2.csv')
class Algorithm_2(object):

    def __init__(self, board, tile):
        self.board = board
        self.tile = tile

    def getBestMove(self):
        bestMove = None
        possibleMoves = getValidMoves(self.board, self.tile)
        random.shuffle(possibleMoves)
        nowScore = -99
        for x, y in possibleMoves:
            source = source_csv[source_csv.columns[x]][y]
            if source > nowScore:
                nowScore = source
                bestMove = [x,y]
        #print(nowScore)
        return bestMove

# Minimax
class Algorithm_3(object):

    # evalTable = [
    #     [ 20,  -5,  10,   5,   5,  10,  -5,  20],
    #     [ -5, -10,   1,   1,   1,   1, -10,  -5],
    #     [ 10,   1,  50,   1,   1,  50,   1,  10],
    #     [ 10,   1,   1,   1,   1,   1,   1,   5],
    #     [ 10,   1,   1,   1,   1,   1,   1,   5],
    #     [ 10,   1,  50,   1,   1,  50,   1,  10],
    #     [ -5, -10,   1,   1,   1,   1, -10,  -5],
    #     [ 20,  -5,  10,   5,   5,  10,  -5,  20],
    # ]

    def __init__(self, board, tile):
        self.board = board
        self.tile = tile
        self.depth = 3
        self.minEvalBoard = -1
        self.maxEvalBoard = 101  # n^2+4n+4+1, n=8
        self.maximizingPlayer = True

    def getBestMove(self):
        maxPoints = 0
        bestMove = None
        for x in range(8):
            for y in range(8):
                if isValidMove(self.board, self.tile, x, y):
                    boardTemp = copy.deepcopy(self.board)
                    points = self.minimax(boardTemp, self.tile, self.depth, self.maximizingPlayer)
                    if points > maxPoints:
                        maxPoints = points
                        bestMove = [x, y]
        return bestMove

    def evalBoard(self, board, tile):
        tot = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == tile:
                    if (x == 0 or x == 7) and (y == 0 or y == 7):
                        tot += 20  # corner
                    elif (x == 0 or x == 7) or (y == 0 or y == 7):
                        tot += 2  # side
                    else:
                        tot += 1
        return tot

    def minimax(self, board=None, tile=None, depth=None, maximizingPlayer=None):
        if board is None:
            board = self.board
        if tile is None:
            tile = self.tile
        if depth is None:
            depth = self.depth
        if maximizingPlayer is None:
            maximizingPlayer = self.maximizingPlayer

        if depth == 0 or len(getValidMoves(board, tile)) == 0:
            return self.evalBoard(board, tile)
        print(depth)
        if maximizingPlayer:
            bestValue = self.minEvalBoard
            for x in range(8):
                for y in range(8):
                    if isValidMove(board, tile, x, y):
                        boardTemp = copy.deepcopy(board)
                        makeMove(boardTemp, tile, x, y)
                        v = self.minimax(boardTemp, tile, depth - 1, False)
                        bestValue = max(bestValue, v)
        else:
            bestValue = self.maxEvalBoard
            for x in range(8):
                for y in range(8):
                    if isValidMove(board, tile, x, y):
                        boardTemp = copy.deepcopy(board)
                        makeMove(boardTemp, tile, x, y)
                        v = self.minimax(boardTemp, tile, depth - 1, True)
                        bestValue = min(bestValue, v)
        print(bestValue)
        return bestValue


# AlphaBeta
class Algorithm_4(object):

    # evalTable = [
    #     [ 20,  -5,  10,   5,   5,  10,  -5,  20],
    #     [ -5, -10,   1,   1,   1,   1, -10,  -5],
    #     [ 10,   1,  50,   1,   1,  50,   1,  10],
    #     [ 10,   1,   1,   1,   1,   1,   1,   5],
    #     [ 10,   1,   1,   1,   1,   1,   1,   5],
    #     [ 10,   1,  50,   1,   1,  50,   1,  10],
    #     [ -5, -10,   1,   1,   1,   1, -10,  -5],
    #     [ 20,  -5,  10,   5,   5,  10,  -5,  20],
    # ]

    def __init__(self, board, tile):
        self.board = board
        self.tile = tile
        self.depth = 1
        self.minEvalBoard = -1
        self.maxEvalBoard = 101  # n^2+4n+4+1, n=8
        self.maximizingPlayer = True

    def getBestMove(self):
        maxPoints = 0
        bestMove = None
        for x in range(8):
            for y in range(8):
                if isValidMove(self.board, self.tile, x, y):
                    boardTemp = copy.deepcopy(self.board)
                    points = self.alphabeta(boardTemp, self.tile, self.depth, self.minEvalBoard, self.maxEvalBoard,
                                            self.maximizingPlayer)
                    if points > maxPoints:
                        maxPoints = points
                        bestMove = [x, y]
        return bestMove

    def evalBoard(self, board, tile):
        oppositeTile = 0 if tile == 1 else 1

        possibleMoves = getValidMoves(board, tile)
        oppositePossibleMoves = getValidMoves(board, oppositeTile)

        if len(possibleMoves) == 0 and len(oppositePossibleMoves) == 0:
            score = getScoreOfBoard(board)
            result = score[tile] - score[oppositeTile]
            addend = pow(8, 4) + pow(8, 3)
            if result < 0:
                addend = -addend
            return result + addend
        else:
            mobility = getPossibleConvertions(board, tile, possibleMoves) - getPossibleConvertions(board, oppositeTile,
                                                                                                   oppositePossibleMoves)
            return mobility

    def alphabeta(self, board=None, tile=None, depth=None, alpha=None, beta=None, maximizingPlayer=None):
        if board is None:
            board = self.board
        if tile is None:
            tile = self.tile
        if depth is None:
            depth = self.depth
        if alpha is None:
            alpha = self.minEvalBoard
        if beta is None:
            beta = self.maxEvalBoard
        if maximizingPlayer is None:
            maximizingPlayer = self.maximizingPlayer

        if depth == 0 or len(getValidMoves(board, tile)) == 0:
            return self.evalBoard(board, tile)

        v = None
        if maximizingPlayer:
            v = alpha
            for x, y in getValidMoves(board, tile):
                boardTemp = copy.deepcopy(board)
                makeMove(boardTemp, tile, x, y)
                v = self.alphabeta(boardTemp, tile, depth - 1, alpha, beta, False)
                v = max(alpha, v)
                if v >= beta:
                    break
        else:
            v = beta
            for x, y in getValidMoves(board, tile):
                boardTemp = copy.deepcopy(board)
                makeMove(boardTemp, tile, x, y)
                v = self.alphabeta(boardTemp, tile, depth - 1, alpha, beta, True)
                v = min(beta, v)
                if v <= alpha:
                    break
        print(v)
        return v

class Algorithm_5(object):
    def __init__(self, board, tile):
        self.board = board
        self.tile = tile

    def getBestMove(self):
        bestMove = None
        possibleMoves = getValidMoves(self.board, self.tile)
        random.shuffle(possibleMoves)
        diff = []
        for x, y in possibleMoves:
            bestMove1 = source_csv[source_csv.columns[x]][y]
            bestMove2 = self.checkOtherPlayerSource([x, y])
            diff.append((x, y, bestMove2 - bestMove1))
        diff = sorted(diff, key=lambda x: x[2])
        better = diff[0]
        return [better[0], better[1]]

    # 檢查對方的分數
    def checkOtherPlayerSource(self, pBestMove):
        otherTile = self.tile
        if self.tile == 1:
            otherTile = 0
        pinBoard = self.board
        pinBoard[pBestMove[0]][pBestMove[1]] = self.tile
        Moves = getValidMoves(pinBoard, otherTile)
        return self.getBestScore(Moves)

    # 計算獲得分數
    def getBestScore(self, pPossibleMoves):
        nowScore = -99
        for x, y in pPossibleMoves:
            source = source_csv[source_csv.columns[x]][y]
            if source > nowScore:
                nowScore = source
                BestScore = [x, y, source]
        return nowScore
