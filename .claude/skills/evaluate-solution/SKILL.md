---
name: evaluate-solution
description: Evaluate a written solution -- reads the problem statement, runs the provided examples, generates and tests edge cases, checks correctness and complexity. Use after writing a solution to get it tested and reviewed. Handles Python (DSA and pandas), SQL, PowerQuery, and DAX.
argument-hint: "[solution-file]"
context: fork
agent: solution-evaluator
---

Current branch: !`git branch --show-current`

Evaluate the solution on the current branch. $ARGUMENTS
