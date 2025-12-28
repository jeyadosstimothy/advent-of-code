from typing import List, Optional
import sys
import re
from pulp import LpProblem, LpVariable, LpMinimize, lpSum, LpInteger, PULP_CBC_CMD

def find_solution_ilp(A: List[List[int]], B: List[int], bounds: int = 299):
    n_vars = len(A[0])
    n_eqs = len(A)

    # Define ILP problem
    prob = LpProblem("MinSumSolution", LpMinimize)

    # Define integer variables
    x = [LpVariable(f"x{i}", lowBound=0, upBound=bounds, cat=LpInteger) for i in range(n_vars)]

    # Objective: minimize sum of variables
    prob += lpSum(x)

    # Constraints: AX = B
    for i in range(n_eqs):
        prob += lpSum(A[i][j] * x[j] for j in range(n_vars)) == B[i]

    # Solve
    prob.solve(PULP_CBC_CMD(msg=0))  # msg=0 to suppress output

    if prob.status != 1:
        return None  # no feasible solution

    return [int(v.varValue) for v in x]


total = 0
num = 0
for line in sys.stdin:
    num = num + 1
    groups = re.search(r"^\[(.*)\] ((?:\([0-9,]*\) )+){(.*)}$", line)
    lights = groups[1]
    buttons = [[int(ss) for ss in s[1:-1].split(",")] for s in groups[2].strip().split(" ")]
    joltage = [int(s) for s in groups[3].split(",")]
    buttons = [[1 if i in button else 0 for i in range(len(joltage))] for button in buttons]
    buttons = list(zip(*buttons))
    ans = find_solution_ilp(buttons, joltage)
    # print(f"input: {num}, answer: {ans}")
    total = total + sum(ans)
print(total)