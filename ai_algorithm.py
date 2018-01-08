import random, copy
import sys
import math
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
        self.depth = 3
        self.minEvalBoard = float('-inf')
        self.maxEvalBoard = float('inf')
        self.maximizingPlayer = True

    def getBestMove(self):
        maxPoints = float('-inf')
        bestMove = None
        for x, y in getValidMoves(self.board, self.tile):
            boardTemp = copy.deepcopy(self.board)
            makeMove(boardTemp, self.tile, x, y)
            points = self.alphabeta(boardTemp, self.tile, self.depth, self.minEvalBoard, self.maxEvalBoard,
                                    not self.maximizingPlayer)
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

#棋盤物件
class Board(list):
    def __init__(self, board):
        list.__init__([])
        self.extend(board)
        self.DEFAULT_BOARD_SIZE = 8
        self.Size = self.DEFAULT_BOARD_SIZE
        self.mInvertedDiscsLastMove = 0
        #self.InvertedDiscsLastMove = self.mInvertedDiscsLastMove 
        self.mFieldColors = []
        for rowIndex in range(self.Size):
            for columnIndex in range(self.Size):
                self.mFieldColors.append(self[rowIndex])

    def SetFieldColor(self,rowIndex,columnIndex,color):
        if self.CanSetFieldColor(rowIndex,columnIndex,color):
            self[columnIndex][rowIndex] = color
            self.InvertOpponentDisks(rowIndex,columnIndex,color)

    def CanSetFieldColor(self,rowIndex,columnIndex,color):
        hasColor = True if self[columnIndex][rowIndex] != None else False
        if not hasColor:
            if color == None:
                return True
            else:
                for rowIndexChange in range(-1,2):
                    for columnIndexChange in range(-1,2):
                        if rowIndexChange != 0 or columnIndexChange != 0:
                            if self.CheckDirection(rowIndex,columnIndex,rowIndexChange,columnIndexChange,color):
                                return True
        return False
    
    def CheckDirection(self,rowIndex,columnIndex,rowIndexChange,columnIndexChange,color):
        areOpositeColorDiscsFound = False
        rowIndex += rowIndexChange
        columnIndex += columnIndexChange
        while rowIndex >= 0 and rowIndex < self.Size and columnIndex >= 0 and columnIndex < self.Size:
            if areOpositeColorDiscsFound:
                if self[columnIndex][rowIndex] == color:
                    return True
                elif self[columnIndex][rowIndex] == None:
                    return False
            else:
                opositeColor = Algorithm_6.GetOpposite(color)
                if self[columnIndex][rowIndex] == opositeColor:
                    areOpositeColorDiscsFound = True
                else:
                    return False
            rowIndex += rowIndexChange
            columnIndex += columnIndexChange

        return False

    def CanSetAnyField(self,color):
        for rowIndex in range(self.Size):
            for columnIndex in range(self.Size):
                if self.CanSetFieldColor(rowIndex,columnIndex,color):
                    return True
        return True
    
    def GetDiscsCount(self,color):
        result = 0
        for rowIndex in range(self.Size):
            for columnIndex in range(self.Size):
                if self[columnIndex][rowIndex] == color:
                    result = result + 1
        return result

    def InvertOpponentDisks(self,rowIndex,columnIndex,color):
        self.mInvertedDiscsLastMove = 0
        for rowIndexChange in range(-1,2):
            for columnIndexChange in range(-1,2):
                if rowIndexChange != 0 or columnIndexChange != 0:
                   if self.CheckDirection(rowIndex,columnIndex,rowIndexChange, columnIndexChange, color):
                       self.InvertDirection(rowIndex, columnIndex, rowIndexChange, columnIndexChange, color)

    def InvertDirection(self,rowIndex,columnIndex,rowIndexChange,columnIndexChange,color):
        opositeColor = Algorithm_6.GetOpposite(color)
        rowIndex += rowIndexChange
        columnIndex += columnIndexChange
        while self[columnIndex][rowIndex] == opositeColor:
             self[columnIndex][rowIndex] = color
             self.mInvertedDiscsLastMove = self.mInvertedDiscsLastMove + 1
             rowIndex += rowIndexChange
             columnIndex += columnIndexChange
    
    def Clone(self):
        return copy.deepcopy(self)

