def isOnCorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


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


def getValidMoves(board, tile):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y):
                validMoves.append((x, y))
    return validMoves


def isValidMove(board, tile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] is not None:
        return False

    board[xstart][ystart] = tile

    if tile == 1:
        otherTile = 0
    else:
        otherTile = 1

    tilesToFlip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection

        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue

            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break

            if not isOnBoard(x, y):
                continue

            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection

                    if x == xstart and y == ystart:
                        break

                    tilesToFlip.append([x, y])

    board[xstart][ystart] = None

    if len(tilesToFlip) == 0:
        return False

    return tilesToFlip


def isOnBoard(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


def makeMove(board, tile, xstart, ystart):
    tilesToFlip = isValidMove(board, tile, xstart, ystart)

    if not tilesToFlip:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToFlip:
        board[x][y] = tile
    return True
