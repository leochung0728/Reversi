WHITE_TILE = 'WHITE_TILE'
BLACK_TILE = 'BLACK_TILE'
EMPTY_SPACE = 'EMPTY_SPACE'
HINT_TILE = 'HINT_TILE'


class AlgorithmFactory(object):

    def __init__(self, board, tile, useMethod):
        self.board = self.getBoardArray(board)
        self.tile = 1 if tile == BLACK_TILE else 0
        self.useMethod = useMethod

    def getBestMove(self):
        ai_method = self.useMethod(self.board, self.tile)
        return ai_method.getBestMove()

    @staticmethod
    def getBoardArray(board):  # get board array. 0 => white, 1 => black, else => None
        for x in range(8):
            for y in range(8):
                if board[x][y] == BLACK_TILE:
                    board[x][y] = 1
                elif board[x][y] == WHITE_TILE:
                    board[x][y] = 0
                else:
                    board[x][y] = None
        return board
