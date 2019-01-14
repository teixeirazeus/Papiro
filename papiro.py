#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  papiro.py
#  
#  Copyright 2019 Thiago da Silva Teixeira <teixeira.zeus@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
# import sys, os
import curses

def smartCursor(lineNow, code, atual, cursor_x, lineIndex):
    # Colagem de cursor no final do codigo
    if lineIndex == atual:  # final da string
        goline = len(code[lineNow])
        dif = abs(atual - goline)
        if dif == 0:
            return cursor_x, lineIndex
        elif atual > goline:
            cursor_x -= dif
            lineIndex -= dif
        elif atual < goline:
            cursor_x += dif
            lineIndex += dif

    return cursor_x, lineIndex


def draw_menu(stdscr):
    # code = list(string.ascii_letters)
    code = ['filename', 'Este e um texto', 'para testar o editor']
    lenCode = len(code) - 1  # menos o titulo

    # Configurações
    tabSize = 4


    # Mapeamento do codigo
    lineNow = 1
    lineIndex = 0
    scroll = 0

    # Mapeamento do editor
    k = 0  # Botão pressionado
    # Coordenadas do cursor
    cursor_x = 1
    cursor_y = 1

    # Limpa tela
    stdscr.clear()
    stdscr.refresh()

    # Inicialização de cores
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # Loop principal
    while k != ord('q'):

        # Inicialização
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        lenbar = len(str(lenCode))

		# Begin Analise de tecla
        # Movimento do cursor
        if k == curses.KEY_DOWN:
            if lineNow < lenCode:
                cursor_y += 1
                lineNow += 1

                atual = len(code[lineNow - 1])
                cursor_x, lineIndex = smartCursor(lineNow, code, atual, cursor_x, lineIndex)

        elif k == curses.KEY_UP:
            if lineNow != 1:
                cursor_y -= 1
                lineNow -= 1

                atual = len(code[lineNow + 1])
                cursor_x, lineIndex = smartCursor(lineNow, code, atual, cursor_x, lineIndex)

        elif k == curses.KEY_RIGHT:
            if lineIndex < len(code[lineNow]):
                cursor_x += 1
                lineIndex += 1

        elif k == curses.KEY_LEFT:
            if lineIndex != 0:
                cursor_x -= 1
                lineIndex -= 1

        # Ações
        # Enter
        elif k == 10:
            p1 = code[:lineNow]  # antes

            # corte da linha
            new1 = code[lineNow][:lineIndex]
            new2 = code[lineNow][lineIndex:]

            # depois sem a linha
            p2 = code[lineNow + 1:]
            code = p1 + [new1, new2] + p2

            # Movimentos
            cursor_x = 0
            lineIndex = 0

            lenCode += 1

            cursor_y += 1
            lineNow += 1

        # Backspace
        elif k == 263:
            if lineIndex != 0:
                code[lineNow] = code[lineNow][:lineIndex - 1] + code[lineNow][lineIndex:]
                cursor_x -= 1
                lineIndex -= 1
            elif lineNow > 1:
                cursor_y -= 1
                lineNow -= 1
                lineIndex = len(code[lineNow])
                cursor_x += lineIndex

                code[lineNow] += code[lineNow+1]
                code = code[:lineNow] + code[lineNow:]
                lenCode -= 1

        # Tab
        elif k == 9:
            code[lineNow] = code[lineNow][:lineIndex] + ' '*tabSize + code[lineNow][lineIndex:]
            cursor_x = cursor_x + tabSize
            lineIndex += tabSize

        # Digitos ascii
        elif k >= 32 and k <= 126:
            code[lineNow] = code[lineNow][:lineIndex]+chr(k)+code[lineNow][lineIndex:]
            cursor_x = cursor_x + 1
            lineIndex += 1

		# End Analise de tecla

        # Scroll
        if cursor_y > height - 2:
            if scroll + height - 2 < lenCode:
                scroll += 1
        elif cursor_y < 1:
            if scroll > 0:
                scroll -= 1

        # Limites do cursor
        cursor_x = max(lenbar + 2, cursor_x)
        cursor_x = min(width - 1, cursor_x)

        cursor_y = max(1, cursor_y)
        cursor_y = min(height - 2, cursor_y)

        # Barra lateral

        for i in range(1, height - 1):
            if i > lenCode: break
            number = str(i + scroll)
            stdscr.addstr(i, 0, ' ' + ' ' * (lenbar - len(number)) + number + ' ', curses.color_pair(4))

        # Imprimir codigo
        l = scroll + 1
        for i in range(1, height - 1):
            if i > lenCode: break
            stdscr.addstr(i, lenbar + 2, code[l], curses.color_pair(0))
            l += 1

        # Strings
        keystr = "Last key pressed: {}".format(k)[:width - 1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {} | Debug: {} ".format(cursor_x, cursor_y, lineNow)

        if k == 0:
            keystr = "No key press detected..."[:width - 1]

        # Centering calculations
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        # Barra superior
        stdscr.addstr(0, 0, ' '*width, curses.color_pair(3))
        stdscr.addstr(0, 0, code[0], curses.color_pair(3))
        stdscr.addstr(0, int((width // 2)) - len("PAPIRO"), "PAPIRO", curses.color_pair(3))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height - 1, 0, statusbarstr)
        stdscr.addstr(height - 1, len(statusbarstr), " " * (width - len(statusbarstr) -1))
        stdscr.attroff(curses.color_pair(3))

        # Turning on attributes for title
        stdscr.attron(curses.color_pair(2))
        stdscr.attron(curses.A_BOLD)

        # Turning off attributes for title
        stdscr.attroff(curses.color_pair(2))
        stdscr.attroff(curses.A_BOLD)

        # Print rest of text
        stdscr.addstr(start_y + 3, (width // 2) - 2, '-' * 4)
        stdscr.addstr(start_y + 5, start_x_keystr, keystr)
        stdscr.move(cursor_y, cursor_x)

        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()


def main():
    curses.wrapper(draw_menu)


if __name__ == "__main__":
    main()
