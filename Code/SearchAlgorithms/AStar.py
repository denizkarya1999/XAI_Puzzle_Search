from screen import clear_screen
from heapq import heappop, heappush
from itertools import count
from pathlib import Path
from time import perf_counter


# <DKA - October 9th 2026> AStar
# Description: Find a minimum-cost path using cost so far plus a goal estimate.
# Input: A puzzle search problem and misplaced or manhattan heuristic.
# Output: An A* search object.
class AStar:
    # <DKA - October 9th 2026> AStar.__init__
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

    # <DKA - October 9th 2026> AStar.misplaced_tiles
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

    # <DKA - October 9th 2026> AStar.manhattan_distances
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

    # <DKA - October 9th 2026> AStar.manhattan_distance
    # Description: Add the individual numbered-tile distances.
    # Input: A puzzle state.
    # Output: Total Manhattan distance; the blank is ignored.
    def manhattan_distance(self, state):
        return sum(self.manhattan_distances(state).values())

    # <DKA - October 9th 2026> AStar.estimate
    # Description: Calculate the selected heuristic for a board.
    # Input: A puzzle state.
    # Output: Its misplaced-tile count or Manhattan distance.
    def estimate(self, state):
        if self.heuristic_name == 'manhattan':
            return self.manhattan_distance(state)
        return self.misplaced_tiles(state)

    # <DKA - October 9th 2026> AStar.search
    # Description: Explore the lowest cost-so-far plus estimated remaining cost.
    # Input: show_steps enables board and action printing; costs must be nonnegative.
    # Output: Optimal solution actions for an admissible heuristic, or None.
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

        # Prioritize f = g + h, using insertion order to break ties.
        order = count()
        frontier = [(self.estimate(start), next(order), 0, start, [])]
        best_cost = {start: 0}

        while frontier:
            priority, entry_order, path_cost, state, path = heappop(frontier)
            if path_cost != best_cost[state]:
                continue
            self.states_explored += 1
            heuristic = self.estimate(state)

            # Optionally show the board, actions, and heuristic details.
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
                if self.heuristic_name == 'manhattan':
                    for tile, distance in sorted(self.manhattan_distances(state).items()):
                        print('Tile ' + str(tile) + ': ' + str(distance))
                print(self.heuristic_label + ':', heuristic)
                print('g(n):', path_cost)
                print('f(n) = g(n) + h(n):', priority)
                display_time += perf_counter() - display_start

            # Accept the goal only when its lowest-priority entry is popped.
            if self.problem.isGoalState(state):
                self.runtime = perf_counter() - start_time - display_time
                return path

            self.states_expanded += 1
            for next_state, action, cost in self.problem.getSuccessors(state):
                if cost < 0:
                    raise ValueError('A* requires nonnegative move costs.')
                next_cost = path_cost + cost

                # Revisit a board if a cheaper route to it is found.
                if next_state not in best_cost or next_cost < best_cost[next_state]:
                    if next_state not in best_cost:
                        self.states_discovered += 1
                    best_cost[next_state] = next_cost
                    next_path = path + [action]
                    priority = next_cost + self.estimate(next_state)
                    heappush(frontier, (priority, next(order), next_cost, next_state, next_path))
                    self.max_depth = max(self.max_depth, len(next_path))

        self.runtime = perf_counter() - start_time - display_time
        return None

    # <DKA - October 9th 2026> AStar.save_results
    # Description: Save the solution and measurements.
    # Input: Solution actions (or None) and an optional folder.
    # Output: Creates a separate AStar results file for the chosen heuristic.
    def save_results(self, actions, output_dir=None):
        # Create the results folder beside eightpuzzle.py.
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / 'results'
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / ('output_A*_' + self.heuristic_name + '.txt')

        lines = ['A*', '**********', 'Priority: f(n) = g(n) + h(n)', 'Heuristic: ' + self.heuristic_label.lower(), self.heuristic_description, '']
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
                current_cost = self.problem.getCostOfActions(actions[:step])
                lines.append('g(n): ' + str(current_cost))
                lines.append('f(n) = g(n) + h(n): ' + str(current_cost + self.estimate(state)))
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
