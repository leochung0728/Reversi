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
