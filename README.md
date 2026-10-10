# XAI Puzzle Search

XAI 8-Puzzle 1.0 - an interactive Python eight-puzzle solver with BFS, DFS, IDS, UCS, greedy best-first search, and A*.

Developed by Deniz K. Acikbas  
Release date: October 9th 2026  
Programming language: Python

This program solves the CIS 579 eight-puzzle assignment and demonstrates how the blank moves around the board. Each legal move costs 1.

## Requirements

Python 3 is required. The program uses only the Python standard library; no additional packages are needed.

From this folder, open a terminal and enter the `Code` folder before running the examples below:

```bash
cd Code
```

## Interactive menu

```bash
python3 eightpuzzle.py
```

Running without parameters opens the main menu:

```text
XAI 8-Puzzle 1.0
1. Puzzle demonstrations
2. Search algorithms
3. About
0. Exit
```

Type a number and press Enter. Demonstrations include viewing the boards, checking legal moves, making continuous moves until the goal, and walking through an example solution. The example walkthrough uses a fixed solution; the search algorithms calculate their own solutions.

The search menu asks whether to display each explored board and its actions. Type `y` to show them, or press Enter for only the final summary. Press Enter after results to return to the menu. Menus and changing boards clear the interactive terminal.

The default boards are:

```text
Initial     Goal
- 2 3       1 2 3
1 4 5       8 - 4
8 7 6       7 6 5
```

## Command-line mode

Command-line mode runs directly without menu prompts. For one search:

```bash
python3 eightpuzzle.py --search "A*" --initial '[[-,2,3],[1,4,5],[8,7,6]]' --goal '[[1,2,3],[8,-,4],[7,6,5]]' --heuristic manhattan
```

To run all required searches and both heuristics:

```bash
python3 eightpuzzle.py \
  --search "BFS/DFS/IDS/UCS/GBS/A*" \
  --initial '[[-,2,3],[1,4,5],[8,7,6]]' \
  --goal '[[1,2,3],[8,-,4],[7,6,5]]' \
  --heuristic "misplaced/manhattan"
```

Keep a command on one line, or put `\` at the end of each continued line as shown above. Use ordinary quotes when copying commands into a terminal.

| Argument | Meaning |
| --- | --- |
| `--search` | Required: one algorithm or several separated by `/`. |
| `--initial` | Required: a nested list containing the initial 3-by-3 board. |
| `--goal` | Required: a nested list containing the goal 3-by-3 board. |
| `--heuristic` | `misplaced`, `manhattan`, or both separated by `/`. Default: `misplaced`. Used by GBS and A*. |
| `--show-steps` | Optional flag to display each explored board and its actions. |
| `--help` | Display command-line usage. |

Search names are case-insensitive. The program also recognizes the assignment's en-dash flags, such as `–search`. Every board must contain each number from 1 to 8 once and exactly one blank, written as `-` or `0`. Invalid boards and unreachable initial/goal pairs produce an error.

BFS, DFS, IDS, and UCS run once per batch. GBS and A* run once per selected heuristic. The assignment's full lists, `BFS/DFS/IDS/UCS/GBS/A*/Beam` and `misplaced/manhattan/other`, are accepted: **Beam and other are not implemented**, so the program reports this and skips them.

## Search algorithms and heuristics

- **BFS:** explores the shallowest states first using a queue.
- **DFS:** explores a branch deeply using a stack. Its solution can be long and is not guaranteed shortest.
- **IDS:** repeats depth-limited DFS with increasing limits.
- **UCS:** explores the lowest accumulated path cost first.
- **GBS:** explores the smallest heuristic estimate first; shortest solutions are not guaranteed.
- **A*:** explores the smallest `f(n) = g(n) + h(n)`, where `g(n)` is the path cost and `h(n)` is the selected heuristic.

Misplaced tiles counts each numbered tile outside its goal position as 1. Manhattan distance adds each numbered tile's horizontal and vertical distances from its goal. Both ignore the blank. Manhattan displays also show each tile's distance.

## Results

Results are saved in `Code/results`, which is created automatically if needed. Each run overwrites the corresponding results file. Generated reports are kept locally and are not tracked in Git.

| Search | Results file |
| --- | --- |
| BFS | `output_BFS.txt` |
| DFS | `output_DFS.txt` |
| IDS | `output_IDS.txt` |
| UCS | `output_UCS.txt` |
| GBS, misplaced | `output_GBS_misplaced.txt` |
| GBS, Manhattan | `output_GBS_manhattan.txt` |
| A*, misplaced | `output_A*_misplaced.txt` |
| A*, Manhattan | `output_A*_manhattan.txt` |

The `*` in the A* filenames is a literal character. Quote these filenames in terminal commands.

Each report contains an algorithm heading, `**********`, the solution boards and actions, path cost, solution depth, maximum generated search depth, elapsed search time, expanded nodes, explored states, and unique discovered states. The last line gives the saved file's location.

Search depth and solution depth are reported separately. Runtime excludes board printing and file writing. IDS counts repeated visits and expansions across depth limits; its discovered-state count is unique across iterations. Expanded-node counts describe expansions and are not a direct measurement of memory in bytes.

## Project layout

- `Code/`: Python source and local generated results.
- `README.md`: setup, usage, and references.

## Main files

- `eightpuzzle.py`: entry point, boards, search problem, menus, and command-line parsing.
- `puzzle.py`: board representation and legal moves.
- `SearchAlgorithms/`: BFS, DFS, IDS, UCS, GBS, and A* classes.
- `search.py`: functions that run searches, save reports, and print summaries.
- `demonstrations.py`: puzzle demonstrations and manual play.
- `About.py`: program information.
- `screen.py`: interactive terminal clearing.
- `util.py`: the starter search-interface error helper.

## References and acknowledgment

- CIS 579 Programming Assignment 1: assignment requirements and example boards. The course handout is kept locally and is not included in this repository.
- [UC Berkeley Pacman AI Projects](http://ai.berkeley.edu): source of the supplied starter code. Original licensing and attribution notices are retained in the derived starter files.
- ChatGPT, OpenAI: assistance with this project and report, including algorithm explanations, menu options, and the comparison table.

## Topics

#python #eight-puzzle #artificial-intelligence #search-algorithms #breadth-first-search #depth-first-search #iterative-deepening #uniform-cost-search #greedy-best-first-search #a-star
