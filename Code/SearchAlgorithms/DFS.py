from screen import clear_screen
from pathlib import Path
from time import perf_counter


# <DKA - October 9th 2026> DFS
# Description: Use a stack to follow deep branches; paths may be longer.
# Input: A search problem.
# Output: A DFS search object.
class DFS:
    # <DKA - October 9th 2026> DFS.__init__
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

    # <DKA - October 9th 2026> DFS.get_path
    # Description: Recover a path by following parent links.
    # Input: A state and its parent-link dictionary.
    # Output: Actions from the start to this state.
    def get_path(self, state, parents):
        actions = []
        while parents[state][0] is not None:
            parent, action = parents[state]
            actions.append(action)
            state = parent
        # Reverse the backward path into start-to-goal order.
        actions.reverse()
        return actions

    # <DKA - October 9th 2026> DFS.search
    # Description: Explore the newest board first until reaching the goal.
    # Input: show_steps enables board and action printing.
    # Output: Solution actions, or None if no solution exists.
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

        # Parent links recover paths without storing copies for every board.
        stack = [start]
        parents = {start: (None, None)}
        depths = {start: 0}

        while stack:
            # Explore the newest stacked board first.
            state = stack.pop()
            self.states_explored += 1
            is_goal = self.problem.isGoalState(state)
            path = self.get_path(state, parents) if show_steps or is_goal else None

            # Optionally display the board and its actions.
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

            # Stop when the goal is reached.
            if is_goal:
                self.runtime = perf_counter() - start_time - display_time
                return path

            # Push unseen successors; the last one is explored first.
            self.states_expanded += 1
            for next_state, action, cost in self.problem.getSuccessors(state):
                if next_state not in parents:
                    parents[next_state] = (state, action)
                    depths[next_state] = depths[state] + 1
                    self.max_depth = max(self.max_depth, depths[next_state])
                    self.states_discovered += 1
                    stack.append(next_state)

        self.runtime = perf_counter() - start_time - display_time
        return None

    # <DKA - October 9th 2026> DFS.save_results
    # Description: Save the solution and measurements.
    # Input: Solution actions (or None) and an optional folder.
    # Output: Creates output_DFS.txt and returns its file path.
    def save_results(self, actions, output_dir=None):
        # Create the results folder beside eightpuzzle.py.
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / 'results'
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / 'output_DFS.txt'

        lines = ['DFS', '**********', '']
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
