import numpy as np
import sys
import re
import argparse
import math
import time
import signal
import multiprocessing
from random import randrange
import itertools
import multiprocessing, logging
import cProfile as profile


# argv[1] = -n, argv[2] = board size, argv[3] = -1 (player is light)
# python3 gobang.py -n size -1
# human player indicates move through command line <move> with <letter, col><number, row>
# 1 = black, 2 = white

def checkEqual(list):
    list = iter(list)
    try:
        first = next(list)
    except StopIteration:
        return True
    return all(first == restOfList for restOfList in list)

# shape[0] = row, shape[1] = col, board[0,:] prints first row, board[:,0] prints first col
#  checkWinner does not seem to affect the timing
def checkWinner(board, players):
    winner = ''

    # diagonal left check
    i = (size - 1) * -1
    while(i != size):
        diag = np.diagonal(board, i)
        if(len(diag) == 5):
            if(0 not in diag and checkEqual(diag)):
                return players[diag[0]]
        if(len(diag) > 5):
            ranger = len(diag) - 5
            j = 0
            while(j <= ranger):
                if(0 not in diag[j:j+5] and checkEqual(diag[j:j+5])):
                    return players[diag[j]]
                j += 1
        i += 1

    # diagonal right check
    tempBoard = np.fliplr(board)
    i = (size - 1) * -1
    while(i != size):
        diag = np.diagonal(tempBoard, i)
        if(len(diag) == 5):
            if(0 not in diag and checkEqual(diag)):
                return players[diag[0]]
        if(len(diag) > 5):
            ranger = len(diag) - 5
            j = 0
            while(j <= ranger):
                if(0 not in diag[j:j+5] and checkEqual(diag[j:j+5])):
                    return players[diag[j]]
                j += 1
        i += 1

    # horizontal check
    ranger = size - 5
    for i in range(size):
        j = 0
        while(j <= ranger):
            horz = board[i, j:j+5]
            if(0 not in horz):
                if(checkEqual(horz)):
                    return players[horz[0]]
            j += 1
    # vertical check
    for i in range(size):
        j = 0
        while(j <= ranger):
            vertz = board[j:j+5, i]
            if(0 not in vertz):
                if(checkEqual(vertz)):
                    return players[vertz[0]]
            j += 1
    # tie check
    if(np.count_nonzero(board) == np.square(size)):
        return 'tie'
    return winner


def diagonal(m, x, y):
    row = max((y - x, 0))
    col = max((x - y, 0))
    for i in range(min((len(m), len(m[0]))) - max((row, col))):
        yield m[row + i][col + i]





q = multiprocessing.Queue()


def checkScore(arr, ai, opp):
    score = 0
    # newarr = np.array2string(arr).replace(' ', '') # took ~4 seconds
    newarr = ' '.join(map(str, arr)).replace(' ','')
    a = str(ai)
    o = str(opp)
    z = str(0)

    scores = {0: math.inf, 1: 1000, 2: 100, 3: 100, 4: 100, 5: 100, 6: 100, 7: 50, 8: 5, 9: 5, 10: 2, 11: 2, 12: 2, 13: 2}

    ai_moves = [a+a+a+a+a+"", z+a+a+a+a+z+"", a+a+a+a+z+"", z+a+a+a+a+"", a+a+a+z+a+"", a+a+z+a+a+"",
                 a+z+a+a+a+"", z+a+a+a+z+"", a+a+a+z+"", z+a+a+a+"", z+a+z+a+z+"", z+a+a+z+"", z+a+a+"", a+a+z+""]
    opp_moves = [o+o+o+o+o+"", z+o+o+o+o+z+"", o+o+o+o+z+"", z+o+o+o+o+"", o+o+o+z+o+"", o+o+z+o+o+"",
                 o+z+o+o+o+"", z+o+o+o+z+"", o+o+o+z+"", z+o+o+o+"", z+o+z+o+z+"", z+o+o+z+"", z+o+o+"", o+o+z+""]
    # strang = ai + ai + ai + ai + ""
    for i, move in enumerate(ai_moves): # checking ai moves
        if(move in newarr):
            score += scores[i]
            break
    for i, move in enumerate(opp_moves): # checking opponent moves
        if(move in newarr):
            score -= scores[i]
            break
    # return_dict[score] = score
    # q.put(score)
    return score