Algorithm_MaxDepth = 4 #2-7
class Algorithm_6(object):
    #建構子
    def __init__(self, board, tile):
        self.board = Board(board)
        self.tile = tile
        self.resultRowIndex = 0
        self.resultColumnIndex = 0
        self.MAX_BOARD_VALUE = 2147483647
        self.MIN_BOARD_VALUE = - self.MAX_BOARD_VALUE
        self.MaxDepth = Algorithm_MaxDepth
    #取得最佳路線
    def getBestMove(self):
        self.GetNextMove(self.board,True,1,self.MIN_BOARD_VALUE,self.MAX_BOARD_VALUE)
        return [self.resultColumnIndex,self.resultRowIndex]
    
    #取得下一步路線
    def GetNextMove(self,board,isMaximizing,currentDepth,alpha,beta):
        self.resultRowIndex = 0
        self.resultColumnIndex = 0

        color = self.tile if isMaximizing else self.GetOpposite(self.tile)
        playerSkipsMove = False
        possibleMoves = None
        isFinalMove = (currentDepth >= self.MaxDepth)
        if not isFinalMove:
            possibleMoves = self.GetPossibleMoves(board, color)
            if len(possibleMoves) == 0:
                playerSkipsMove = True
                possibleMoves = self.GetPossibleMoves(board, self.GetOpposite(color))
            isFinalMove = (len(possibleMoves) == 0)
        if isFinalMove:
            self.resultRowIndex = -1
            self.resultColumnIndex = -1
            return self.EvaluateBoard(board)
        else:
            bestBoardValue = self.MIN_BOARD_VALUE if isMaximizing else self.MAX_BOARD_VALUE
            bestMoveRowIndex = -1
            bestMoveColumnIndex = -1
            for nextMove in possibleMoves:
                rowIndex = nextMove[1]
                columnIndex = nextMove[0]
                nextBoard = board.Clone()
                nextBoard.SetFieldColor(rowIndex,columnIndex,color)

                nextIsMaximizing = isMaximizing if playerSkipsMove else  not isMaximizing
                #dummyIndex # values of resultRowIndex and resultColumnIndex are not needed in recursive function calls
                currentBoardValue = self.GetNextMove(nextBoard,nextIsMaximizing,currentDepth + 1 ,alpha,beta)
                if isMaximizing:
                    if currentBoardValue > bestBoardValue:
                        bestBoardValue = currentBoardValue
                        bestMoveRowIndex = rowIndex
                        bestMoveColumnIndex = columnIndex
                        if bestBoardValue > alpha:
                            alpha = bestBoardValue
                        if bestBoardValue >= beta:
                            break
                else:
                    if currentBoardValue < bestBoardValue:
                        bestBoardValue = currentBoardValue
                        bestMoveRowIndex = rowIndex
                        bestMoveColumnIndex = columnIndex
                        if bestBoardValue < beta:
                            beta = bestBoardValue
                        if bestBoardValue <= alpha:
                            break

        self.resultRowIndex = bestMoveRowIndex
        self.resultColumnIndex = bestMoveColumnIndex
        return bestBoardValue
    #取得顏色
    @staticmethod
    def GetOpposite(color):
        if color == 0:
            return 1
        elif color == 1:
            return 0
        else:
            return None
    
    #取得路徑
    def GetPossibleMoves(self,board,color):
        result = []
        for rowIndex in range(board.Size):
            for columnIndex in range(board.Size):
                if board.CanSetFieldColor(rowIndex,columnIndex,color):
                    result.append([rowIndex,columnIndex])
        return result 

    def EvaluateBoard(self,board):
        color = self.tile
        oppositeColor = self.GetOpposite( self.tile)
        oppositePlayerPossibleMoves = self.GetPossibleMoves(board,oppositeColor)
        possibleMoves = self.GetPossibleMoves(board,color)
        if len(possibleMoves) == 0 and len(oppositePlayerPossibleMoves) ==0:
            result = self.GetDiscsCount(color) - self.GetDiscsCount(oppositeColor)
            addend = math.pow(board.Size,4) + math.pow(board.Size,3)# because it is a terminal state, its weight must be bigger than the heuristic ones
            if result < 0:
                 addend = -addend
            return result + addend
        else:
            mobility = self.GetPossibleConvertions(board,color,possibleMoves) - self.GetPossibleConvertions(board,oppositeColor,oppositePlayerPossibleMoves)
            stability = (self.GetStableDiscsCount(board,color) - self.GetStableDiscsCount(board,oppositeColor)) * board.Size * 2 / 3
            return mobility + stability
    
    def GetPossibleConvertions(self,board,color,possibleMoves):
        result = 0
        for move in possibleMoves:
            newBoard = board.Clone()
            columnIndex = move[0]
            rowIndex = move[1]
            newBoard.SetFieldColor(rowIndex, columnIndex, color)
            result += newBoard.mInvertedDiscsLastMove
        return result

    def GetStableDiscsCount(self,board,color):
        pCa = self.GetStableDiscsFromCorner(board, color, 0, 0)
        pCb = self.GetStableDiscsFromCorner(board, color, 0, board.Size - 1)
        pCc = self.GetStableDiscsFromCorner(board, color, board.Size - 1, 0)
        pCd = self.GetStableDiscsFromCorner(board, color, board.Size - 1, board.Size - 1)
        pCe = self.GetStableDiscsFromEdge(board, color, 0, False)
        pCf = self.GetStableDiscsFromEdge(board, color, board.Size - 1, False)
        pCg = self.GetStableDiscsFromEdge(board, color, 0, True)
        pCh = self.GetStableDiscsFromEdge(board, color, board.Size - 1, True)
        return pCa  + pCb +pCc + pCd + pCe + pCf + pCg + pCh
    
    def GetStableDiscsFromCorner(self,board,color,cornerRowIndex,cornerColumnIndex):
        result = 0
        rowIndexChange =  1 if cornerRowIndex == 0 else -1
        columnIndexChange = 1 if cornerColumnIndex == 0 else -1

        rowIndex = cornerRowIndex
        rowIndexLimit =  board.Size if cornerRowIndex == 0 else 0
        columnIndexLimit = board.Size if cornerColumnIndex == 0 else 0
        rowIndex = cornerRowIndex
        while rowIndex != rowIndexLimit:
            columnIndex = cornerColumnIndex
            while columnIndex != columnIndexLimit:
                if board[columnIndex][rowIndex] == color:
                    result = result +1
                else:
                    break
                columnIndex += columnIndexChange
            
            if (columnIndexChange > 0 and columnIndex < board.Size ) or (columnIndexChange < 0 and columnIndex > 0):
                columnIndexLimit = columnIndex - columnIndexChange
                if columnIndexChange > 0 and columnIndexLimit == 0:
                    columnIndexLimit = columnIndexLimit +1
                elif columnIndexChange < 0 and columnIndexLimit == board.Size - 1:
                    columnIndexLimit = columnIndexLimit -1
                if (columnIndexChange > 0 and columnIndexLimit < 0) or (columnIndexChange < 0 and columnIndexLimit > board.Size - 1):
                    break
            rowIndex += rowIndexChange
        return result

    def GetStableDiscsFromEdge(self,board,color,edgeCoordinate,isHorizontal):
        result = 0
        if self.IsEdgeFull(board, edgeCoordinate, isHorizontal):
            oppositeColorDiscsPassed = False
            for otherCoordinate in range(board.Size):
                fieldColor = board[otherCoordinate][edgeCoordinate] if isHorizontal else board[edgeCoordinate][otherCoordinate]
                if fieldColor != color:
                    oppositeColorDiscsPassed = True
                elif oppositeColorDiscsPassed:
                    consecutiveDiscsCount = 0
                    while otherCoordinate < board.Size and fieldColor == color:
                        consecutiveDiscsCount = consecutiveDiscsCount +1
                        otherCoordinate = otherCoordinate +1
                        if otherCoordinate < board.Size:
                            fieldColor = board[otherCoordinate][edgeCoordinate] if isHorizontal else board[edgeCoordinate][otherCoordinate]
                    if otherCoordinate != board.Size:
                        result += consecutiveDiscsCount
                        oppositeColorDiscsPassed = True
        return result           

    def IsEdgeFull(self,board,edgeCoordinate,isHorizontal):
        for otherCoordinate in range(board.Size):
            if (isHorizontal and board[otherCoordinate][ edgeCoordinate] == None) or (not isHorizontal and board[edgeCoordinate][ otherCoordinate] == None):
                return False
        return True


