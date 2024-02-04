import multiprocessing
import time
def solveSudoku(board,qq):
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
            # for ii in board:
            #     print(ii)
            # print('\n')
            board[row][column] = '.'
        
        return False
    help(0,0)
    qq.put(board)
def isValidSudoku(board):
    rows,columns,squares = [[]for i in range(9)],[[]for i in range(9)],[[]for i in range(9)]
    for c,i in enumerate(board):
        for cc,j in enumerate(i):
            if j != '.':
                rows[c].append(j)
                columns[cc].append(j)
                squares[cc//3 + (c//3)*3].append(j)
    for c,i in enumerate(rows):        
        if len(set(rows[c])) != len(rows[c]):
            return False
        if len(set(columns[c])) != len(columns[c]):
            return False
        if len(set(squares[c])) != len(squares[c]):
            return False
    return True
def rand(b):
    nums = [str(i) for i in range(1,10)]
    nums2 = nums[:]
    coords2 = [8,3,5,6,4,7]
    for i in range(3):
        coords2.append(randint(3,8))

    for c,i in enumerate(b):
        r = randint(0,len(nums)-1)
        rand_num = randint(0,len(nums2)-1)
        cc = 0

        while nums2[rand_num] == nums[r] and cc<1000:
            rand_num = randint(0,len(nums2)-1)
            cc += 1

        b[c][0] = nums.pop(r)
        b[c][coords2.pop(randint(0,len(coords2)-1))] = nums2.pop(rand_num)
    return b
def solve(bb):
    if isValidSudoku(bb):
        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=solveSudoku, name="solveSudoku", args=(bb,q))
        p.start()
        p.join(3)
        p.terminate()
        p.join()
        bb = q.get()
    elif ''.join([''.join([i for i in ii if i == '.']) for ii in bd]):
        while ''.join([''.join([i for i in ii if i == '.']) for ii in bd]) or not isValidSudoku(bd):
            bd = [['.' for i in range(9)] for i in range(9)]
            bd = rand(bd)
            print('bruh')
            if isValidSudoku(bd):
                    q = multiprocessing.Queue()
                    p = multiprocessing.Process(target=solveSudoku, name="solveSudoku", args=(bd,q))
                    p.start()
                    p.join(3)
                    p.terminate()
                    p.join()
                    bd = q.get()
    return bb