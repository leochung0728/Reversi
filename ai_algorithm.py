import random, copy
import itertools
import pandas as pd
import numpy as np
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
        return bestValue


# AlphaBeta
class Algorithm_4(object):

    def __init__(self, board, tile):
        self.board = board
        self.tile = tile
        self.depth = 2
        self.minEvalBoard = -5  # float('-inf')
        self.maxEvalBoard = 20  # float('inf')
        self.maximizingPlayer = True

    def getBestMove(self):
        maxPoints = float('-inf')
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
            mobility = getPossibleConvertions(board, tile, possibleMoves) - getPossibleConvertions(board, oppositeTile, oppositePossibleMoves)
            stability = self.getStableDiscsCount(board, tile) - self.getStableDiscsCount(board, oppositeTile) * 8 * 2 / 3
            return mobility + stability

    def alphabeta(self, board, tile, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or len(getValidMoves(board, tile)) == 0:
            return self.evalBoard(board, tile)

        otherTile = 0 if tile == 1 else 1

        if maximizingPlayer:
            val = alpha
            for x, y in getValidMoves(board, tile):
                boardTemp = copy.deepcopy(board)
                makeMove(boardTemp, tile, x, y)
                valTemp = self.alphabeta(boardTemp, tile, depth - 1, alpha, beta, False)
                val = max(val, valTemp)
                if val >= beta:
                    break
        else:
            val = beta
            for x, y in getValidMoves(board, otherTile):
                boardTemp = copy.deepcopy(board)
                makeMove(boardTemp, otherTile, x, y)
                valTemp = self.alphabeta(boardTemp, tile, depth - 1, alpha, beta, True)
                val = min(val, valTemp)
                if val <= alpha:
                    break
        return val

    def getStableDiscsCount(self, board, tile):
        return self.getStableDiscsFromCorner(board, tile) + \
               self.getStableDiscsFromEdge(board, tile)

    @staticmethod
    def getStableDiscsFromCorner(board, tile):
        starts = [(0, 0), (0, 7), (7, 0), (7, 7)]
        result = 0
        for start in starts:
            startX, startY = start
            rowIndexChange = 1 if startY == 0 else -1
            colIndexChange = 1 if startX == 0 else -1
            rowIndexLimit = 8 if startY == 0 else 0
            colIndexLimit = 8 if startX == 0 else 0

            for rowIndex in np.arange(startY, rowIndexLimit, rowIndexChange):
                for colIndex in np.arange(startX, colIndexLimit, colIndexChange):
                    if board[rowIndex][colIndex] == tile:
                        result += 1
                    else:
                        break
                if (colIndexChange > 0 and colIndex < 8) or (colIndexChange < 0 and colIndex > 0):
                    colIndexLimit = colIndex - colIndexChange
                    if colIndexChange > 0 and colIndexLimit == 0:
                        colIndexLimit += 1
                    elif colIndexChange < 0 and colIndexLimit == 7:
                        colIndexLimit -= 1

                    if (colIndexChange > 0 and colIndexLimit < 0) or (colIndexChange < 0 and colIndexLimit > 7):
                        break
        return result

    def getStableDiscsFromEdge(self, board, tile):
        coordinates = [0, 7]
        isHorizontals = [True, False]
        result = 0
        for coordinate, isHorizontal in list(itertools.product(coordinates, isHorizontals)):
            if self.isEdgeFull(board, coordinate, isHorizontal):
                oppositeTileDiscsPassed = False

                for otherCoordinate in range(0, 8):
                    fieldtile = board[coordinate][otherCoordinate] if isHorizontal else board[otherCoordinate][coordinate]
                    if fieldtile == tile:
                        oppositeTileDiscsPassed = True
                    elif oppositeTileDiscsPassed:
                        consecutiveDiscsCount = 0
                        while otherCoordinate < 8 and fieldtile == tile:
                            consecutiveDiscsCount += 1
                            otherCoordinate += 1
                            if otherCoordinate < 8:
                                fieldtile = board[coordinate][otherCoordinate] if isHorizontal else board[otherCoordinate][coordinate]

                        if otherCoordinate != 8:
                            result += consecutiveDiscsCount
                            oppositeTileDiscsPassed = True
        return result

    @staticmethod
    def isEdgeFull(board, coordinate, isHorizontal):
        for otherCoordinate in range(0, 8):
            if (isHorizontal and board[coordinate][otherCoordinate] is None) or (not isHorizontal and board[otherCoordinate][coordinate] is None):
                return False
        return True


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
