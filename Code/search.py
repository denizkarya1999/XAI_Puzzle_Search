# search.py
# ---------
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


"""
Search problem interface and functions for running puzzle search algorithms.
"""

import util
from SearchAlgorithms.BFS import BFS
from SearchAlgorithms.DFS import DFS
from SearchAlgorithms.IDS import IDS
from SearchAlgorithms.UCS import UCS
from SearchAlgorithms.GBS import GBS
from SearchAlgorithms.AStar import AStar

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()



# <DKA - October 9th 2026> depthFirstSearch
# Description: Run DFS and save its solution and measurements in the results folder.
# Input: A search problem and an optional flag to print each explored board.
# Output: A solution action list (or None) and results/output_DFS.txt.
def depthFirstSearch(problem: SearchProblem, show_steps=False):
    solver = DFS(problem)
    path = solver.search(show_steps=show_steps)
    output_file = solver.save_results(path)

    # Keep the saved-file message as the last result line.
    if path is None:
        print('No solution found.')
    else:
        print('Goal reached in', len(path), 'moves!')
    print('States explored (checked for the goal):', solver.states_explored)
    print('States expanded (generated next boards):', solver.states_expanded)
    print('Unique states discovered (including queued boards):', solver.states_discovered)
    print('Results saved to:', output_file)
    return path

# <DKA - October 9th 2026> iterativeDeepeningSearch
# Description: Run IDS and save its solution and measurements in the results folder.
# Input: A search problem and an optional flag to print each explored board.
# Output: A solution action list (or None) and results/output_IDS.txt.
def iterativeDeepeningSearch(problem: SearchProblem, show_steps=False):
    solver = IDS(problem)
    path = solver.search(show_steps=show_steps)
    output_file = solver.save_results(path)

    # Keep the saved-file message as the last result line.
    if path is None:
        print('No solution found.')
    else:
        print('Goal reached in', len(path), 'moves!')
    print('Counts include repeated visits across depth limits.')
    print('States explored (checked for the goal):', solver.states_explored)
    print('States expanded (generated next boards):', solver.states_expanded)
    print('Unique states discovered (including queued boards):', solver.states_discovered)
    print('Results saved to:', output_file)
    return path

# <DKA - October 9th 2026> breadthFirstSearch
# Description: Run BFS and save its solution and measurements in the results folder.
# Input: A search problem and an optional flag to print explored puzzle boards.
# Output: A solution action list (or None) and results/output_BFS.txt.
def breadthFirstSearch(problem: SearchProblem, show_steps=False):
    solver = BFS(problem)
    path = solver.search(show_steps=show_steps)

    # Create or update the results file after each BFS run.
    output_file = solver.save_results(path)

    # Show the final summary whether or not individual steps were requested.
    if path is None:
        print('No solution found.')
    else:
        print('Goal reached in', len(path), 'moves!')
    print('States explored (checked for the goal):', solver.states_explored)
    print('States expanded (generated next boards):', solver.states_expanded)
    print('Unique states discovered (including queued boards):', solver.states_discovered)
    print('Results saved to:', output_file)

    return path

# <DKA - October 9th 2026> uniformCostSearch
# Description: Run UCS and save its solution and measurements in the results folder.
# Input: A search problem and an optional flag to print explored puzzle boards.
# Output: A solution action list (or None) and results/output_UCS.txt.
def uniformCostSearch(problem: SearchProblem, show_steps=False):
    solver = UCS(problem)
    path = solver.search(show_steps=show_steps)

    # Create or update the results file after each UCS run.
    output_file = solver.save_results(path)

    # Show the final summary whether or not individual steps were requested.
    if path is None:
        print('No solution found.')
    else:
        print('Goal reached in', len(path), 'moves!')
    print('States explored (checked for the goal):', solver.states_explored)
    print('States expanded (generated next boards):', solver.states_expanded)
    print('Unique states discovered (including queued boards):', solver.states_discovered)
    print('Results saved to:', output_file)

    return path

# <DKA - October 9th 2026> greedyBestFirstSearch
# Description: Run greedy search with the chosen heuristic and save its results.
# Input: A search problem, display flag, and misplaced or manhattan heuristic.
# Output: Solution actions (or None) and a separate results file for each heuristic.
def greedyBestFirstSearch(problem: SearchProblem, show_steps=False, heuristic='misplaced'):
    solver = GBS(problem, heuristic=heuristic)
    print(solver.heuristic_description)
    print('Initial ' + solver.heuristic_label.lower() + ':', solver.estimate(problem.getStartState()))
    path = solver.search(show_steps=show_steps)

    # Create or update the results file after each GBS run.
    output_file = solver.save_results(path)

    # Show the final summary whether or not individual steps were requested.
    if path is None:
        print('No solution found.')
    else:
        print('Goal reached in', len(path), 'moves!')
    print('States explored (checked for the goal):', solver.states_explored)
    print('States expanded (generated next boards):', solver.states_expanded)
    print('Unique states discovered (including queued boards):', solver.states_discovered)
    print('Results saved to:', output_file)

    return path


# <DKA - October 9th 2026> aStarSearch
# Description: Run A* with the chosen heuristic and save its results.
# Input: A search problem, display flag, and misplaced or manhattan heuristic.
# Output: Solution actions (or None) and a separate results file for each heuristic.
def aStarSearch(problem: SearchProblem, show_steps=False, heuristic='misplaced'):
    solver = AStar(problem, heuristic=heuristic)
    print(solver.heuristic_description)
    print('Priority: f(n) = g(n) + h(n)')
    print('Initial ' + solver.heuristic_label.lower() + ':', solver.estimate(problem.getStartState()))
    path = solver.search(show_steps=show_steps)

    # Create or update the results file after each AStar run.
    output_file = solver.save_results(path)

    # Show the final summary whether or not individual steps were requested.
    if path is None:
        print('No solution found.')
    else:
        print('Goal reached in', len(path), 'moves!')
    print('States explored (checked for the goal):', solver.states_explored)
    print('States expanded (generated next boards):', solver.states_expanded)
    print('Unique states discovered (including queued boards):', solver.states_discovered)
    print('Results saved to:', output_file)

    return path


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
ids = iterativeDeepeningSearch
astar = aStarSearch
ucs = uniformCostSearch
gbs = greedyBestFirstSearch
