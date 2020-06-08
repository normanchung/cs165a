import numpy
import sys
import argparse
import cProfile
import itertools
import logging
import math
import multiprocessing
from random import randrange
import re
import signal
import time


def boardinitialize():
    size = 11
    lightchoice = False
    self = {1: 'dark', 'dark':1, 'lightchosen': False}
    for i in range(1,len(sys.argv)):
        if(sys.argv[i] == "-n"):
            if((int(sys.argv[i+1]) < 5) or (int(sys.argv[i+1])) > 26):
                print("Not a valid board size")
                exit(1)
            else:
                size = int(sys.argv[i+1])
        if(sys.argv[i] == "-l"):
            self = {2: 'light', 'light': 2, 'lightchosen': True}
            lightchoice = True
    boardlist = [ [0] * size for i in range(size) ]
    board = numpy.array(list(boardlist))
    print(board)
    if(lightchoice):
        lightp = self
        darkp = {1: 'dark', 'dark': 1, 'lightchosen': False}
    else:
        darkp = self
        lightp = {2: 'light', 'light': 2, 'lightchosen': True}
    return board, lightp, darkp, size, lightchoice


def movepiece(board, players):
    if(players['lightchosen']):
        currentmax = players['light']
        currentmin = allplayers['dark']
        minimizer = darkp
        player = lightp
    else:
        currentmax = players['dark']
        currentmin = allplayers['light']
        minimizer = lightp
        player = darkp

    m = size//2
    if(board[m][m] == 0):
        movechosenis = [m, m]
    else:
        cProfile.runctx('minimax(board, player, 0, True, -99999, 99999)', globals(), locals())
        score, movechosenis = minimax(board, player, 0, True, -99999, 99999)

    if(players['lightchosen']):
        board[movechosenis[0]][movechosenis[1]] = players['light']
    else:
        board[movechosenis[0]][movechosenis[1]] = players['dark']
    print("Move played:", piecemoving)
    print("Move played: %s%d" % (chr(movechosenis[1]+97), (movechosenis[0]+1)))
    print(board)
    winner = checkingwinner(board, allplayers)
    if(winner == 'tie'):
        print("It's a tie!")
        return False
    elif(winner != ''):
        print("%s wins!" % (winner))
        return False
    return True


def checkingifequal(list):
    list = iter(list)
    try:
        first = next(list)
    except StopIteration:
        return True
    return all(first == remaininglist for remaininglist in list)


def checkingwinner(board, players):
    winner = ''

    i = (size - 1) * -1
    while(i != size):
        diag = numpy.diagonal(board, i)
        if(len(diag) == 5):
            if(0 not in diag and checkingifequal(diag)):
                return players[diag[0]]
        if(len(diag) > 5):
            rang = len(diag) - 5
            j = 0
            while(j <= rang):
                if(0 not in diag[j:j+5] and checkingifequal(diag[j:j+5])):
                    return players[diag[j]]
                j += 1
        i += 1

    temp = numpy.fliplr(board)
    i = (size - 1) * -1
    while(i != size):
        diag = numpy.diagonal(temp, i)
        if(len(diag) == 5):
            if(0 not in diag and checkingifequal(diag)):
                return players[diag[0]]
        if(len(diag) > 5):
            rang = len(diag) - 5
            j = 0
            while(j <= rang):
                if(0 not in diag[j:j+5] and checkingifequal(diag[j:j+5])):
                    return players[diag[j]]
                j += 1
        i += 1
    rang = size - 5

    for i in range(size):
        j = 0
        while(j <= rang):
            horizontal = board[i, j:j+5]
            if(0 not in horizontal):
                if(checkingifequal(horizontal)):
                    return players[horizontal[0]]
            j += 1

    for i in range(size):
        j = 0
        while(j <= rang):
            vertical = board[j:j+5, i]
            if(0 not in vertical):
                if(checkingifequal(vertical)):
                    return players[vertical[0]]
            j += 1

    if(numpy.count_nonzero(board) == numpy.square(size)):
        return 'tie'
    return winner


def checkingscore(arr, ai, opponent):
    score = 0
    newarr = ' '.join(map(str, arr)).replace(' ','')
    a = str(ai)
    o = str(opponent)
    e = str(0)

    scores = {0: math.inf, 1: 1000, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 50, 8: 5, 9: 5, 10: 2, 11: 2, 12: 2, 13: 2}

    aipossiblemoves = [a+a+a+a+a+"", e+a+a+a+a+e+"", a+a+a+a+e+"", e+a+a+a+a+"", a+a+a+e+a+"", a+a+e+a+a+"",
                 a+e+a+a+a+"", e+a+a+a+e+"", a+a+a+e+"", e+a+a+a+"", e+a+e+a+e+"", e+a+a+e+"", e+a+a+"", a+a+e+""]
    opponentpossiblemoves = [o+o+o+o+o+"", e+o+o+o+o+e+"", o+o+o+o+e+"", e+o+o+o+o+"", o+o+o+e+o+"", o+o+e+o+o+"",
                 o+e+o+o+o+"", e+o+o+o+e+"", o+o+o+e+"", e+o+o+o+"", e+o+e+o+e+"", e+o+o+e+"", e+o+o+"", o+o+e+""]
    for i, move in enumerate(aipossiblemoves):
        if(move in newarr):
            score += scores[i]
            break
    for i, move in enumerate(opponentpossiblemoves):
        if(move in newarr):
            score -= scores[i]
            break
    return score


