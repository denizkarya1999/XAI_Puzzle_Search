from screen import clear_screen
from heapq import heappop, heappush
from itertools import count
from pathlib import Path
from time import perf_counter


# <DKA - October 9th 2026> UCS
# Description: Use a priority queue to find a minimum-cost path.
# Input: A search problem with nonnegative move costs.
# Output: A UCS search object.
class UCS:
    # <DKA - October 9th 2026> UCS.__init__
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

    # <DKA - October 9th 2026> UCS.search
    # Description: Explore the board with the lowest total path cost first.
    # Input: show_steps enables board and action printing; move costs must be nonnegative.
    # Output: Minimum-cost solution actions, or None if no solution exists.
    def search(self, show_steps=False):
        # Reset measurements for this run.
        start_time = perf_counter()
        display_time = 0.0
        self.runtime = 0.0
        self.max_depth = 0
        self.states_explored = 0
        self.states_expanded = 0
        self.states_discovered = 1
        start = self.problem.getStartState()

        # Use insertion order to break ties between equal-cost paths.
        order = count()
        frontier = [(0, next(order), start, [])]
        best_cost = {start: 0}

        while frontier:
            path_cost, entry_order, state, path = heappop(frontier)

            # Skip an old entry if a cheaper route to its board was found.
            if path_cost != best_cost[state]:
                continue
            self.states_explored += 1

            # Optionally show the current board and its actions.
            if show_steps:
                display_start = perf_counter()
                clear_screen()
                print('\nCurrent board:')
                for row in state.cells:
                    display_row = []
                    for tile in row:
                        display_row.append('-' if tile == 0 else str(tile))
                    print(' '.join(display_row))
                print('Actions taken:', path)
                display_time += perf_counter() - display_start

            # A goal is accepted only when it is removed as the cheapest entry.
            if self.problem.isGoalState(state):
                self.runtime = perf_counter() - start_time - display_time
                return path

            self.states_expanded += 1
            for next_state, action, cost in self.problem.getSuccessors(state):
                if cost < 0:
                    raise ValueError('UCS requires nonnegative move costs.')
                next_cost = path_cost + cost

                # Keep a new state, or replace its route with a cheaper one.
                if next_state not in best_cost or next_cost < best_cost[next_state]:
                    if next_state not in best_cost:
                        self.states_discovered += 1
                    best_cost[next_state] = next_cost
                    next_path = path + [action]
                    heappush(frontier, (next_cost, next(order), next_state, next_path))
                    self.max_depth = max(self.max_depth, len(next_path))

        self.runtime = perf_counter() - start_time - display_time
        return None

    # <DKA - October 9th 2026> UCS.save_results
    # Description: Save the solution and measurements.
    # Input: Solution actions (or None) and an optional folder.
    # Output: Creates output_UCS.txt and returns its file path.
    def save_results(self, actions, output_dir=None):
        # Create the results folder beside eightpuzzle.py.
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / 'results'
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'output_UCS.txt'

        lines = ['UCS', '**********', '']
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