#棋盤物件
class Board2(list):
    def __init__(self, board):
        list.__init__([])
        self.DEFAULT_BOARD_SIZE = 8
        self.Size = self.DEFAULT_BOARD_SIZE
        self.mInvertedDiscsLastMove = 0
        #self.InvertedDiscsLastMove = self.mInvertedDiscsLastMove 
        pBoard = []
        for i in range(self.Size):
            pBoard.append([None] * self.Size)
        for i in range(self.Size):
            for j in range(self.Size):
                pBoard[i][j] = board[j][i]
        self.extend(pBoard)

    def SetFieldColor(self,rowIndex,columnIndex,color):
        if self.CanSetFieldColor(rowIndex,columnIndex,color):
            self[rowIndex][columnIndex] = color
            self.InvertOpponentDisks(rowIndex,columnIndex,color)

    def CanSetFieldColor(self,rowIndex,columnIndex,color):
        hasColor = True if self[rowIndex][columnIndex] != None else False
        if not hasColor:
            if color == None:
                return True
            else:
                for rowIndexChange in range(-1,2):
                    for columnIndexChange in range(-1,2):
                        if rowIndexChange != 0 or columnIndexChange != 0:
                            if self.CheckDirection(rowIndex,columnIndex,rowIndexChange,columnIndexChange,color):
                                return True
        return False
    
    def CheckDirection(self,rowIndex,columnIndex,rowIndexChange,columnIndexChange,color):
        areOpositeColorDiscsFound = False
        rowIndex += rowIndexChange
        columnIndex += columnIndexChange
        while rowIndex >= 0 and rowIndex < self.Size and columnIndex >= 0 and columnIndex < self.Size:
            if areOpositeColorDiscsFound:
                if self[rowIndex][columnIndex] == color:
                    return True
                elif self[rowIndex][columnIndex] == None:
                    return False
            else:
                opositeColor = Algorithm_7.GetOpposite(color)
                if self[rowIndex][columnIndex] == opositeColor:
                    areOpositeColorDiscsFound = True
                else:
                    return False
            rowIndex += rowIndexChange
            columnIndex += columnIndexChange

        return False

    def CanSetAnyField(self,color):
        for rowIndex in range(self.Size):
            for columnIndex in range(self.Size):
                if self.CanSetFieldColor(rowIndex,columnIndex,color):
                    return True
        return True
    
    def GetDiscsCount(self,color):
        result = 0
        for rowIndex in range(self.Size):
            for columnIndex in range(self.Size):
                if self[rowIndex][columnIndex] == color:
                    result = result + 1
        return result

    def InvertOpponentDisks(self,rowIndex,columnIndex,color):
        self.mInvertedDiscsLastMove = 0
        for rowIndexChange in range(-1,2):
            for columnIndexChange in range(-1,2):
                if rowIndexChange != 0 or columnIndexChange != 0:
                   if self.CheckDirection(rowIndex,columnIndex,rowIndexChange, columnIndexChange, color):
                       self.InvertDirection(rowIndex, columnIndex, rowIndexChange, columnIndexChange, color)

    def InvertDirection(self,rowIndex,columnIndex,rowIndexChange,columnIndexChange,color):
        opositeColor = Algorithm_6.GetOpposite(color)
        rowIndex += rowIndexChange
        columnIndex += columnIndexChange
        while self[rowIndex][columnIndex] == opositeColor:
             self[rowIndex][columnIndex] = color
             self.mInvertedDiscsLastMove = self.mInvertedDiscsLastMove + 1
             rowIndex += rowIndexChange
             columnIndex += columnIndexChange
    
    def Clone(self):
        return copy.deepcopy(self)

