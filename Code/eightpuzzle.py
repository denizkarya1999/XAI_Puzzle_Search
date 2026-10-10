# eightpuzzle.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import argparse
import ast
import re
import sys

import search
from demonstrations import show_demonstrations
from About import show_about
from screen import clear_screen
from puzzle import EightPuzzleState


# Starting puzzle arrangement. The starter class uses 0 for the blank.
initial_puzzle = EightPuzzleState([0, 2, 3,
                                  1, 4, 5,
                                  8, 7, 6])

# Target puzzle arrangement from the assignment.
goal_puzzle = EightPuzzleState([1, 2, 3,
                               8, 0, 4,
                               7, 6, 5])


class EightPuzzleSearchProblem(search.SearchProblem):
    """
      Implementation of a SearchProblem for the  Eight Puzzle domain

      Each state is represented by an instance of an eightPuzzle.
    """
    def __init__(self, puzzle, goal=None):
        "Creates a new EightPuzzleSearchProblem which stores search information."
        self.puzzle = puzzle
        self.goal = goal if goal is not None else goal_puzzle

    # Return the starting puzzle stored in this search problem.
    def getStartState(self):
        return self.puzzle

    def isGoalState(self,state):
        return state == self.goal

    def getSuccessors(self,state):
        """
          Returns list of (successor, action, stepCost) pairs where
          each succesor is either left, right, up, or down
          from the original state and the cost is 1.0 for each
        """
        succ = []
        for a in state.legalMoves():
            succ.append((state.result(a), a, 1))
        return succ

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)

# <DKA - October 9th 2026> show_search_menu
# Description: Let the user select a search algorithm.
# Input: No arguments; the user enters menu choices.
# Output: Printed search results; returns None.
def show_search_menu():
    search_options = {
        '1': ('BFS', 'Explore the shallowest states first.'),
        '2': ('DFS', 'Explore the deepest states first.'),
        '3': ('IDS', 'Repeat depth-limited searches with increasing limits.'),
        '4': ('UCS', 'Explore the state with the lowest path cost first.'),
        '5': ('GBS - misplaced tiles', 'Choose the fewest misplaced numbered tiles.'),
        '6': ('GBS - Manhattan distance', 'Choose the smallest total tile distance.'),
        '7': ('A* - misplaced tiles', 'Use path cost plus misplaced numbered tiles.'),
        '8': ('A* - Manhattan distance', 'Use path cost plus total tile distance.')
    }

    while True:
        clear_screen()
        print('\nSearch algorithms')
        for number, option in search_options.items():
            print(number + '. ' + option[0])
        print('0. Back to the main menu')

        choice = input('Type an option number and press Enter: ').strip()
        clear_screen()
        if choice == '0':
            return
        elif choice in ('1', '2', '3', '4', '5', '6', '7', '8'):
            # Ask before displaying search steps for any implemented algorithm.
            answer = input('Show each explored board and its actions? (y/N): ').strip().lower()
            clear_screen()
            show_steps = answer in ('y', 'yes')
            problem = EightPuzzleSearchProblem(initial_puzzle, goal_puzzle)
            algorithms = {
                '1': search.breadthFirstSearch,
                '2': search.depthFirstSearch,
                '3': search.iterativeDeepeningSearch,
                '4': search.uniformCostSearch,
                '5': search.greedyBestFirstSearch,
                '6': search.greedyBestFirstSearch,
                '7': search.aStarSearch,
                '8': search.aStarSearch,
            }
            if choice in ('6', '8'):
                algorithms[choice](problem, show_steps=show_steps, heuristic='manhattan')
            else:
                algorithms[choice](problem, show_steps=show_steps)
            input('Press Enter to return to the search menu...')
        else:
            print('Please choose a number from 0 to 8.')
            input('Press Enter to try again...')


# <DKA - October 9th 2026> parse_board
# Description: Read and validate a 3-by-3 board, using '-' or 0 for the blank.
# Input: A board written as a nested list in a command-line argument.
# Output: An EightPuzzleState, or an argument error for an invalid board.
def parse_board(text):
    # Replace an unquoted blank before safely reading the list.
    text = text.strip().strip('\"\'“”‘’')
    text = re.sub(r'(?<=[\[,])\s*-\s*(?=[,\]])', '0', text)
    try:
        board = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        raise argparse.ArgumentTypeError('Use a board such as [[-,2,3],[1,4,5],[8,7,6]].')

    if not isinstance(board, list) or len(board) != 3:
        raise argparse.ArgumentTypeError('The board must contain three rows.')
    tiles = []
    for row in board:
        if not isinstance(row, list) or len(row) != 3:
            raise argparse.ArgumentTypeError('Each board row must contain three tiles.')
        for tile in row:
            if tile == '-':
                tile = 0
            if type(tile) is not int:
                raise argparse.ArgumentTypeError('Tiles must be integers; use - or 0 for the blank.')
            tiles.append(tile)
    if sorted(tiles) != list(range(9)):
        raise argparse.ArgumentTypeError('Use each tile from 1 to 8 once and exactly one blank.')
    return EightPuzzleState(tiles)