# checks possibilities of player and opponent on current board
def evaluation(board, players, aiPlayer, pot_moves):
    r1 = 0
    r2 = 0
    r3 = 0
    r4 = 0
    score = 0
    if(aiPlayer == lightPlayer):
        ai = 2
        opp = 1
    else:
        ai = 1
        opp = 2

    for i in range(size):
        for j in range(size):
            if ((i,j) in pot_moves):
                horz = board[i, :]
                vertz = board[:, j]
                diagL = list(diagonal(board, j+1, i+1))
                tempboard = np.fliplr(board)
                diagR = list(diagonal(tempboard, j+1, i+1))
                diagL = np.asarray(diagL)
                diagR = np.asarray(diagR)

                # logger = multiprocessing.log_to_stderr()
                # logger.setLevel(multiprocessing.SUBDEBUG)

                # p1 = multiprocessing.Process(target=checkScore, args=(horz, ai, opp))
                # p2 = multiprocessing.Process(target=checkScore, args=(vertz, ai, opp))
                # p3 = multiprocessing.Process(target=checkScore, args=(diagL, ai, opp))
                # p4 = multiprocessing.Process(target=checkScore, args=(diagR, ai, opp))

                # p1.start()
                # p2.start()
                # p3.start()
                # p4.start()

                # r1 += q.get()
                # p1.join()
                # r2 += q.get()
                # p2.join()
                # r3 += q.get()
                # p3.join()
                # r4 += q.get()
                # p4.join()


                score += checkScore(horz, ai, opp)
                score += checkScore(vertz, ai, opp)
                score += checkScore(diagL, ai, opp)
                score += checkScore(diagR, ai, opp)


    return score

# gets the neighbors of selected element
neighbors = lambda x, y : [(x2, y2) for x2 in range(x-1, x+2)
                               for y2 in range(y-1, y+2)
                               if (-1 < x <= size and
                                   -1 < y <= size and
                                   (x != x2 or y != y2) and
                                   (0 <= x2 <= size) and
                                   (0 <= y2 <= size))]


def minimax(board, players, depth, is_maximizer, alpha, beta):
    # print(scores['opp'])
    move = []
    if(players['isLight']):
        max_marker = players['light']
        min_marker = allPlayers['dark']
        minimizer = darkPlayer
        player = lightPlayer
    else:
        max_marker = players['dark']
        min_marker = allPlayers['light']
        player = darkPlayer
        minimizer = lightPlayer

    # check for adjacent moves
    n = []
    empty_spots = []
    for i in range(size):
        for j in range(size):
            if((board[i][j] == max_marker) or (board[i][j] == min_marker)):
                n += (neighbors(i, j))
            if(board[i][j] == 0):
                empty_spots.append((i,j))
    n = set(n)
    empty_spots = set(empty_spots)
    if(len(empty_spots) > len(n)):
        pot_moves = n
    else:
        pot_moves = empty_spots
    if(depth == 2):
        # like tic tac toe example from lecture -
        return evaluation(board, allPlayers, player, pot_moves)
    if(is_maximizer):
        bestScore = -math.inf
        for i in range(size):
            for j in range(size):
                if((i,j) in pot_moves):
                    if(board[i][j] == 0):
                        board[i][j] = max_marker
                        score = minimax(board, minimizer, depth+1, False, alpha, beta)
                        board[i][j] = 0
                        # choosing the best move for 'light' player
                        if(score > bestScore):
                            move = [i,j]
                        bestScore = max(bestScore, score)
                        alpha = max(alpha, bestScore)
                        # Alpha-Beta Pruning
                        if alpha >= beta:
                            break
            print("Best Score", bestScore)
        return bestScore, move
    else:
        bestScore = math.inf
        for i in range(size):
            for j in range(size):
                if((i,j) in pot_moves):
                    if(board[i][j] == 0):
                        board[i][j] = max_marker
                        temp =[i,j]
                        score = minimax(board, minimizer, depth+1, True, alpha, beta)
                        board[i][j] = 0
                        # chooses the lowest score (aka best move for DARK player)
                        # print(score)
                        bestScore = min(bestScore, score)
                        beta = min(beta, bestScore)
                        # Alpha-Beta pruning
                        if beta <= alpha:
                            break
        return bestScore


