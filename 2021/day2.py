import common


class Position:
    def __init__(self):
        self.forward = 0
        self.depth = 0

    def step(self, command: str):
        direction, distance = command.split(" ")
        if direction == "forward":
            self.forward += int(distance)
        elif direction == "down":
            self.depth += int(distance)
        elif direction == "up":
            self.depth -= int(distance)

    def step_all(self, command_list: str):
        for command in command_list.split("\n"):
            self.step(command)

    def return_total(self) -> int:
        return self.depth * self.forward


class Position2:
    def __init__(self):
        self.forward = 0
        self.depth = 0
        self.aim = 0

    def step(self, command: str):
        direction, distance = command.split(" ")
        if direction == "forward":
            self.forward += int(distance)
            self.depth += self.aim * int(distance)
        elif direction == "down":
            self.aim += int(distance)
        elif direction == "up":
            self.aim -= int(distance)

    def step_all(self, command_list: str):
        for command in command_list.split("\n"):
            self.step(command)

    def return_total(self) -> int:
        return self.depth * self.forward


if __name__ == "__main__":
    text = common.import_file("input/day2_input")

    """
    Part 1
    """
    pos = Position()
    pos.step_all(text)
    print(f"Part 1: {pos.return_total()}")

    """
    Part 2
    """
    pos = Position2()
    pos.step_all(text)
    print(f"Part 2: {pos.return_total()}")