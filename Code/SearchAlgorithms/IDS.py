from screen import clear_screen
from pathlib import Path
from time import perf_counter


# <DKA - October 9th 2026> IDS
# Description: Find a shortest path by gradually increasing the DFS depth limit.
# Input: A search problem with equal move costs.
# Output: An IDS search object.
class IDS:
    # <DKA - October 9th 2026> IDS.__init__
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

    # <DKA - October 9th 2026> IDS.search
    # Description: Repeat depth-limited DFS with limits 0, 1, 2, and so on.
    # Input: show_steps enables board and action printing.
    # Output: A shortest solution action list, or None if no solution exists.
    def search(self, show_steps=False):
        # Reset measurements once for the entire iterative-deepening run.
        start_time = perf_counter()
        self.display_time = 0.0
        self.runtime = 0.0
        self.max_depth = 0
        self.states_explored = 0
        self.states_expanded = 0
        self.states_discovered = 1
        self.unique_states = {self.problem.getStartState()}
        self.depth_limit = 0

        while True:
            actions, cutoff = self.depth_limited_search(self.depth_limit, show_steps)
            if actions is not None or not cutoff:
                self.runtime = perf_counter() - start_time - self.display_time
                return actions
            self.depth_limit += 1

    # <DKA - October 9th 2026> IDS.depth_limited_search
    # Description: Explore paths without going beyond the supplied depth limit.
    # Input: A depth limit and an optional board-display flag.
    # Output: A solution (or None) and whether deeper paths may remain.
    def depth_limited_search(self, limit, show_steps=False):
        start = self.problem.getStartState()
        stack = [(start, [], {start})]
        cutoff = False

        while stack:
            state, path, path_states = stack.pop()
            self.states_explored += 1

            # Optionally show the board and the actions that reached it.
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
                self.display_time += perf_counter() - display_start

            if self.problem.isGoalState(state):
                return path, cutoff

            # Stop this branch at the limit and try a deeper search later.
            if len(path) == limit:
                cutoff = True
                continue

            self.states_expanded += 1
            for next_state, action, cost in self.problem.getSuccessors(state):
                # Avoid cycles on this path; other paths may revisit the state.
                if next_state not in path_states:
                    next_path = path + [action]
                    stack.append((next_state, next_path, path_states | {next_state}))
                    self.max_depth = max(self.max_depth, len(next_path))
                    self.unique_states.add(next_state)
                    self.states_discovered = len(self.unique_states)

        return None, cutoff

    # <DKA - October 9th 2026> IDS.save_results
    # Description: Save the solution and measurements.
    # Input: Solution actions (or None) and an optional folder.
    # Output: Creates output_IDS.txt and returns its file path.
    def save_results(self, actions, output_dir=None):
        # Create the results folder beside eightpuzzle.py.
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / 'results'
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'output_IDS.txt'

        lines = ['IDS', '**********', '']
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
            'Counts include repeated visits across depth limits.',
            'Final depth limit: ' + str(self.depth_limit),
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
