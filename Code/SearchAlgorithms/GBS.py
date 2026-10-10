from screen import clear_screen
from heapq import heappop, heappush
from itertools import count
from pathlib import Path
from time import perf_counter


# <DKA - October 9th 2026> GBS
# Description: Guide greedy search with misplaced tiles or Manhattan distance.
# Input: A puzzle search problem with a supplied goal board.
# Output: A GBS search object.
class GBS:
    # <DKA - October 9th 2026> GBS.__init__
    # Description: Store the problem and reset measurements.
    # Input: A search problem and heuristic name: misplaced or manhattan.
    # Output: Initialized search object; returns None.
    def __init__(self, problem, heuristic='misplaced'):
        if heuristic not in ('misplaced', 'manhattan'):
            raise ValueError('Choose misplaced or manhattan.')
        self.problem = problem
        self.heuristic_name = heuristic
        if heuristic == 'misplaced':
            self.heuristic_label = 'Misplaced tiles'
            self.heuristic_description = 'Each misplaced numbered tile counts 1; the blank is ignored.'
        else:
            self.heuristic_label = 'Manhattan distance'
            self.heuristic_description = 'Add each numbered tile\'s row and column distances; the blank is ignored.'
        self.states_explored = 0
        self.states_expanded = 0
        self.states_discovered = 0
        self.runtime = 0.0
        self.max_depth = 0

    # <DKA - October 9th 2026> GBS.misplaced_tiles
    # Description: Count numbered tiles outside their goal positions; ignore the blank.
    # Input: A puzzle state.
    # Output: The number of misplaced tiles.
    def misplaced_tiles(self, state):
        misplaced = 0
        for row in range(3):
            for col in range(3):
                tile = state.cells[row][col]
                if tile != 0 and tile != self.problem.goal.cells[row][col]:
                    misplaced += 1
        return misplaced

    # <DKA - October 9th 2026> GBS.manhattan_distances
    # Description: Calculate the distance of each numbered tile from its goal.
    # Input: A puzzle state.
    # Output: A dictionary of tile numbers and distances; excludes the blank.
    def manhattan_distances(self, state):
        goal_positions = {}
        for row in range(3):
            for col in range(3):
                tile = self.problem.goal.cells[row][col]
                if tile != 0:
                    goal_positions[tile] = (row, col)

        distances = {}
        for row in range(3):
            for col in range(3):
                tile = state.cells[row][col]
                if tile != 0:
                    goal_row, goal_col = goal_positions[tile]
                    distances[tile] = abs(row - goal_row) + abs(col - goal_col)
        return distances

    # <DKA - October 9th 2026> GBS.manhattan_distance
    # Description: Add the individual numbered-tile distances.
    # Input: A puzzle state.
    # Output: Total Manhattan distance; the blank is ignored.
    def manhattan_distance(self, state):
        return sum(self.manhattan_distances(state).values())

    # <DKA - October 9th 2026> GBS.estimate
    # Description: Calculate the selected heuristic for a board.
    # Input: A puzzle state.
    # Output: Its misplaced-tile count or Manhattan distance.
    def estimate(self, state):
        if self.heuristic_name == 'manhattan':
            return self.manhattan_distance(state)
        return self.misplaced_tiles(state)

    # <DKA - October 9th 2026> GBS.search
    # Description: Explore the board with the smallest selected heuristic first.
    # Input: show_steps enables board and action printing.
    # Output: Solution actions, or None if no solution exists; the path may not be shortest.
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

        # Rank boards by the heuristic alone; insertion order breaks ties.
        order = count()
        frontier = [(self.estimate(start), next(order), start, [])]
        visited = {start}

        while frontier:
            heuristic, entry_order, state, path = heappop(frontier)
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
                # Show each numbered tile's contribution to the total.
                if self.heuristic_name == 'manhattan':
                    for tile, distance in sorted(self.manhattan_distances(state).items()):
                        print('Tile ' + str(tile) + ': ' + str(distance))
                print(self.heuristic_label + ':', heuristic)
                display_time += perf_counter() - display_start

            if self.problem.isGoalState(state):
                self.runtime = perf_counter() - start_time - display_time
                return path

            # Add unseen boards using their heuristic values as priorities.
            self.states_expanded += 1
            for next_state, action, cost in self.problem.getSuccessors(state):
                if next_state not in visited:
                    visited.add(next_state)
                    self.states_discovered += 1
                    next_path = path + [action]
                    heappush(frontier, (self.estimate(next_state), next(order), next_state, next_path))
                    self.max_depth = max(self.max_depth, len(next_path))

        self.runtime = perf_counter() - start_time - display_time
        return None

    # <DKA - October 9th 2026> GBS.save_results
    # Description: Save the solution and measurements.
    # Input: Solution actions (or None) and an optional folder.
    # Output: Creates a separate GBS results file for the chosen heuristic.
    def save_results(self, actions, output_dir=None):
        # Create the results folder beside eightpuzzle.py.
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / 'results'
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / ('output_GBS_' + self.heuristic_name + '.txt')

        lines = ['GBS', '**********', 'Heuristic: ' + self.heuristic_label.lower(), self.heuristic_description, '']
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
                if self.heuristic_name == 'manhattan':
                    for tile, distance in sorted(self.manhattan_distances(state).items()):
                        lines.append('Tile ' + str(tile) + ': ' + str(distance))
                lines.append(self.heuristic_label + ': ' + str(self.estimate(state)))
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
