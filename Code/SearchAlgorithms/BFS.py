from screen import clear_screen
from collections import deque
from pathlib import Path
from time import perf_counter


# <DKA - October 9th 2026> BFS
# Description: Use a queue to find a shortest path with equal move costs.
# Input: A search problem.
# Output: A BFS search object.
class BFS:
    # <DKA - October 9th 2026> BFS.__init__
    # Description: Store the problem and reset measurements.
    # Input: A search problem.
    # Output: Initialized search object; returns None.
    def __init__(self, problem):
        self.problem = problem
        self.states_explored = 0
        self.states_expanded = 0
        self.states_discovered = 0
        self.runtime = 0.0
        self.max_depth = 0

    # <DKA - October 9th 2026> BFS.search
    # Description: Explore boards level by level.
    # Input: show_steps enables board and action printing.
    # Output: Solution actions, or None if no solution exists.
    def search(self, show_steps=False):
        # Exclude board printing from the search time.
        start_time = perf_counter()
        display_time = 0.0
        self.runtime = 0.0
        self.max_depth = 0

        # Reset state counts for this run.
        self.states_explored = 0
        self.states_expanded = 0
        self.states_discovered = 1
        start = self.problem.getStartState()

        # Queue the starting board with an empty path.
        queue = deque([(start, [])])
        visited = {start}

        while queue:
            # Explore the oldest queued board first.
            state, path = queue.popleft()
            self.states_explored += 1

            # Optionally display the board and its actions.
            if show_steps:
                display_start = perf_counter()
                clear_screen()
                print('\nCurrent board:')
                for row in state.cells:
                    display_row = []
                    for tile in row:
                        if tile == 0:
                            display_row.append('-')
                        else:
                            display_row.append(str(tile))
                    print(' '.join(display_row))
                print('Actions taken:', path)
                display_time += perf_counter() - display_start

            # Stop at the first goal: its path is shortest.
            if self.problem.isGoalState(state):
                self.runtime = perf_counter() - start_time - display_time
                return path

            # Count a state when its successors are generated.
            self.states_expanded += 1

            # Add unseen boards and their paths to the queue.
            for next_state, action, cost in self.problem.getSuccessors(state):
                if next_state not in visited:
                    visited.add(next_state)
                    self.states_discovered += 1
                    queue.append((next_state, path + [action]))
                    self.max_depth = max(self.max_depth, len(path) + 1)

        self.runtime = perf_counter() - start_time - display_time
        return None

    # <DKA - October 9th 2026> BFS.save_results
    # Description: Save the solution and measurements.
    # Input: Solution actions (or None) and an optional folder.
    # Output: Creates output_BFS.txt and returns its file path.
    def save_results(self, actions, output_dir=None):
        # Create the results folder beside eightpuzzle.py.
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / 'results'
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'output_BFS.txt'

        lines = ['BFS', '**********', '']
        if actions is None:
            lines.append('No solution found.')
            path_cost = 'N/A'
            solution_depth = 'N/A'
        else:
            path_cost = self.problem.getCostOfActions(actions)
            solution_depth = len(actions)
            lines.append('Solution path (states and actions):')
            state = self.problem.getStartState()

            # Replay the solution to record each board.
            for step in range(len(actions) + 1):
                label = ' (goal)' if step == len(actions) else ''
                lines.append('State ' + str(step) + label + ':')
                for row in state.cells:
                    display_row = []
                    for tile in row:
                        display_row.append('-' if tile == 0 else str(tile))
                    lines.append(' '.join(display_row))
                if step < len(actions):
                    action = actions[step]
                    lines.append('Action: ' + action.upper())
                    state = state.result(action)
                lines.append('')
            lines.append('Actions taken: ' + str(actions))

        # Append search measurements and the saved-file location.
        lines.extend([
            '',
            'Path cost: ' + str(path_cost),
            'Solution depth (number of moves): ' + str(solution_depth),
            'Depth of search tree (maximum generated depth): ' + str(self.max_depth),
            'Time taken (seconds, excluding board display and file writing): ' + format(self.runtime, '.6f'),
            'Nodes expanded: ' + str(self.states_expanded),
            'States explored (checked for the goal): ' + str(self.states_explored),
            'Unique states discovered (including queued boards): ' + str(self.states_discovered),
            'Results saved to: ' + str(output_file),
        ])
        output_file.write_text('\n'.join(lines) + '\n', encoding='utf-8')
        return output_file
