import sys


# <DKA - October 9th 2026> clear_screen
# Description: Clear the terminal and scrollback before showing a new menu or board.
# Input: No arguments.
# Output: A cleared interactive terminal; returns None.
def clear_screen():
    # Keep redirected output and saved files free of terminal commands.
    if sys.stdout.isatty():
        print('\033[2J\033[3J\033[H', end='', flush=True)
