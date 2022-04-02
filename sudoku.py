import random
import itertools


def __solve_rec(_grid, i, j):
    """
    Recursive helper for solve function. Solves the grid from an position (i,j)
    :param _grid: Sudoku to solve
    :param i: row of working position
    :param j: column of working position
    :return: solved grid or False if not possible
    """
    grid = [row[:] for row in _grid][:]  # copy grid array to not change it, but return the solved version
    if 0 not in itertools.chain(*grid):  # If there is no empty cell, we are done
        return grid
    if j == 9:  # jump to next row if at the border
        j -= 9
        i += 1
    if i == 9:  # jump to first row if in the bottom right corner
        i -= 9
    if grid[i][j] == 0:  # if the current cell is empty, we try to fill it
        poss_nums = set(range(1, 10))  # possible numbers to fill in current cell, initialized to sudoku numbers (1-9)
        poss_nums -= set(grid[i])  # numbers already present in the current row, won't be in the current cell
        poss_nums -= {grid[k][j] for k in range(9)}  # neither do those present in the current column
        square = []
        for k in range(3):
            square += grid[(i // 3) * 3 + k][(j // 3) * 3: (j // 3) * 3 + 3]
        poss_nums -= set(square)  # neither those in the current cell's 3x3 sudoku square
        while True:  # Try all the possible numbers (recursively) until a solution is found
            if len(poss_nums) == 0:  # If there is no more possible number, no solution is possible
                grid[i][j] = 0  # reset current cell's value
                return False
            number = random.choice(list(poss_nums))
            poss_nums.remove(number)
            grid[i][j] = number
            solved_grid = __solve_rec(grid, i, j+1)  # recursively try to find a solution
            if solved_grid:
                return solved_grid
    return __solve_rec(grid, i, j+1)


def solve(grid):
    """
    Solve a given sudoku
    :param grid: sudoku to solve
    :return: solved grid or False if no possible solution found
    """
    return __solve_rec(grid, 0, 0)


def generate_grid():
    """
    Generate a full sudoku grid, compliant to the rules.
    :return: 9x9 grid with every number from 1 to 9 appearing exactly once in every row, every column and every
            3x3 sudoku square.
    """
    grid = [[0 for _ in range(9)] for _ in range(9)]
    return solve(grid)


def check(grid):
    """
    Check if a given 9x9 grid complies to the sudoku rules, meaning it is a valid solution to a sudoku.
    :param grid: Solved sudoku
    :return: True if legal solution, False if not.
    """
    for row in grid:  # In every row, every number from 1 to 9 should appear exactly once
        if not set(row) == set(range(1, 10)):
            return False
    for column in [[grid[i][j] for i in range(9)] for j in range(9)]:  # In every column as well
        if not set(column) == set(range(1, 10)):
            return False
    squares = []
    for i in range(3):
        for j in range(3):
            square = []
            for k in range(3):
                square += grid[i * 3 + k][j * 3: j * 3 + 3]
            squares.append(square)
    for square in squares:  # In every sudoku square as well
        if not set(square) == set(range(1, 10)):
            return False
    return True


def mask_values(_grid, percentage):
    """
    Mask a given percentage of the 9x9-grid's cells by setting them to 0.
    :param _grid: 9x9 grid to mask
    :param percentage: percentage of cells to mask
    :return: masked grid
    """
    grid = [row[:] for row in _grid][:]  # copy grid to not modify it but return the masked grid
    for _ in range(round(9*9 * percentage / 100)):
        while True:
            row = random.randint(0, 8)
            column = random.randint(0, 8)
            if not grid[row][column] == 0:  # If we didn't mask the random cell yet, mask it
                grid[row][column] = 0
                break
    return grid


def generate_sudoku(mask_percentage):
    """
    Generates a sudoku very likely to have a unique solution.
    :param mask_percentage: Percentage of cells to be empty (zeroed)
    :return: sudoku grid
    """
    grid = generate_grid()  # generate a random sudoku grid
    masked = mask_values(grid[:], mask_percentage)  # mask it
    while True:
        # Try to solve it two times and if both are equal to the grid originally created, assume the solution is unique
        # Else try again
        if not grid == __solve_rec(masked, 0, 0) or not grid == __solve_rec(masked, random.randint(0, 8),
                                                                            random.randint(0, 8)):
            grid = generate_grid()
            masked = mask_values(grid, mask_percentage)
        break
    return masked
