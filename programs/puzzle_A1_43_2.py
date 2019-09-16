"""
A* search using Manhattan distance heuristic.
"""

import heapq
import sys


class Puzzle(object):
    def __init__(self, init_state, goal_state):
        # You may add more attributes as necessary
        self.init_state = init_state
        self.goal_state = goal_state

        self.size = 3
    
    def h(self, state):
        """
        Returns sum of number of steps needed to resolve linear conflicts on 
        both axes and manhattan distances.
        """
        conflicts = 0

        cur_goal_pairs = []
        for i in xrange(len(state)):
            row = state[i]
            goal_row = self.goal_state[i]
            col = [state[j][i] for j in xrange(len(state))]
            goal_col = [self.goal_state[j][i] for j in xrange(len(self.goal_state))]
            cur_goal_pairs.extend([(row, goal_row), (col, goal_col)])

        for cur, goal in cur_goal_pairs:
            in_goal = [goal.index(elem) for elem in cur if elem in goal and elem != 0]
            if not in_goal:
                continue
            conflict_arr = [0 for i in xrange(len(in_goal))]
            for j in xrange(len(in_goal)):
                for k in xrange(j + 1, len(in_goal)):
                    if in_goal[j] > in_goal[k]:
                        conflict_arr[j] += 1
                        conflict_arr[k] += 1
            conflict_max = max(conflict_arr)
            if conflict_max > 0:
                # Not guaranteed to work for dimension n > 3
                conflicts += max(1, conflict_arr.count(conflict_max) - 1)

        return self.manhattan(state) + 2 * conflicts

    def manhattan(self, state):
        """
        Returns sum of manhattan distances of all tiles except blank tile.
        """
        loc = {
            val: (i, j)
            for i, row in enumerate(self.goal_state)
            for j, val in enumerate(row)
        }

        def calculate_cost(i, j):
            val = state[i][j]
            goal_i, goal_j = loc[val]
            return abs(goal_i - i) + abs(goal_j - j)

        return sum(
            calculate_cost(i, j) for i in xrange(self.size)
            for j in xrange(self.size) if state[i][j])

    def solve(self):
        def find_blank(state):
            for i in xrange(self.size):
                for j in xrange(self.size):
                    if not state[i][j]:
                        return (i, j)

        def generate_state(old_state, action, i, j):
            # Much faster than deep.deepcopy(x) because we know old_state is a
            # non-recursive 2D list.
            # Time to explore all nodes fell from 27s to 8s
            state = [row[:] for row in old_state]
            if action == "UP":
                state[i][j], state[i + 1][j] = state[i + 1][j], state[i][j]
            if action == "DOWN":
                state[i][j], state[i - 1][j] = state[i - 1][j], state[i][j]
            if action == "LEFT":
                state[i][j], state[i][j + 1] = state[i][j + 1], state[i][j]
            if action == "RIGHT":
                state[i][j], state[i][j - 1] = state[i][j - 1], state[i][j]
            return state

        def successors(state):
            actions = []
            blank_i, blank_j = find_blank(state)
            if blank_i < self.size - 1:
                actions.append("UP")
            if blank_i > 0:
                actions.append("DOWN")
            if blank_j < self.size - 1:
                actions.append("LEFT")
            if blank_j > 0:
                actions.append("RIGHT")
            return [(action, generate_state(state, action, blank_i, blank_j))
                    for action in actions]

        pred = {}

        str_init = str(self.init_state)

        def backtrack(state):
            result = []
            cur = str(state)
            while cur != str_init:
                cur, action = pred[cur]
                result.append(action)
            return result[::-1]

        # Frontier is (f, state, g)
        frontier = [(self.h(self.init_state), self.init_state, 0)]
        frontier_set = set([str_init])
        visited = set()
        while frontier:
            _, state, g = heapq.heappop(frontier)
            str_old_state = str(state)
            frontier_set.remove(str_old_state)

            if state == self.goal_state:
                return backtrack(state)
            visited.add(str_old_state)
            new_g = g + 1
            for new_action, new_state in successors(state):
                str_state = str(new_state)
                if str_state not in visited and str_state not in frontier_set:
                    pred[str_state] = (str_old_state, new_action)
                    new_score = new_g + self.h(new_state)
                    frontier_set.add(str_state)
                    heapq.heappush(frontier, (new_score, new_state, new_g))
        return ["UNSOLVABLE"]

    # You may add more (helper) methods if necessary.
    # Note that our evaluation scripts only call the solve method.
    # Any other methods that you write should be used within the solve() method


if __name__ == "__main__":
    # do NOT modify below
    if len(sys.argv) != 3:
        raise ValueError("Wrong number of arguments!")

    try:
        f = open(sys.argv[1], 'r')
    except IOError:
        raise IOError("Input file not found!")

    init_state = [[0 for i in xrange(3)] for j in xrange(3)]
    goal_state = [[0 for i in xrange(3)] for j in xrange(3)]
    lines = f.readlines()

    i, j = 0, 0
    for line in lines:
        for number in line:
            if '0' <= number <= '8':
                init_state[i][j] = int(number)
                j += 1
                if j == 3:
                    i += 1
                    j = 0

    for i in xrange(1, 9):
        goal_state[(i - 1) // 3][(i - 1) % 3] = i
    goal_state[2][2] = 0

    puzzle = Puzzle(init_state, goal_state)
    ans = puzzle.solve()

    with open(sys.argv[2], 'a') as f:
        for answer in ans:
            f.write(answer + '\n')