def move(board, players):
    if(players['isLight']):
        max_marker = players['light']
        min_marker = allPlayers['dark']
        minimizer = darkPlayer
        player = lightPlayer
    else:
        max_marker = players['dark']
        min_marker = allPlayers['light']
        minimizer = lightPlayer
        player = darkPlayer

    # makes it pick the middle spot when game starts
    v = size//2
    # if(board[v][v] == 0 and players['isLight'] == False):
    if(board[v][v] == 0):
        chosenMove = [v, v]
    else:
        profile.runctx('minimax(board, player, 0, True, -99999, 99999)', globals(), locals())
        score, chosenMove = minimax(board, player, 0, True, -99999, 99999)

    if(players['isLight']):
        board[chosenMove[0]][chosenMove[1]] = players['light']
    else:
        board[chosenMove[0]][chosenMove[1]] = players['dark']
    print("Move played:", valueMoved)
    print("Move played: %s%d" % (chr(chosenMove[1]+97), (chosenMove[0]+1)))
    print(board)
    # CHANGED PLAYERS TO ALLPLAYERS
    winner = checkWinner(board, allPlayers)
    if(winner == 'tie'):
        print("It's a tie!")
        return False
    elif(winner != ''):
        print("%s wins!" % (winner))
        return False
    return True


def boardSetUp():
    # default parameters
    size = 11
    chosenLight = False
    me = {1: 'dark', 'dark':1, 'isLight': False}
    for i in range(1,len(sys.argv)):
        # checking if board size is specified or in bounds
        if(sys.argv[i] == "-n"):
            if((int(sys.argv[i+1]) < 5) or (int(sys.argv[i+1])) > 26):
                print("Not a valid board size")
                exit(1)
            else:
                size = int(sys.argv[i+1])
        # check if player chose "-l" they play LIGHT = 2
        if(sys.argv[i] == "-l"):
            me = {2: 'light', 'light': 2, 'isLight': True}
            chosenLight = True
    board_list = [ [0] * size for i in range(size) ]
    board = np.array(list(board_list))
    print(board)
    if(chosenLight):
        lightPlayer = me
        darkPlayer = {1: 'dark', 'dark': 1, 'isLight': False}
    else:
        darkPlayer = me
        lightPlayer = {2: 'light', 'light': 2, 'isLight': True}
    return board, lightPlayer, darkPlayer, size, chosenLight

board, lightPlayer, darkPlayer, size, chosenLight = boardSetUp()
game = True
allPlayers = {1: 'dark', 'dark': 1, 2: 'light', 'light': 2}

oppStarts = chosenLight
valueMoved = ''

# actual game
while(game):
    if(oppStarts):
        if(chosenLight):
            move(board, darkPlayer)
        else:
            move(board, lightPlayer)
        oppStarts = False
    else:
        val = input("What's your move? ")
        val = val.lower()
        #  might have to change this findall function to accept all answers
        player_col, player_row = re.findall(r'(\w+?)(\d+)', val)[0]
        player_col = int(ord(player_col)-96)
        player_row = int(player_row)

        if((player_col > size) or (player_row > size) or (board[player_row-1][player_col-1] != 0)):
            print("Invalid move. Try again!")
            invalid = True
        else:
            if(chosenLight):
                board[player_row-1][player_col-1] = lightPlayer['light']
            else:
                board[player_row-1][player_col-1] = darkPlayer['dark']
            invalid = False
            valueMoved = val
            print(board)
        # checks the state of the board
        if(invalid == False):
            winner = checkWinner(board, allPlayers)
            if(winner == 'tie'):
                print("It's a tie!")
                game = False
            elif(winner != ''):
                print("%s wins!" % (winner))
                game = False
            else:
                if(chosenLight):
                    game = move(board, darkPlayer)
                else:
                    game = move(board, lightPlayer)
