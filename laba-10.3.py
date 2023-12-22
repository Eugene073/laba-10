import random
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy

sign = 0

global board
board = [[" " for x in range(3)] for y in range(3)]

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def close_gameboard(game_board):
    game_board.destroy()
    global board, sign
    board = [[" " for x in range(3)] for y in range(3)]
    sign = 0
    play()

def close_game():
    if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти из игры?"):
        menu.destroy()

def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))


def get_text(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    if winner(board, "X"):
        box = messagebox.showinfo("Крестики нолики", "Игрок №1 победил")
        close_gameboard(gb)
    elif winner(board, "O"):
        box = messagebox.showinfo("Крестики нолики", "Игрок №2 победил")
        close_gameboard(gb)
    elif (isfull()):
        box = messagebox.showinfo("Крестики нолики", "Ничья")
        close_gameboard(gb)


def isfree(i, j):
    return board[i][j] == " "


def isfull():
    flag = True
    for i in board:
        if (i.count(' ') > 0):
            flag = False
    return flag


def gameboard_pl(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


def pc():
    possiblemove = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                possiblemove.append([i, j])
    move = []
    if possiblemove == []:
        return
    else:
        for let in ['O', 'X']:
            for i in possiblemove:
                boardcopy = deepcopy(board)
                boardcopy[i[0]][i[1]] = let
                if winner(boardcopy, let):
                    return i
        corner = []
        for i in possiblemove:
            if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corner.append(i)
        if len(corner) > 0:
            move = random.randint(0, len(corner) - 1)
            return corner[move]
        edge = []
        for i in possiblemove:
            if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edge.append(i)
        if len(edge) > 0:
            move = random.randint(0, len(edge) - 1)
            return edge[move]


def get_text_pc(i, j, gb, l1, l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    x = True
    if winner(board, "X"):
        x = False
        box = messagebox.showinfo("Крестики нолики", "Вы победили!")
        close_gameboard(gb)
    elif winner(board, "O"):
        x = False
        box = messagebox.showinfo("Крестики нолики", "Вы проиграли!")
        close_gameboard(gb)
    elif (isfull()):
        x = False
        box = messagebox.showinfo("Крестики нолики", "Ничья!")
        close_gameboard(gb)
    if (x):
        if sign % 2 != 0:
            move = pc()
            button[move[0]][move[1]].config(state=DISABLED)
            get_text_pc(move[0], move[1], gb, l1, l2)

def gameboard_pc(game_board, l1, l2):
    global button
    button = []
    for i in range(3):
        m = 3 + i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text_pc, i, j, game_board, l1, l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()


def withpc(game_board):
    game_board.destroy()
    game_board = Tk()
    window_width = 237
    window_height = 285
    center_window(game_board, window_width, window_height)
    game_board.title("Крестики нолики")
    l1 = Button(game_board, text="Игрок : X", width=12)
    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Компьютер : O",
                width=12, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pc(game_board, l1, l2)


def withplayer(game_board):
    game_board.destroy()
    game_board = Tk()
    window_width = 225
    window_height = 285
    center_window(game_board, window_width, window_height)
    game_board.title("Крестики нолики")
    l1 = Button(game_board, text="Игрок №1 : X", width=10)

    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Игрок №2 : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pl(game_board, l1, l2)


def play():
    global menu
    menu = Tk()
    window_width = 250
    window_height = 112
    center_window(menu, window_width, window_height)
    menu.title("Крестики нолики")
    wpc = partial(withpc, menu)
    wpl = partial(withplayer, menu)

    # Установка обработчика закрытия окна
    menu.protocol("WM_DELETE_WINDOW", close_game)

    B1 = Button(menu, text="Одиночная игра", command=wpc,
                activeforeground='gray',
                activebackground="white", bg="gray",
                fg="white", width=500, font='summer', bd=5)

    B2 = Button(menu, text="Игра на двоих", command=wpl, activeforeground='gray',
                activebackground="white", bg="gray", fg="white",
                width=500, font='summer', bd=5)

    B3 = Button(menu, text="Выход", command=close_game, activeforeground='gray',
                activebackground="white", bg="gray", fg="white",
                width=500, font='summer', bd=5)

    B1.pack(side='top')
    B2.pack(side='top')
    B3.pack(side='top')
    menu.mainloop()


play()