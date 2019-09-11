import os
import sys


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # You may add more attributes as necessary
        self.init_state = init_state
        self.goal_state = goal_state
        self.actions = list()
        self.solvable = True

        self.size = 3

    def h(self, state):
        """Returns sum of manhattan distances of all tiles except blank tile."""
        cost = 0
        for row in range(self.size):
            for col in range(self.size):
                if state[row][col] != 0:
                    goal_r = (state[row][col] - 1) // self.size;
                    goal_c = (state[row][col] - 1) % self.size;
                    cost += abs(goal_r - row) + abs(goal_c - col)
        return cost

    def eval_score(self, step, state):
        """Returns evaluation function f(x) = g(x) + h(x)."""
        return step + self.h(state)

    def solve(self):
        # TODO: Write your code here
        # return: a list of actions like: ["UP", "DOWN"]
        print(self.init_state, self.goal_state)
        print(self.heuristic(self.init_state))
        return []

    # You may add more (helper) methods if necessary.
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method.

if __name__ == "__main__":
    # do NOT modify below
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    init_state = [[0 for i in range(3)] for j in range(3)]
    goal_state = [[0 for i in range(3)] for j in range(3)]
    lines = f.readlines()

    i,j = 0, 0
    for line in lines:
        for number in line:
            if '0'<= number <= '8':
                init_state[i][j] = int(number)
                j += 1
                if j == 3:
                    i += 1
                    j = 0

    for i in range(1, 9):
        goal_state[(i-1)//3][(i-1)%3] = i
    goal_state[2][2] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer+'\n')







