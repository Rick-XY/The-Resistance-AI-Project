# resistanceAI

AI platform for the card game resistance.

Xinyu Lei (22604588)

# Description

This projects aims to provide a set of java classes and interface to facilliate agents playing Don Eskridge's card game: Resistance.

# Getting started

## Python

To run the contest, you should edit the `__main__.py` file to import agent class, and add different agents to the agent array.

The basic command line game code can then be executed using the command:

`python3 resistance`

called from `src-py` (the directory containing the `resistance` package).

The `ai_tabu_agent.py` file contains the agent with basic spy logic and resistance member with tabu search algorithm.

The `tabu_with_improvedSpy.py` file contains the agent with improved spy logic and resistance member with tabu search algorithm.

The default agent contains three ai_tabu_agent and four tabu_with_improvedSpy. Run `__main__.py` file will show the number of spy winning and resistant winning in 1000 games in terminal.
