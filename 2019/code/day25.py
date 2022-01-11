from copy import deepcopy

import common
from day21 import Ascii

class Environment(Ascii):
    def __init__(self, code):
        super().__init__(code, pause_on_no_inputs=True)

    def prompt(self):
        command = input("Enter instruction: ")

        self.run_on_ascii(command + "\n")

    def go(self):
        paused = False
        while True:
            self.prompt()

if __name__ == "__main__":
    code = common.import_file('../input/day25')
    game = Environment(code)
    game.go()