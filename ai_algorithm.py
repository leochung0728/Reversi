import random


class Algorithm_1(object):
    # 建構子
    def __init__(self, pUserTitle, pPossibleMoves, pBoard):
        self.mainboard = pBoard  # 複製後的棋盤位置
        self.possibleMoves = pPossibleMoves  # 合法位置
        self.userTitle = pUserTitle  # 執行玩家
        self.position = self.getBestMove()

    # 取得位置
    def getPosition(self):
        return self.position

    # 是否在角上
    @staticmethod
    def isOnCorner(x, y):
        return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)

    # 獲取棋盤上雙方的棋子數
    @staticmethod
    def getScoreOfBoard(board):
        xscore = 0
        oscore = 0
        for x in range(8):
            for y in range(8):
                if board[x][y] == 1:
                    xscore += 1
                if board[x][y] == 0:
                    oscore += 1
        return {1: xscore, 0: oscore}

    # 是否為合法走法
    def isValidMove(self, board, tile, xstart, ystart):
        # 檢查該位置是否出界或已有棋子
        if not self.isOnBoard(xstart, ystart) or board[xstart][ystart] is not None:
            return False

        # 臨時將tile放到指定的位置
        board[xstart][ystart] = tile

        if tile == 1:
            otherTile = 0
        else:
            otherTile = 1

        # 要被翻轉的棋子
        tilesToFlip = []
        for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = xstart, ystart
            x += xdirection
            y += ydirection
            # 前進方向第一格是 合法範圍 且 是對方的棋子
            if self.isOnBoard(x, y) and board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not self.isOnBoard(x, y):
                    continue
                # 一直走到出界或是不是對方棋子
                while board[x][y] == otherTile:
                    x += xdirection
                    y += ydirection
                    if not self.isOnBoard(x, y):
                        break
                # 出界了，則没有棋子要翻轉
                if not self.isOnBoard(x, y):
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
    @staticmethod
    def isOnBoard(x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    # 將一個tile棋子放到(xstart, ystart)
    def makeMove(self, board, tile, xstart, ystart):
        tilesToFlip = self.isValidMove(board, tile, xstart, ystart)

        if not tilesToFlip:
            return False

        board[xstart][ystart] = tile
        for x, y in tilesToFlip:
            board[x][y] = tile
        return True

    # 主程式
    def getBestMove(self):
        # 打亂順序
        random.shuffle(self.possibleMoves)
        # [x, y]在角上，則優先走
        for x, y in self.possibleMoves:
            if self.isOnCorner(x, y):
                return [x, y]
        # 預設最低分數
        bestScore = -1
        for x, y in self.possibleMoves:
            dupeBoard = self.mainboard
            self.makeMove(dupeBoard, self.userTitle, x, y)
            # 按照分數選擇走法，優先選擇翻轉後分數最多的走法
            score = self.getScoreOfBoard(dupeBoard)[self.userTitle]
            if score > bestScore:
                bestMove = [x, y]
                bestScore = score
        return bestMove
