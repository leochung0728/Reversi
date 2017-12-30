import random
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
            bestMove2 = self.checkOtherPlayerSource([x,y])
            diff.append((x, y,bestMove2-bestMove1))
        diff = sorted(diff, key=lambda x: x[2])
        better = diff[0]
        return [better[0],better[1]]
    #檢查對方的分數
    def checkOtherPlayerSource(self,pBestMove):
        otherTile = self.tile
        if self.tile == 1:
            otherTile = 0
        pinBoard = self.board
        pinBoard[pBestMove[0]][pBestMove[1]] = self.tile
        Moves = getValidMoves(pinBoard, otherTile)
        return self.getBestScore(Moves)
    #計算獲得分數
    def getBestScore(self,pPossibleMoves):
        nowScore = -99
        for x, y in pPossibleMoves:
            source = source_csv[source_csv.columns[x]][y]
            if source > nowScore:
                nowScore = source
                BestScore = [x,y,source]
        return nowScore
        
        