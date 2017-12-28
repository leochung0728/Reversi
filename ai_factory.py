from ai_algorithm import Algorithm_1

WHITE_TILE = 'WHITE_TILE'
BLACK_TILE = 'BLACK_TILE'
EMPTY_SPACE = 'EMPTY_SPACE'
HINT_TILE = 'HINT_TILE'


class AlgorithmFactory(object):
    # 建構子
    def __init__(self, pFunc, pUserTitle, pPossibleMoves, pBoard):
        self.position = None
        if pUserTitle == BLACK_TILE:
            pUserTitle = 1
        else:
            pUserTitle = 0
        pBoard = self.getBoardArray(pBoard)
        if pFunc == 0:
            self.position = Algorithm_1(pUserTitle, pPossibleMoves, pBoard).getPosition()
        else:
            self.position = Algorithm_1(pUserTitle, pPossibleMoves, pBoard).getPosition()

    # 取得位置
    def getPosition(self):
        return self.position

    # 取得棋盤array陣列 0:白棋 1:黑棋
    @staticmethod
    def getBoardArray(pBoard):
        for x in range(8):
            for y in range(8):
                if not pBoard[x][y] == EMPTY_SPACE:
                    if pBoard[x][y] == BLACK_TILE:
                        pBoard[x][y] = 1
                    else:
                        pBoard[x][y] = 0
        return pBoard
