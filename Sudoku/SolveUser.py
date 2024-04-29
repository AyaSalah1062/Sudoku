class SolveUser:
    def __init__(self, puzzle):
        self.puzzle = puzzle

    def solve(self, flag):
        # Start the solution process with different algorithms
        if self.is_solved():
            return self.puzzle

        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return None

        row, col = empty_cell
        domain_values = list(self.get_domain_values(row, col))
        domain_values.sort(key=lambda num: self.count_constrained_values(row, col, num))

        for num in domain_values:
            if self.is_valid_move(row, col, num):
                temp_puzzle = [row[:] for row in self.puzzle]  # Make a copy of the puzzle
                temp_puzzle[row][col] = num  # Assign the value temporarily

                if self.apply_arc_consistency(flag):
                    if self.forward_checking():
                        if self.mrv():
                            if self.lcv(row, col):
                                solution = SolveUser(temp_puzzle).solve(flag)
                                if solution:
                                    return solution

        # If no solution found using other algorithms, resort to backtracking
        return self.solve_with_backtracking()

    def solve_with_backtracking(self):
        # Solve the puzzle using backtracking
        if self.is_solved():
            return self.puzzle

        empty_cell = self.find_empty_cell()
        if not empty_cell:
            return None

        row, col = empty_cell
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                temp_puzzle = [row[:] for row in self.puzzle]  # Make a copy of the puzzle
                temp_puzzle[row][col] = num  # Assign the value temporarily

                solution = SolveUser(temp_puzzle).solve_with_backtracking()
                if solution:
                    return solution

        return None
    
    def apply_arc_consistency(self, flag):
        queue = []
        domains = [[list(range(1, 10)) for _ in range(9)] for _ in range(9)]
        steps = []

        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] != 0:
                    domains[i][j] = [self.puzzle[i][j]]
                    queue.append((i, j))

        def revise(xi, xj):
            revised = False
            removed_values = []
            old_domain = domains[xi[0]][xi[1]].copy()
            for value in domains[xi[0]][xi[1]]:
                if isinstance(domains[xj[0]][xj[1]], list) and value in domains[xj[0]][xj[1]]:
                    domains[xi[0]][xi[1]].remove(value)
                    removed_values.append(value)
                    revised = True
            if flag & revised:
                steps.append(((xi[0], xi[1]), (xj[0], xj[1]), removed_values))
                print("step", len(steps), ":")
                print("    Queue size:", len(queue))
                print("    Arc: (", xi[0], " , ", xi[1], ") -> (", xj[0], " , ", xj[1], ")")
                print("    Domains: ", old_domain, " -> ", domains[xj[0]][xj[1]])
                print("    Remove", removed_values, "From (", xi[0], " , ", xi[1], ")")
                print("    New Domain:", domains[xi[0]][xi[1]])
                print()
            return revised

        while queue:
            xi, xj = queue.pop(0)
            for i in range(9):
                if i != xi and revise((i, xj), (xi, xj)):
                    if len(domains[i][xj]) == 0:
                        return False
                    queue.append((i, xj))
            for j in range(9):
                if j != xj and revise((xi, j), (xi, xj)):
                    if len(domains[xi][j]) == 0:
                        return False
                    queue.append((xi, j))

        return True

    def forward_checking(self):
        for row in range(9):
            for col in range(9):
                if self.puzzle[row][col] == 0:
                    domain = self.get_domain_values(row, col)
                    if not domain:
                        return False
        return True

    def mrv(self):
        min_remaining_values = float('inf')
        selected_cell = None
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    remaining_values = len(self.get_domain_values(i, j))
                    if remaining_values < min_remaining_values:
                        min_remaining_values = remaining_values
                        selected_cell = (i, j)
        return selected_cell

    def lcv(self, row, col):
        domain_values = self.get_domain_values(row, col)
        domain_values.sort(key=lambda num: self.count_constrained_values(row, col, num))
        return domain_values

    def count_constrained_values(self, row, col, num):
        count = 0
        for i in range(9):
            if i != col and not self.is_valid_move(row, i, num):
                count += 1
            if i != row and not self.is_valid_move(i, col, num):
                count += 1
        for i in range(row - row % 3, row - row % 3 + 3):
            for j in range(col - col % 3, col - col % 3 + 3):
                if (i != row or j != col) and not self.is_valid_move(i, j, num):
                    count += 1
        return count

    def get_domain_values(self, row, col):
        domain = set(range(1, 10))
        for i in range(9):
            if self.puzzle[row][i] in domain:
                domain.remove(self.puzzle[row][i])
            if self.puzzle[i][col] in domain:
                domain.remove(self.puzzle[i][col])
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.puzzle[i][j] in domain:
                    domain.remove(self.puzzle[i][j])
        return domain

    def is_valid_move(self, row, col, num):
        if num in self.puzzle[row]:
            return False
        if num in [self.puzzle[i][col] for i in range(9)]:
            return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.puzzle[i][j] == num:
                    return False
        return True

    def is_solved(self):
        for row in self.puzzle:
            if 0 in row:
                return False
        return True

    def find_empty_cell(self):
        for i in range(9):
            for j in range(9):
                if self.puzzle[i][j] == 0:
                    return (i, j)
        return None
