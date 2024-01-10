def solveSudoku(self, board):
    rows = [[] for i in range(9)]
    columns = [[] for i in range(9)]
    squares = [[] for i in range(9)]
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                columns[j].append(board[i][j])
                rows[i].append(board[i][j])
                squares[j//3 + (i//3)*3].append(board[i][j])
    def help(row,column):
        if row == 9:
            return True
        if column == 9:
            return help(row+1,0)
        if board[row][column] != '.':
            return help(row,column+1)
        for i in range(1,10):
            h = str(i)
            if not h in rows[row] and not h in columns[column] and not h in squares[column//3 + (row//3)*3]:
                board[row][column] = h
                rows[row].append(h)
                columns[column].append(h)
                squares[column//3 + (row//3)*3].append(h)
                if help(row,column+1):
                    return True
                rows[row].remove(h)
                columns[column].remove(h)
                squares[column//3 + (row//3)*3].remove(h)
            board[row][column] = '.'
        
        return False
    help(0,0)
    return board