def diagonal(m, x, y):
    row = max((y - x, 0))
    col = max((x - y, 0))
    for i in range(min((len(m), len(m[0]))) - max((row, col))):
        yield m[row + i][col + i]


def evalhuer(board, players, aiplayer, possmove):
    score = 0
    if(aiplayer == lightp):
        ai = 2
        opponent = 1
    else:
        ai = 1
        opponent = 2

    for i in range(size):
        for j in range(size):
            if ((i,j) in possmove):
                horizontal = board[i, :]
                vertical = board[:, j]
                leftdiag = list(diagonal(board, j+1, i+1))
                temp = numpy.fliplr(board)
                rightdiag = list(diagonal(temp, j+1, i+1))
                leftdiag = numpy.asarray(leftdiag)
                rightdiag = numpy.asarray(rightdiag)
                score += checkingscore(horizontal, ai, opponent)
                score += checkingscore(vertical, ai, opponent)
                score += checkingscore(leftdiag, ai, opponent)
                score += checkingscore(rightdiag, ai, opponent)
    return score


neighbs = lambda x, y : [(x1, y1) for x1 in range(x-1, x+2)
                               for y1 in range(y-1, y+2)
                               if (-1 < x <= size and
                                   -1 < y <= size and
                                   (x != x1 or y != y1) and
                                   (0 <= x1 <= size) and
                                   (0 <= y1 <= size))]


def minimax(board, players, depth, findingmax, alpha, beta):
    possmovearr = []
    if(players['lightchosen']):
        currentmax = players['light']
        currentmin = allplayers['dark']
        minimizer = darkp
        player = lightp
    else:
        currentmax = players['dark']
        currentmin = allplayers['light']
        player = darkp
        minimizer = lightp

    currneighbs = []
    emptyspace = []
    for i in range(size):
        for j in range(size):
            if((board[i][j] == currentmax) or (board[i][j] == currentmin)):
                currneighbs += (neighbs(i, j))
            if(board[i][j] == 0):
                emptyspace.append((i,j))
    currneighbs = set(currneighbs)
    emptyspace = set(emptyspace)
    if(len(emptyspace) > len(currneighbs)):
        possmove = currneighbs
    else:
        possmove = emptyspace
    if(depth == 2):
        return evalhuer(board, allplayers, player, possmove)
    if(findingmax):
        best = -math.inf
        for i in range(size):
            for j in range(size):
                if((i,j) in possmove):
                    if(board[i][j] == 0):
                        board[i][j] = currentmax
                        score = minimax(board, minimizer, depth+1, False, alpha, beta)
                        board[i][j] = 0
                        if(score > best):
                            possmovearr = [i,j]
                        best = max(best, score)
                        alpha = max(alpha, best)
                        if alpha >= beta:
                            break
        return best, possmovearr
    else:
        best = math.inf
        for i in range(size):
            for j in range(size):
                if((i,j) in possmove):
                    if(board[i][j] == 0):
                        board[i][j] = currentmax
                        temp = [i,j]
                        score = minimax(board, minimizer, depth+1, True, alpha, beta)
                        board[i][j] = 0
                        best = min(best, score)
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
        return best


board, lightp, darkp, size, lightchoice = boardinitialize()
game = True
allplayers = {1: 'dark', 'dark': 1, 2: 'light', 'light': 2}

goingsecond = lightchoice
piecemoving = ''





while(game):
    if(goingsecond):
        if(lightchoice):
            movepiece(board, darkp)
        else:
            movepiece(board, lightp)
        goingsecond = False
    else:
        val = input("What's your move? ")
        val = val.lower()
        colp, rowp = re.findall(r'(\w+?)(\d+)', val)[0]
        colp = int(ord(colp)-96)
        rowp = int(rowp)

        if((colp > size) or (rowp > size) or (board[rowp-1][colp-1] != 0)):
            print("Invalid move. Try again!")
            invalid = True
        else:
            if(lightchoice):
                board[rowp-1][colp-1] = lightp['light']
            else:
                board[rowp-1][colp-1] = darkp['dark']
            invalid = False
            piecemoving = val
            print(board)
        if(invalid == False):
            winner = checkingwinner(board, allplayers)
            if(winner == 'tie'):
                print("It's a tie!")
                game = False
            elif(winner != ''):
                print("%s wins!" % (winner))
                game = False
            else:
                if(lightchoice):
                    game = movepiece(board, darkp)
                else:
                    game = movepiece(board, lightp)


#if __name__ == '__main__':
#    main()
