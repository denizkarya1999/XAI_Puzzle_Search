from screen import clear_screen


# <DKA - October 9th 2026> format_row
# Description: Format one puzzle row, showing the blank as '-'.
# Input: A row of tile numbers, where 0 is the blank.
# Output: A string with the tiles separated by spaces.
def format_row(row):
    display_tiles = []
    for tile in row:
        if tile == 0:
            display_tiles.append('-')
        else:
            display_tiles.append(str(tile))
    return ' '.join(display_tiles)


# <DKA - October 9th 2026> play_puzzle
# Description: Let the user make continuous moves until the goal is reached or they exit.
# Input: Initial and goal EightPuzzleState objects, plus user-entered directions.
# Output: Printed boards, legal moves, and move count; returns None.
def play_puzzle(initial_puzzle, goal_puzzle):
    # Start from the initial board and count only successful moves.
    current_puzzle = initial_puzzle
    move_count = 0

    while True:
        # Show the changing board beside the fixed target after every move.
        print('\nCurrent    | Target (fixed)')
        for row in range(3):
            print(format_row(current_puzzle.cells[row]), end='      | ')
            print(format_row(goal_puzzle.cells[row]))
        print('Moves made:', move_count)

        # Stop automatically as soon as the current board matches the target.
        if current_puzzle == goal_puzzle:
            print('Goal reached in', move_count, 'moves!')
            input('Press Enter to return to the demonstrations menu...')
            return

        # Read a direction, or let the user leave before reaching the goal.
        legal_moves = current_puzzle.legalMoves()
        print('Legal moves:', legal_moves)
        move = input('Type a move (UP/DOWN/LEFT/RIGHT), or 0 to return: ').strip().lower()
        clear_screen()
        if move == '0':
            return

        # Each legal move creates the board used by the next turn.
        if move in legal_moves:
            current_puzzle = current_puzzle.result(move)
            move_count += 1
        else:
            print('That move is not legal from the current board.')


# <DKA - October 9th 2026> show_goal_walkthrough
# Description: Show each example board in three rows and the actions taken as a list.
# Input: Initial and goal EightPuzzleState objects, plus Enter or 0 from the user.
# Output: Printed current boards and cumulative action lists; returns None.
def show_goal_walkthrough(initial_puzzle, goal_puzzle):
    # Use the verified solution for the example boards, rather than a search algorithm.
    moves = ['down', 'down', 'right', 'right', 'up', 'left']
    states = [initial_puzzle]

    # Check the entire example path before displaying it.
    for move in moves:
        if move not in states[-1].legalMoves():
            print('This walkthrough only supports the assignment\'s example boards.')
            return
        states.append(states[-1].result(move))
    if states[-1] != goal_puzzle:
        print('This walkthrough only supports the assignment\'s example boards.')
        return

    # Show the current board in three rows and the actions taken so far.
    for step in range(len(states)):
        clear_screen()
        print('\nCurrent board:')
        for row in states[step].cells:
            print(format_row(row))
        print('Actions taken:', moves[:step])

        # Wait before advancing, or let the user leave the walkthrough early.
        if step < len(moves):
            choice = input('Press Enter for the next state, or type 0 to return: ').strip()
            if choice == '0':
                return

    # Keep the final matching board visible before returning to the menu.
    input('\nGoal reached. Press Enter to return to the demonstrations menu...')


# <DKA - October 9th 2026> show_demonstrations
# Description: Let the user choose puzzle demonstrations or continuous moves.
# Input: Initial and goal EightPuzzleState objects, plus user choices.
# Output: Printed boards, goal checks, blank positions, and moves; returns None.
def show_demonstrations(initial_puzzle, goal_puzzle):
    while True:
        clear_screen()
        print('\nPuzzle Demonstrations')
        print('1. Show initial and goal boards')
        print('2. Check whether the initial board is the goal')
        print('3. Show the blank position')
        print('4. Show legal moves')
        print('5. Demonstrate one legal move')
        print('6. Make continuous moves until the goal')
        print('7. Show example boards and action lists')
        print('0. Back to the main menu')

        choice = input('Type an option number and press Enter: ').strip()
        clear_screen()

        # Show both boards side by side.
        if choice == '1':
            print('\nInitial    | Target (fixed)')
            for row in range(3):
                print(format_row(initial_puzzle.cells[row]), end='      | ')
                print(format_row(goal_puzzle.cells[row]))

        # Compare with the assignment's goal, rather than the template's default goal.
        elif choice == '2':
            print('Already at the goal?', initial_puzzle == goal_puzzle)

        # Use the blank position already tracked by the starter class.
        elif choice == '3':
            blank_row, blank_col = initial_puzzle.blankLocation
            print('Blank position:', blank_row, blank_col)
            print('Row and column numbers start at 0.')

        # Use the starter's existing legal-move function.
        elif choice == '4':
            print('Legal moves:', initial_puzzle.legalMoves())

        # Demonstrate a move on a new board, keeping the initial board unchanged.
        elif choice == '5':
            legal_moves = initial_puzzle.legalMoves()
            print('Legal moves:', legal_moves)
            move = input('Type a legal move and press Enter: ').strip().lower()
            clear_screen()
            if move in legal_moves:
                next_puzzle = initial_puzzle.result(move)
                print('After ' + move.upper() + ':')
                for row in next_puzzle.cells:
                    print(format_row(row))
            else:
                print('That move is not legal from the initial board.')

        # Keep moving from the current board until the target is reached.
        elif choice == '6':
            play_puzzle(initial_puzzle, goal_puzzle)
            continue

        # Walk through the example solution one state at a time.
        elif choice == '7':
            show_goal_walkthrough(initial_puzzle, goal_puzzle)
            continue

        # Return to the main menu or explain an invalid choice.
        elif choice == '0':
            return
        else:
            print('Please choose a number from 0 to 7.')

        # Keep the result visible until the user is ready to return to the menu.
        input('\nPress Enter to return to the demonstrations menu...')