# <DKA - October 9th 2026> run_from_command_line
# Description: Run one search or every slash-separated search and heuristic combination.
# Input: Search names, initial and goal boards, heuristics, and a display option.
# Output: Printed search summaries and separate results files; returns None.
def run_from_command_line():
    parser = argparse.ArgumentParser(description='XAI 8-Puzzle 1.0', prefix_chars='-–')
    parser.add_argument('--search', '–search', required=True,
                        help='BFS, DFS, IDS, UCS, GBS, A*, or Beam; separate multiple names with /.')
    parser.add_argument('--initial', '–initial', required=True, type=parse_board,
                        help='Initial 3-by-3 board; use - or 0 for the blank.')
    parser.add_argument('--goal', '–goal', required=True, type=parse_board,
                        help='Goal 3-by-3 board; use - or 0 for the blank.')
    parser.add_argument('--heuristic', '–heuristic', default='misplaced',
                        help='misplaced/manhattan; optional other is recognized but not implemented.')
    parser.add_argument('--show-steps', '–show-steps', action='store_true',
                        help='Display each explored board and its actions.')
    args = parser.parse_args()

    # Accept the curly quotes in the assignment's example as well as ordinary quotes.
    searches = args.search.strip().strip('\"\'“”‘’.').upper().split('/')
    heuristics = args.heuristic.strip().strip('\"\'“”‘’.').lower().split('/')
    searches = list(dict.fromkeys(name.strip() for name in searches))
    heuristics = list(dict.fromkeys(name.strip() for name in heuristics))
    algorithms = {
        'BFS': search.breadthFirstSearch,
        'DFS': search.depthFirstSearch,
        'IDS': search.iterativeDeepeningSearch,
        'UCS': search.uniformCostSearch,
        'GBS': search.greedyBestFirstSearch,
        'A*': search.aStarSearch,
    }
    if any(name not in algorithms and name != 'BEAM' for name in searches):
        parser.error('Search names must be BFS/DFS/IDS/UCS/GBS/A*/Beam (choose one or several).')
    if any(name not in ('misplaced', 'manhattan', 'other') for name in heuristics):
        parser.error('Heuristics must be misplaced/manhattan/other (choose one or several).')
    if 'other' in heuristics:
        print('The optional other heuristic is not implemented; skipping it.')
    heuristics = [name for name in heuristics if name != 'other']

    # Boards with different inversion parity cannot reach each other.
    parities = []
    for board in (args.initial, args.goal):
        tiles = [tile for row in board.cells for tile in row if tile != 0]
        inversions = sum(tiles[i] > tiles[j] for i in range(8) for j in range(i + 1, 8))
        parities.append(inversions % 2)
    if parities[0] != parities[1]:
        parser.error('The initial board cannot reach this goal board (different inversion parity).')

    # Uninformed searches run once; informed searches run once per heuristic.
    problem = EightPuzzleSearchProblem(args.initial, args.goal)
    for name in searches:
        if name == 'BEAM':
            print('Optional Beam search is not implemented; skipping it.')
        elif name in ('GBS', 'A*'):
            for heuristic in heuristics:
                print('\nSearch: ' + name + ' | Heuristic: ' + heuristic)
                algorithms[name](problem, show_steps=args.show_steps, heuristic=heuristic)
        else:
            print('\nSearch: ' + name)
            algorithms[name](problem, show_steps=args.show_steps)


# <DKA - October 9th 2026> main
# Description: Run the main menu using the global initial and goal puzzles.
# Input: No arguments; the user enters menu choices.
# Output: Printed menus and the selected demonstrations or search menu; returns None.
def main():
    # Let the user choose demonstrations, search algorithms, or program information.
    while True:
        clear_screen()
        print('\nXAI 8-Puzzle 1.0')
        print('1. Puzzle demonstrations')
        print('2. Search algorithms')
        print('3. About')
        print('0. Exit')

        try:
            choice = input('Type an option number and press Enter: ').strip()
            clear_screen()
            if choice == '1':
                show_demonstrations(initial_puzzle, goal_puzzle)
            elif choice == '2':
                show_search_menu()
            elif choice == '3':
                print()
                show_about()
                input('Press Enter to return to the main menu...')
            elif choice == '0':
                print('Goodbye!')
                return
            else:
                print('Please choose 0, 1, 2, or 3.')
                input('Press Enter to try again...')

        # Exit cleanly when input ends or the user presses Ctrl+C.
        except (EOFError, KeyboardInterrupt):
            print('\nGoodbye!')
            return


if __name__ == '__main__':
    if len(sys.argv) > 1:
        run_from_command_line()
    else:
        main()