class Algorithm_7(object):
        #建構子
    def __init__(self, board, tile):
        self.board = Board2(board)
        self.tile = tile
        self.resultRowIndex = 0
        self.resultColumnIndex = 0
        self.MAX_BOARD_VALUE = 2147483647
        self.MIN_BOARD_VALUE = - self.MAX_BOARD_VALUE
        self.MaxDepth = 7
    #取得最佳路線
    def getBestMove(self):
        self.GetNextMove(self.board,True,1,self.MIN_BOARD_VALUE,self.MAX_BOARD_VALUE)
        #print( [self.resultRowIndex,self.resultColumnIndex])
        return [self.resultColumnIndex,self.resultRowIndex]
    
    #取得下一步路線
    def GetNextMove(self,board,isMaximizing,currentDepth,alpha,beta):
        self.resultRowIndex = 0
        self.resultColumnIndex = 0

        color = (self.GetOpposite(self.tile),self.tile)[isMaximizing]
        playerSkipsMove = False
        possibleMoves = None
        isFinalMove = (currentDepth >= self.MaxDepth)
        if not isFinalMove:
            possibleMoves = self.GetPossibleMoves(board, color)
            if len(possibleMoves) == 0:
                playerSkipsMove = True
                possibleMoves = self.GetPossibleMoves(board, self.GetOpposite(color))
            isFinalMove = (len(possibleMoves) == 0)
        if isFinalMove:
            self.resultRowIndex = -1
            self.resultColumnIndex = -1
            return self.EvaluateBoard(board)
        else:
            bestBoardValue = (self.MAX_BOARD_VALUE,self.MIN_BOARD_VALUE)[isMaximizing]
            bestMoveRowIndex = -1
            bestMoveColumnIndex = -1
            for nextMove in possibleMoves:
                rowIndex = nextMove[0]
                columnIndex = nextMove[1]
                nextBoard = board.Clone()
                nextBoard.SetFieldColor(rowIndex,columnIndex,color)

                nextIsMaximizing = (not isMaximizing,isMaximizing)[playerSkipsMove]
                #dummyIndex # values of resultRowIndex and resultColumnIndex are not needed in recursive function calls
                currentBoardValue = self.GetNextMove(nextBoard,nextIsMaximizing,currentDepth + 1 ,alpha,beta)
                currentBoardValue = int(currentBoardValue)
                if isMaximizing:
                    if currentBoardValue > bestBoardValue:
                        bestBoardValue = currentBoardValue
                        bestMoveRowIndex = rowIndex
                        bestMoveColumnIndex = columnIndex
                        if bestBoardValue > alpha:
                            alpha = bestBoardValue
                        if bestBoardValue >= beta:
                            break
                else:
                    if currentBoardValue < bestBoardValue:
                        bestBoardValue = currentBoardValue
                        bestMoveRowIndex = rowIndex
                        bestMoveColumnIndex = columnIndex
                        if bestBoardValue < beta:
                            beta = bestBoardValue
                        if bestBoardValue <= alpha:
                            break

        self.resultRowIndex = bestMoveRowIndex
        self.resultColumnIndex = bestMoveColumnIndex
        return bestBoardValue
    #取得顏色
    @staticmethod
    def GetOpposite(color):
        if color == 0:
            return 1
        elif color == 1:
            return 0
        else:
            return None
    
    #取得路徑
    def GetPossibleMoves(self,board,color):
        result = []
        for rowIndex in range(board.Size):
            for columnIndex in range(board.Size):
                if board.CanSetFieldColor(rowIndex,columnIndex,color):
                    result.append([rowIndex,columnIndex])
        return result 

    def EvaluateBoard(self,board):
        color = self.tile
        oppositeColor = self.GetOpposite( self.tile)
        oppositePlayerPossibleMoves = self.GetPossibleMoves(board,oppositeColor)
        possibleMoves = self.GetPossibleMoves(board,color)
        if len(possibleMoves) == 0 and len(oppositePlayerPossibleMoves) ==0:
            result = board.GetDiscsCount(color) - board.GetDiscsCount(oppositeColor)
            addend = math.pow(board.Size,4) + math.pow(board.Size,3)# because it is a terminal state, its weight must be bigger than the heuristic ones
            if result < 0:
                 addend = -addend
            return result + addend
        else:
            mobility = self.GetPossibleConvertions(board,color,possibleMoves) - self.GetPossibleConvertions(board,oppositeColor,oppositePlayerPossibleMoves)
            stability = (self.GetStableDiscsCount(board,color) - self.GetStableDiscsCount(board,oppositeColor)) * board.Size * 2 / 3
            return mobility + stability
    
    def GetPossibleConvertions(self,board,color,possibleMoves):
        result = 0
        for move in possibleMoves:
            newBoard = board.Clone()
            columnIndex = move[1]
            rowIndex = move[0]
            newBoard.SetFieldColor(rowIndex, columnIndex, color)
            result += newBoard.mInvertedDiscsLastMove
        return result

    def GetStableDiscsCount(self,board,color):
        pCa = self.GetStableDiscsFromCorner(board, color, 0, 0)
        pCb = self.GetStableDiscsFromCorner(board, color, 0, board.Size - 1)
        pCc = self.GetStableDiscsFromCorner(board, color, board.Size - 1, 0)
        pCd = self.GetStableDiscsFromCorner(board, color, board.Size - 1, board.Size - 1)
        pCe = self.GetStableDiscsFromEdge(board, color, 0, False)
        pCf = self.GetStableDiscsFromEdge(board, color, board.Size - 1, False)
        pCg = self.GetStableDiscsFromEdge(board, color, 0, True)
        pCh = self.GetStableDiscsFromEdge(board, color, board.Size - 1, True)
        return pCa  + pCb +pCc + pCd + pCe + pCf + pCg + pCh
    
    def GetStableDiscsFromCorner(self,board,color,cornerRowIndex,cornerColumnIndex):
        result = 0
        rowIndexChange =  1 if cornerRowIndex == 0 else -1
        columnIndexChange = 1 if cornerColumnIndex == 0 else -1

        rowIndex = cornerRowIndex
        rowIndexLimit =  board.Size if cornerRowIndex == 0 else 0
        columnIndexLimit = board.Size if cornerColumnIndex == 0 else 0
        rowIndex = cornerRowIndex
        while rowIndex != rowIndexLimit:
            columnIndex = cornerColumnIndex
            while columnIndex != columnIndexLimit:
                if board[rowIndex][columnIndex] == color:
                    result = result +1
                else:
                    break
                columnIndex += columnIndexChange
            
            if (columnIndexChange > 0 and columnIndex < board.Size ) or (columnIndexChange < 0 and columnIndex > 0):
                columnIndexLimit = columnIndex - columnIndexChange
                if columnIndexChange > 0 and columnIndexLimit == 0:
                    columnIndexLimit = columnIndexLimit +1
                elif columnIndexChange < 0 and columnIndexLimit == board.Size - 1:
                    columnIndexLimit = columnIndexLimit -1
                if (columnIndexChange > 0 and columnIndexLimit < 0) or (columnIndexChange < 0 and columnIndexLimit > board.Size - 1):
                    break
            rowIndex += rowIndexChange
        return result

    def GetStableDiscsFromEdge(self,board,color,edgeCoordinate,isHorizontal):
        result = 0
        if self.IsEdgeFull(board, edgeCoordinate, isHorizontal):
            oppositeColorDiscsPassed = False
            for otherCoordinate in range(board.Size):
                fieldColor = board[edgeCoordinate][otherCoordinate] if isHorizontal else board[otherCoordinate][edgeCoordinate]
                if fieldColor != color:
                    oppositeColorDiscsPassed = True
                elif oppositeColorDiscsPassed:
                    consecutiveDiscsCount = 0
                    while otherCoordinate < board.Size and fieldColor == color:
                        consecutiveDiscsCount = consecutiveDiscsCount +1
                        otherCoordinate = otherCoordinate +1
                        if otherCoordinate < board.Size:
                            fieldColor = board[edgeCoordinate][otherCoordinate] if isHorizontal else board[otherCoordinate][edgeCoordinate]
                    if otherCoordinate != board.Size:
                        result += consecutiveDiscsCount
                        oppositeColorDiscsPassed = True
        return result           

    def IsEdgeFull(self,board,edgeCoordinate,isHorizontal):
        for otherCoordinate in range(board.Size):
            if (isHorizontal and board[edgeCoordinate][ otherCoordinate] == None) or (not isHorizontal and board[otherCoordinate][ edgeCoordinate] == None):
                return False
        return True

