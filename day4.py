import numpy as np

import common

class Bingo:
    """
    A single bingo board
    """
    def __init__(self, board):
        self.board = board
        self.marked = np.zeros_like(board, dtype=bool)

    def step(self, number):
        if number in self.board:
            self.marked[self.board == number] = True

        # Check if finished
        if np.any(np.sum(self.marked, axis=0) == 5):
            return True
        if np.any(np.sum(self.marked, axis=1) == 5):
            return True

        return False

    def get_sum(self):
        # Get metric for this board
        return np.sum(self.board * (1-self.marked).astype(int))


class ManyBingo:
    def __init__(self, boards):
        # Store all the boards
        self.bingos = [Bingo(b) for b in boards]

    def step(self, command):
        for b in self.bingos:
            is_finished = b.step(command)
            if is_finished:
                return b.get_sum()*command

        return None

    def step_all(self, command_list):
        for c in command_list:
            out = self.step(c)
            if out:
                return out


class ManyBingoLosing:
    def __init__(self, boards):
        self.bingos = [Bingo(b) for b in boards]

        # Keep track of finished boards
        self.finished_list = np.zeros(len(self.bingos), dtype=bool)

    def step(self, command):
        for i, b in enumerate(self.bingos):
            if not self.finished_list[i]:
                # Skip if already done
                is_finished = b.step(command)
                if is_finished:
                    # Mark as done
                    self.finished_list[i] = True

                if np.all(self.finished_list):
                    # All boards done: return
                    return b.get_sum()*command

        return None

    def step_all(self, command_list):
        for c in command_list:
            out = self.step(c)
            if out:
                return out


if __name__ == "__main__":
    text = common.import_file('input/day4_input')

    chunks = text.split('\n\n')
    commands = [int(c) for c in chunks[0].split(',')]
    boards = []
    for c in chunks[1:]:
        lines = c.split('\n')
        nums = []
        for line in lines:
            if line:
                nums.append([int(line[3 * j:(3 * j + 2)]) for j in range(5)])
        boards.append(np.array(nums))

    test = ManyBingo(boards)
    print(f"Part 1: {test.step_all(commands)}")

    test2 = ManyBingoLosing(boards)
    print(f"Part 2: {test2.step_all(commands)}")