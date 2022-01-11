import common
import intcode


class Computers:
    def __init__(self, code):
        self.computers = []
        for i in range(50):
            computer = intcode.Intcode(code, pause_on_no_inputs=True)
            computer.input_list.append(i)
            self.computers.append(computer)

        self.NAT = ()

    def step(self):
        is_idle = True
        for computer in self.computers:
            if computer.input_pointer == len(computer.input_list):
                computer.input_list.append(-1)
            else:
                is_idle = False
            computer.step_all()

            while computer.output_list:
                destination = computer.output_list.pop(0)
                X = computer.output_list.pop(0)
                Y = computer.output_list.pop(0)
                if 0 <= destination < 50:
                    self.computers[destination].input_list.append(X)
                    self.computers[destination].input_list.append(Y)
                elif destination == 255:
                    self.NAT = (X, Y)

        if is_idle:
            print(f"Sending {self.NAT} to 0")
            self.computers[0].input_list.append(self.NAT[0])
            self.computers[0].input_list.append(self.NAT[1])
            return True
        else:
            return False

    def step_until_255(self):
        while not self.NAT:
            self.step()

        return self.NAT[1]

    def step_until_repeat_NAT(self):
        previous_NAT = -1
        while True:
            restarted = self.step()
            if restarted:
                if previous_NAT == self.NAT[1]:
                    return previous_NAT
                else:
                    previous_NAT = self.NAT[1]


if __name__ == "__main__":
    code = common.import_file(("../input/day23"))
    comps = Computers(code)
    common.part(1, comps.step_until_255())

    comps = Computers(code)
    common.part(2, comps.step_until_repeat_NAT())
